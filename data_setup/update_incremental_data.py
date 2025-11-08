"""
Incremental Data Update Script for ACME Intelligence
Updates existing scheduled jobs to completed status and adds new data
through the current date (Oct 20, 2025)

This maintains data consistency and demo narratives.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import random
import logging
from snowflake_connection import SnowflakeConnection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IncrementalDataUpdater:
    """Updates ACME data incrementally without regenerating everything"""
    
    def __init__(self, connection_name: str = 'snowflake_intelligence'):
        self.connection_name = connection_name
        # Underperforming technicians from original data
        self.underperforming_technicians = ['TECH_015', 'TECH_023']
        
        # Seed for reproducible results
        random.seed(42)
        np.random.seed(42)
        
    def get_jobs_to_complete(self, conn: SnowflakeConnection, 
                            start_date: str, end_date: str) -> pd.DataFrame:
        """Get jobs that are scheduled but not completed in date range"""
        query = f"""
        SELECT 
            job_id,
            customer_id,
            technician_id,
            job_type,
            scheduled_date,
            job_status,
            job_revenue,
            job_duration_hours
        FROM ACME_INTELLIGENCE.RAW.JOBS
        WHERE scheduled_date BETWEEN '{start_date}' AND '{end_date}'
          AND job_status = 'Scheduled'
        ORDER BY scheduled_date
        """
        
        result = conn.fetch(query)
        if not result:
            logger.info("No jobs found to complete in date range")
            return pd.DataFrame()
            
        # Convert to DataFrame
        jobs_df = pd.DataFrame([dict(row.as_dict()) for row in result])
        logger.info(f"Found {len(jobs_df)} jobs to mark as completed")
        return jobs_df
        
    def complete_jobs(self, conn: SnowflakeConnection, 
                     start_date: str, end_date: str) -> int:
        """Mark scheduled jobs as completed with realistic completion dates"""
        
        jobs_df = self.get_jobs_to_complete(conn, start_date, end_date)
        
        if jobs_df.empty:
            logger.info("No jobs to complete")
            return 0
            
        # Update each job
        completed_count = 0
        for _, job in jobs_df.iterrows():
            # Completed 0-3 days after scheduled (realistic completion window)
            days_to_complete = random.randint(0, 3)
            completed_date = job['SCHEDULED_DATE'] + timedelta(days=days_to_complete)
            
            # Don't complete jobs in the future
            if completed_date > datetime.now().date():
                continue
                
            update_query = f"""
            UPDATE ACME_INTELLIGENCE.RAW.JOBS
            SET 
                job_status = 'Completed',
                completed_date = '{completed_date}',
                updated_at = CURRENT_TIMESTAMP()
            WHERE job_id = '{job['JOB_ID']}'
            """
            
            conn.execute(update_query)
            completed_count += 1
            
        logger.info(f"✅ Marked {completed_count} jobs as completed")
        return completed_count
        
    def generate_reviews_for_completed_jobs(self, conn: SnowflakeConnection,
                                           start_date: str, end_date: str) -> int:
        """Generate reviews for newly completed jobs (60% review rate)"""
        
        # Get recently completed jobs without reviews
        query = f"""
        SELECT 
            j.job_id,
            j.customer_id,
            j.technician_id,
            j.completed_date
        FROM ACME_INTELLIGENCE.RAW.JOBS j
        LEFT JOIN ACME_INTELLIGENCE.RAW.REVIEWS r ON j.job_id = r.job_id
        WHERE j.completed_date BETWEEN '{start_date}' AND '{end_date}'
          AND j.job_status = 'Completed'
          AND r.review_id IS NULL
        """
        
        result = conn.fetch(query)
        if not result:
            logger.info("No jobs found needing reviews")
            return 0
            
        jobs_df = pd.DataFrame([dict(row.as_dict()) for row in result])
        logger.info(f"Found {len(jobs_df)} completed jobs without reviews")
        
        # Generate reviews for ~60% of completed jobs
        jobs_to_review = jobs_df.sample(frac=0.6)
        
        # Positive review templates
        positive_reviews = [
            "Excellent service! Technician was professional and knowledgeable.",
            "Great work, arrived on time and fixed the issue quickly.",
            "Very satisfied with the quality of work and customer service.",
            "Professional, courteous, and did a thorough job.",
            "Highly recommend! Great communication throughout the process.",
            "Outstanding service, will definitely use again.",
            "Technician was very skilled and explained everything clearly.",
            "Prompt, professional, and reasonably priced.",
            "Excellent workmanship and attention to detail.",
            "Very pleased with the service and results."
        ]
        
        # Negative review templates for underperforming technicians
        negative_reviews = [
            "Technician arrived late and seemed unprepared. Had to come back twice to fix the issue properly.",
            "Poor workmanship. The problem returned within a week and had to call another company.",
            "Unprofessional behavior and left the work area messy. Not satisfied with the service.",
            "Overcharged for simple repair and didn't explain what was being done.",
            "Technician was rude and dismissive when I asked questions about the work.",
            "Sloppy work that created more problems than it solved. Very disappointed.",
            "Showed up without proper tools and had to reschedule multiple times.",
            "Did not follow safety protocols and damaged other equipment in the process.",
            "Incomplete work and poor communication. Would not recommend.",
            "Charged for parts that weren't needed and work was substandard."
        ]
        
        review_sources = ['Google', 'Yelp', 'ACME Services', 'Direct']
        
        # Get next review ID
        max_review_result = conn.fetch("SELECT MAX(CAST(SUBSTRING(review_id, 5) AS INTEGER)) as max_id FROM ACME_INTELLIGENCE.RAW.REVIEWS")
        next_review_num = max_review_result[0]['MAX_ID'] + 1 if max_review_result[0]['MAX_ID'] else 1
        
        reviews_added = 0
        for _, job in jobs_to_review.iterrows():
            review_id = f"REV_{next_review_num:05d}"
            
            # Determine if this is an underperforming technician
            is_underperformer = job['TECHNICIAN_ID'] in self.underperforming_technicians
            
            # Generate rating based on technician performance
            if is_underperformer:
                # Underperformers get mostly 1-2 star reviews (80% bad, 20% mediocre)
                if random.random() < 0.8:
                    rating = random.choice([1, 2])
                    review_text = random.choice(negative_reviews)
                else:
                    rating = 3
                    review_text = "Service was okay but could have been better."
            else:
                # Normal technicians get mostly good reviews
                rating_weights = {5: 0.5, 4: 0.3, 3: 0.15, 2: 0.04, 1: 0.01}
                rating = np.random.choice(list(rating_weights.keys()), p=list(rating_weights.values()))
                
                if rating >= 4:
                    review_text = random.choice(positive_reviews)
                elif rating == 3:
                    review_text = "Service was adequate, met expectations."
                else:
                    review_text = random.choice(negative_reviews)
            
            # Review date is usually within a few days of job completion
            review_date = job['COMPLETED_DATE'] + timedelta(days=random.randint(0, 7))
            
            # Don't create reviews in the future
            if review_date > datetime.now().date():
                review_date = datetime.now().date()
            
            review_source = random.choice(review_sources)
            is_verified = random.choice([True, False])
            
            insert_query = f"""
            INSERT INTO ACME_INTELLIGENCE.RAW.REVIEWS 
            (review_id, job_id, customer_id, technician_id, rating, review_text, 
             review_source, review_date, is_verified, created_at)
            VALUES (
                '{review_id}',
                '{job['JOB_ID']}',
                '{job['CUSTOMER_ID']}',
                '{job['TECHNICIAN_ID']}',
                {rating},
                '{review_text.replace("'", "''")}',
                '{review_source}',
                '{review_date}',
                {is_verified},
                CURRENT_TIMESTAMP()
            )
            """
            
            conn.execute(insert_query)
            reviews_added += 1
            next_review_num += 1
            
        logger.info(f"✅ Added {reviews_added} new reviews")
        return reviews_added
        
    def expire_contracts(self, conn: SnowflakeConnection, as_of_date: str) -> int:
        """Mark contracts as expired if their end_date has passed"""
        
        # Find contracts that should be expired
        query = f"""
        SELECT id, account_id, end_date
        FROM ACME_INTELLIGENCE.RAW.CONTRACTS
        WHERE status = 'Activated'
          AND end_date < '{as_of_date}'
        """
        
        result = conn.fetch(query)
        if not result:
            logger.info("No contracts found that need to be expired")
            return 0
            
        contracts_df = pd.DataFrame([dict(row.as_dict()) for row in result])
        logger.info(f"Found {len(contracts_df)} contracts to mark as expired")
        
        # Update each contract
        for _, contract in contracts_df.iterrows():
            update_query = f"""
            UPDATE ACME_INTELLIGENCE.RAW.CONTRACTS
            SET status = 'Expired'
            WHERE id = '{contract['ID']}'
            """
            
            conn.execute(update_query)
            
        logger.info(f"✅ Marked {len(contracts_df)} contracts as expired")
        return len(contracts_df)
    
    def add_october_billing(self, conn: SnowflakeConnection) -> int:
        """Add October 2025 billing data for ACME Platform"""
        
        # Get accounts that have billing enabled
        accounts_query = """
        SELECT 
            a.id as account_id,
            a.tenant_id_c,
            a.tenant_name_c,
            c.id as contract_id
        FROM ACME_INTELLIGENCE.RAW.ACCOUNTS a
        JOIN ACME_INTELLIGENCE.RAW.CONTRACTS c ON a.id = c.account_id
        WHERE (a.billing_enabled_c = 'Schedule Engine' OR a.product_billed_in_sf_c = TRUE)
          AND c.status = 'Activated'
          AND c.start_date <= '2025-10-01'
          AND c.end_date >= '2025-10-01'
        """
        
        result = conn.fetch(accounts_query)
        if not result:
            logger.warning("No active accounts found for billing")
            return 0
            
        accounts_df = pd.DataFrame([dict(row.as_dict()) for row in result])
        logger.info(f"Found {len(accounts_df)} accounts with active contracts for October billing")
        
        # ACME Platform SKUs (from original generator)
        acme_product_skus = {
            1: 'Enterprise Plus Office User',
            2: 'Professional Plus Office User', 
            4: 'Team Plus Office User',
            8: 'Mobile Office User',
            32: 'Premium Mobile User',
            64: 'Standard Office User',
            128: 'Standard Mobile User',
            256: 'Professional Office User',
            512: 'Professional Mobile User',
            1295: 'Marketing Pro - Contacts',
            1297: 'Dispatch Pro',
            1338: 'Project Tracking',
            1360: 'Sales Pro'
        }
        
        # Get next invoice ID
        max_invoice_result = conn.fetch("SELECT MAX(CAST(SUBSTRING(id, 10) AS INTEGER)) as max_id FROM ACME_INTELLIGENCE.RAW.ACME_BILLING_DATA WHERE id LIKE 'ACME_INV_%'")
        next_invoice_num = max_invoice_result[0]['MAX_ID'] + 1 if max_invoice_result[0]['MAX_ID'] else 1
        
        invoices_added = 0
        trans_date = date(2025, 10, 1)
        
        for _, account in accounts_df.iterrows():
            # Generate 1-3 invoices per account for October
            num_invoices = random.randint(1, 3)
            
            for _ in range(num_invoices):
                invoice_id = f"ACME_INV_{next_invoice_num:05d}"
                
                # Select random SKU
                sku = random.choice(list(acme_product_skus.keys()))
                description = acme_product_skus[sku]
                
                # Generate realistic pricing
                quantity = random.randint(1, 10)
                base_item_price = round(random.uniform(25, 200), 2)
                variance_factor = random.uniform(0.75, 1.3)
                item_price = round(base_item_price * variance_factor, 2)
                amount = quantity * item_price
                tax = round(amount * 0.08, 2)
                
                insert_query = f"""
                INSERT INTO ACME_INTELLIGENCE.RAW.ACME_BILLING_DATA
                (_tenant_id, _tenant_name, account_id, contract_id, id, trans_date,
                 description, amount, tax, type, balancetype, active, isexported,
                 invoice_id, sku, itemprice, quantity)
                VALUES (
                    {account['TENANT_ID_C']},
                    '{account['TENANT_NAME_C'].replace("'", "''")}',
                    '{account['ACCOUNT_ID']}',
                    '{account['CONTRACT_ID']}',
                    '{invoice_id}',
                    '{trans_date}',
                    'Monthly billing - {description} - Contract: {account['CONTRACT_ID']}',
                    {amount},
                    {tax},
                    0,
                    0,
                    TRUE,
                    TRUE,
                    '{invoice_id}',
                    {sku},
                    {item_price},
                    {quantity}
                )
                """
                
                conn.execute(insert_query)
                invoices_added += 1
                next_invoice_num += 1
                
        logger.info(f"✅ Added {invoices_added} October billing records")
        return invoices_added
        
    def run_incremental_update(self, start_date: str = '2025-09-16', 
                              end_date: str = '2025-10-20') -> dict:
        """Run the complete incremental update process"""
        logger.info("="*60)
        logger.info("ACME INTELLIGENCE - INCREMENTAL DATA UPDATE")
        logger.info("="*60)
        logger.info(f"Update period: {start_date} to {end_date}")
        logger.info("")
        
        try:
            # Connect using Snow CLI configuration
            conn = SnowflakeConnection.from_snow_cli(self.connection_name)
            
            # Ensure we're in the right database and schema
            conn.execute("USE DATABASE ACME_INTELLIGENCE")
            conn.execute("USE SCHEMA RAW")
            
            results = {}
            
            # Step 1: Complete scheduled jobs
            logger.info("Step 1: Completing scheduled jobs...")
            results['jobs_completed'] = self.complete_jobs(conn, start_date, end_date)
            
            # Step 2: Generate reviews for completed jobs
            logger.info("\nStep 2: Generating reviews for completed jobs...")
            results['reviews_added'] = self.generate_reviews_for_completed_jobs(conn, start_date, end_date)
            
            # Step 3: Expire contracts that have ended
            logger.info("\nStep 3: Expiring contracts that have ended...")
            results['contracts_expired'] = self.expire_contracts(conn, end_date)
            
            # Step 4: Add October billing data
            logger.info("\nStep 4: Adding October 2025 billing data...")
            results['billing_records_added'] = self.add_october_billing(conn)
            
            conn.close()
            
            # Print summary
            logger.info("\n" + "="*60)
            logger.info("INCREMENTAL UPDATE SUMMARY")
            logger.info("="*60)
            logger.info(f"Jobs completed: {results['jobs_completed']}")
            logger.info(f"Reviews added: {results['reviews_added']}")
            logger.info(f"Contracts expired: {results['contracts_expired']}")
            logger.info(f"Billing records added: {results['billing_records_added']}")
            logger.info("="*60)
            logger.info("✅ Incremental update completed successfully!")
            logger.info("\n⚠️  NEXT STEP: Run dbt to refresh mart tables")
            logger.info("    cd ../acme_intelligence && dbt run")
            
            return results
            
        except Exception as e:
            logger.error(f"Error during incremental update: {str(e)}")
            raise

def main():
    """Main function to run incremental data update"""
    updater = IncrementalDataUpdater(connection_name='snowflake_intelligence')
    
    # Update from Sept 16 (last completed review) through Oct 20 (today)
    results = updater.run_incremental_update(
        start_date='2025-09-16',
        end_date='2025-10-20'
    )
    
    print("\n🎉 Your ACME Intelligence data is now up-to-date through October 20, 2025!")
    print("\n📊 IMPORTANT: Run dbt to refresh your mart tables and semantic views:")
    print("   cd ../acme_intelligence && dbt run")
    print("\nYou can run this script again anytime to add more incremental data.")

if __name__ == "__main__":
    main()

