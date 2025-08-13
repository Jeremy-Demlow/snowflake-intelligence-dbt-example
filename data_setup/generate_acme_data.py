"""
ACME Intelligence Demo - Data Generation Script
Creates realistic sample data for the demo with built-in narrative elements:
- Underperforming technicians with poor reviews
- Clear business impact for the demo story
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import random
from typing import Dict
import logging
from snowflake_connection import SnowflakeConnection

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ACMEServicesDataGenerator:
    """Generates realistic ACME Services data for the intelligence demo"""
    
    def __init__(self, num_customers: int = 50, num_technicians: int = 25, 
                 start_date: str = '2024-01-01', end_date: str = '2025-12-31'):
        self.num_customers = num_customers
        self.num_technicians = num_technicians
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Demo narrative elements - these are the "problem" technicians
        self.underperforming_technicians = ['TECH_015', 'TECH_023']
        
        # Seed for reproducible results
        random.seed(42)
        np.random.seed(42)
        
        # Industry distributions
        self.industries = {
            'HVAC': 0.40,
            'Plumbing': 0.30, 
            'Electrical': 0.20,
            'Roofing': 0.10
        }
        
        self.company_sizes = {
            'Small': 0.60,    # 1-10 employees
            'Medium': 0.30,   # 11-50 employees  
            'Large': 0.10     # 50+ employees
        }
        
        self.subscription_tiers = {
            'Basic': 0.50,
            'Pro': 0.35,
            'Enterprise': 0.15
        }
        
        # NDR-specific segmentation for financial analytics
        self.size_segments = {
            'SMB': 0.60,        # Small/Medium Business
            'Mid-Market': 0.25, # Mid-Market  
            'Enterprise': 0.15  # Enterprise
        }
        
        self.market_segments = {
            'Residential': 0.40,
            'Commercial': 0.35, 
            'Industrial': 0.25
        }
        
        self.trade_segments = {
            'HVAC': 0.40,
            'Plumbing': 0.30,
            'Electrical': 0.20,
            'Multi-Trade': 0.10
        }
        
        self.product_categories = {
            'Core Platform': 0.50,
            'Add-on Modules': 0.30,
            'Premium Features': 0.20
        }
        
        # Parent-child account structure for NDR
        self.num_parent_accounts = 15  # Large enterprise customers
        self.num_child_accounts = 35   # Sub-accounts under parents
        
        self.job_types = {
            'Installation': 0.25,
            'Repair': 0.40,
            'Maintenance': 0.25,
            'Emergency': 0.10
        }
        
        self.review_sources = {
            'Google': 0.40,
            'Yelp': 0.25,
            'ACME Services': 0.20,
            'Direct': 0.15
        }
        
        # US states for realistic addresses
        self.states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
                      'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
        
        self.cities = ['Los Angeles', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
                      'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
                      'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis']
    
    def _weighted_choice(self, choices: Dict[str, float]) -> str:
        """Make a weighted random choice from a dictionary of options"""
        items = list(choices.keys())
        weights = list(choices.values())
        return np.random.choice(items, p=weights)
    
    def generate_customers(self) -> pd.DataFrame:
        """Generate customer companies using ACME Services"""
        logger.info(f"Generating {self.num_customers} customer companies...")
        
        customers = []
        company_names = [
            "Comfort Zone HVAC", "Premier Plumbing Solutions", "Elite Electric Services",
            "Reliable Roofing Co", "Quick Fix Plumbing", "Arctic Air Conditioning",
            "Sparks Electric", "Home Comfort Specialists", "24/7 Emergency Services",
            "Professional HVAC Solutions", "Master Plumbers Inc", "Bright Electric",
            "Superior Heating & Cooling", "Flow Right Plumbing", "Power Pro Electric",
            "Climate Control Experts", "Pipe Dreams Plumbing", "Voltage Electric",
            "Temperature Masters", "Drain Busters", "Circuit Solutions",
            "Cool Breeze HVAC", "Leak Stoppers", "Amp Electric Services",
            "Thermal Dynamics", "Water Works Plumbing", "Lightning Electric",
            "Air Quality Solutions", "Pipe Repair Pros", "Current Electric",
            "Heating Heroes", "Plumbing Perfection", "Electric Excellence",
            "Climate Craft", "Aqua Solutions", "Wired Right Electric",
            "Comfort First HVAC", "Pipe Pro Services", "Shock Electric",
            "Temperature Tech", "H2O Heroes", "Electric Edge",
            "Air Experts", "Drain Doctors", "Power Pulse Electric",
            "HVAC Harmony", "Plumbing Plus", "Electric Empower",
            "Cool Solutions", "Pipe Patrol", "Voltage Vanguard"
        ]
        
        for i in range(self.num_customers):
            customer_id = f"CUST_{str(i+1).zfill(3)}"
            industry = self._weighted_choice(self.industries)
            company_size = self._weighted_choice(self.company_sizes)
            tier = self._weighted_choice(self.subscription_tiers)
            
            # Set monthly revenue based on size and tier
            base_revenue = {
                'Small': {'Basic': 150, 'Pro': 300, 'Enterprise': 500},
                'Medium': {'Basic': 400, 'Pro': 800, 'Enterprise': 1200},
                'Large': {'Basic': 800, 'Pro': 1500, 'Enterprise': 2500}
            }
            
            monthly_revenue = base_revenue[company_size][tier] * np.random.uniform(0.8, 1.2)
            
            # Generate signup date (mostly in 2024, some in 2023)
            if random.random() < 0.8:
                signup_start = datetime(2024, 1, 1).date()
                signup_end = datetime(2024, 12, 31).date()
            else:
                signup_start = datetime(2023, 1, 1).date()
                signup_end = datetime(2023, 12, 31).date()
                
            signup_date = signup_start + timedelta(
                days=random.randint(0, (signup_end - signup_start).days)
            )
            
            customer = {
                'customer_id': customer_id,
                'company_name': company_names[i] if i < len(company_names) else f"ServiceCo {i+1}",
                'industry': industry,
                'company_size': company_size,
                'location_state': random.choice(self.states),
                'location_city': random.choice(self.cities),
                'signup_date': signup_date,
                'subscription_tier': tier,
                'monthly_revenue': round(monthly_revenue, 2),
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            customers.append(customer)
        
        return pd.DataFrame(customers)
    
    def generate_technicians(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Generate technician data with built-in underperformers"""
        logger.info(f"Generating {self.num_technicians} technicians...")
        
        first_names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
                      'Thomas', 'Christopher', 'Charles', 'Daniel', 'Matthew', 'Anthony', 'Mark',
                      'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth', 'Kevin', 'Brian',
                      'George', 'Timothy', 'Ronald', 'Jason', 'Edward', 'Jeffrey', 'Ryan']
        
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                     'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
                     'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
                     'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson']
        
        technicians = []
        
        for i in range(self.num_technicians):
            tech_id = f"TECH_{str(i+1).zfill(3)}"
            
            # Assign to random customer
            customer_id = random.choice(customers_df['customer_id'].tolist())
            customer_industry = customers_df[customers_df['customer_id'] == customer_id]['industry'].iloc[0]
            
            # Specialization usually matches customer industry
            if random.random() < 0.8:
                specialization = customer_industry
            else:
                specialization = random.choice(list(self.industries.keys()))
            
            # Generate hire date (mostly recent hires, some veterans)
            if random.random() < 0.6:
                # Recent hires (last 2 years)
                hire_start = datetime(2023, 1, 1).date()
                hire_end = datetime(2024, 12, 31).date()
            else:
                # Veterans (2-10 years ago)
                hire_start = datetime(2015, 1, 1).date()
                hire_end = datetime(2022, 12, 31).date()
            
            hire_date = hire_start + timedelta(
                days=random.randint(0, (hire_end - hire_start).days)
            )
            
            years_experience = (datetime.now().date() - hire_date).days / 365.25
            
            # Certification level based on experience
            if years_experience < 1:
                cert_level = 'Junior'
            elif years_experience < 5:
                cert_level = 'Senior' 
            else:
                cert_level = 'Expert'
            
            # Special handling for underperforming technicians
            if tech_id in self.underperforming_technicians:
                # Make them newer hires with less experience
                hire_date = datetime(2024, 6, 1).date() + timedelta(days=random.randint(0, 120))
                years_experience = (datetime.now().date() - hire_date).days / 365.25
                cert_level = 'Junior'
            
            technician = {
                'technician_id': tech_id,
                'customer_id': customer_id,
                'first_name': random.choice(first_names),
                'last_name': random.choice(last_names),
                'hire_date': hire_date,
                'specialization': specialization,
                'certification_level': cert_level,
                'years_experience': round(years_experience, 1),
                'is_active': True,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            technicians.append(technician)
        
        return pd.DataFrame(technicians)
    
    def generate_jobs(self, customers_df: pd.DataFrame, technicians_df: pd.DataFrame) -> pd.DataFrame:
        """Generate job data with realistic patterns"""
        logger.info("Generating job data...")
        
        # Generate more jobs for the demo (about 20-30 jobs per technician)
        total_jobs = self.num_technicians * random.randint(20, 30)
        jobs = []
        
        for i in range(total_jobs):
            job_id = f"JOB_{str(i+1).zfill(5)}"
            
            # Pick random technician and their customer
            technician = technicians_df.sample(1).iloc[0]
            technician_id = technician['technician_id']
            customer_id = technician['customer_id']
            
            job_type = self._weighted_choice(self.job_types)
            
            # Generate scheduled date (spread across our date range)
            days_range = (self.end_date - self.start_date).days
            scheduled_date = self.start_date + timedelta(days=random.randint(0, days_range))
            
            # Most jobs are completed (90%), some are in progress or cancelled
            status_weights = {'Completed': 0.90, 'In Progress': 0.05, 'Cancelled': 0.05}
            job_status = self._weighted_choice(status_weights)
            
            # Completed date (if completed)
            completed_date = None
            if job_status == 'Completed':
                # Usually completed within 1-3 days of scheduling
                completed_date = scheduled_date + timedelta(days=random.randint(0, 3))
                # Don't complete jobs in the future
                if completed_date > datetime.now().date():
                    completed_date = None
                    job_status = 'Scheduled'
            
            # Job revenue based on type and customer tier
            customer_info = customers_df[customers_df['customer_id'] == customer_id].iloc[0]
            tier_multiplier = {'Basic': 1.0, 'Pro': 1.3, 'Enterprise': 1.6}[customer_info['subscription_tier']]
            
            base_revenue = {
                'Installation': 800,
                'Repair': 300,
                'Maintenance': 200,
                'Emergency': 500
            }
            
            job_revenue = base_revenue[job_type] * tier_multiplier * np.random.uniform(0.7, 1.5)
            
            # Duration based on job type
            base_duration = {
                'Installation': 4.0,
                'Repair': 2.0,
                'Maintenance': 1.5,
                'Emergency': 3.0
            }
            
            job_duration = base_duration[job_type] * np.random.uniform(0.5, 1.8)
            
            # Service address
            service_address = f"{random.randint(100, 9999)} {random.choice(['Main St', 'Oak Ave', 'Elm Dr', 'Pine Rd', 'Cedar Ln'])}, {customer_info['location_city']}, {customer_info['location_state']}"
            
            job_description = f"{job_type} service for {technician['specialization']} system"
            
            job = {
                'job_id': job_id,
                'customer_id': customer_id,
                'technician_id': technician_id,
                'job_type': job_type,
                'job_status': job_status,
                'scheduled_date': scheduled_date,
                'completed_date': completed_date,
                'job_revenue': round(job_revenue, 2),
                'job_duration_hours': round(job_duration, 2),
                'service_address': service_address,
                'job_description': job_description,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            }
            
            jobs.append(job)
        
        return pd.DataFrame(jobs)
    
    def generate_reviews(self, jobs_df: pd.DataFrame, customers_df: pd.DataFrame, 
                        technicians_df: pd.DataFrame) -> pd.DataFrame:
        """Generate review data with built-in poor reviews for underperforming technicians"""
        logger.info("Generating review data with narrative elements...")
        
        # Only generate reviews for completed jobs (about 60% get reviews)
        completed_jobs = jobs_df[jobs_df['job_status'] == 'Completed'].copy()
        review_jobs = completed_jobs.sample(frac=0.6)
        
        reviews = []
        
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
        
        for _, job in review_jobs.iterrows():
            review_id = f"REV_{len(reviews)+1:05d}"
            
            # Determine if this is an underperforming technician
            is_underperformer = job['technician_id'] in self.underperforming_technicians
            
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
                rating = self._weighted_choice(rating_weights)
                
                if rating >= 4:
                    review_text = random.choice(positive_reviews)
                elif rating == 3:
                    review_text = "Service was adequate, met expectations."
                else:
                    review_text = random.choice(negative_reviews)
            
            # Review date is usually within a few days of job completion
            if job['completed_date']:
                review_date = job['completed_date'] + timedelta(days=random.randint(0, 7))
                # Don't create reviews in the future
                if review_date > datetime.now().date():
                    review_date = datetime.now().date()
            else:
                continue  # Skip if no completion date
            
            review_source = self._weighted_choice(self.review_sources)
            
            review = {
                'review_id': review_id,
                'job_id': job['job_id'],
                'customer_id': job['customer_id'],
                'technician_id': job['technician_id'],
                'rating': rating,
                'review_text': review_text,
                'review_source': review_source,
                'review_date': review_date,
                'is_verified': random.choice([True, False]),
                'created_at': datetime.now()
            }
            
            reviews.append(review)
        
        return pd.DataFrame(reviews)
    
    def load_data_to_snowflake(self, customers_df: pd.DataFrame, technicians_df: pd.DataFrame,
                              jobs_df: pd.DataFrame, reviews_df: pd.DataFrame,
                              tenant_hierarchy_df: pd.DataFrame, customer_segments_df: pd.DataFrame,
                              billing_metrics_df: pd.DataFrame):
        """Load all generated data into Snowflake"""
        logger.info("Connecting to Snowflake and loading data...")
        
        try:
            # Connect using Snow CLI configuration
            conn = SnowflakeConnection.from_snow_cli('snowflake_intelligence')
            
            # Ensure we're in the right database and schema
            conn.execute("USE DATABASE ACME_INTELLIGENCE")
            conn.execute("USE SCHEMA RAW")
            
            # Clear existing data
            logger.info("Clearing existing data...")
            conn.execute("DELETE FROM REVIEWS")
            conn.execute("DELETE FROM JOBS") 
            conn.execute("DELETE FROM TECHNICIANS")
            conn.execute("DELETE FROM CUSTOMERS")
            # Clear NDR tables
            conn.execute("DELETE FROM BILLING_METRICS")
            conn.execute("DELETE FROM CUSTOMER_SEGMENTS")  
            conn.execute("DELETE FROM TENANT_HIERARCHY")
            
            # Load customers
            logger.info(f"Loading {len(customers_df)} customers...")
            # Convert column names to uppercase for Snowflake
            customers_df.columns = customers_df.columns.str.upper()
            conn.session.write_pandas(
                customers_df, 
                table_name="CUSTOMERS",
                auto_create_table=False,
                overwrite=False
            )
            
            # Load technicians
            logger.info(f"Loading {len(technicians_df)} technicians...")
            technicians_df.columns = technicians_df.columns.str.upper()
            conn.session.write_pandas(
                technicians_df,
                table_name="TECHNICIANS", 
                auto_create_table=False,
                overwrite=False
            )
            
            # Load jobs
            logger.info(f"Loading {len(jobs_df)} jobs...")
            jobs_df.columns = jobs_df.columns.str.upper()
            conn.session.write_pandas(
                jobs_df,
                table_name="JOBS",
                auto_create_table=False,
                overwrite=False
            )
            
            # Load reviews
            logger.info(f"Loading {len(reviews_df)} reviews...")
            reviews_df.columns = reviews_df.columns.str.upper()
            conn.session.write_pandas(
                reviews_df,
                table_name="REVIEWS",
                auto_create_table=False,
                overwrite=False
            )
            
            # Load NDR data
            logger.info(f"Loading {len(tenant_hierarchy_df)} tenant hierarchy records...")
            tenant_hierarchy_df.columns = tenant_hierarchy_df.columns.str.upper()
            conn.session.write_pandas(
                tenant_hierarchy_df,
                table_name="TENANT_HIERARCHY",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(customer_segments_df)} customer segments...")
            customer_segments_df.columns = customer_segments_df.columns.str.upper()
            conn.session.write_pandas(
                customer_segments_df,
                table_name="CUSTOMER_SEGMENTS",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(billing_metrics_df)} billing metrics...")
            billing_metrics_df.columns = billing_metrics_df.columns.str.upper()
            conn.session.write_pandas(
                billing_metrics_df,
                table_name="BILLING_METRICS",
                auto_create_table=False,
                overwrite=False
            )
            
            # Verify data load
            logger.info("Verifying data load...")
            results = conn.fetch("""
                SELECT 
                    'CUSTOMERS' as table_name, COUNT(*) as row_count FROM CUSTOMERS
                UNION ALL
                SELECT 'TECHNICIANS', COUNT(*) FROM TECHNICIANS  
                UNION ALL
                SELECT 'JOBS', COUNT(*) FROM JOBS
                UNION ALL
                SELECT 'REVIEWS', COUNT(*) FROM REVIEWS
                UNION ALL
                SELECT 'TENANT_HIERARCHY', COUNT(*) FROM TENANT_HIERARCHY
                UNION ALL
                SELECT 'CUSTOMER_SEGMENTS', COUNT(*) FROM CUSTOMER_SEGMENTS
                UNION ALL
                SELECT 'BILLING_METRICS', COUNT(*) FROM BILLING_METRICS
            """)
            
            for result in results:
                logger.info(f"{result[0]}: {result[1]} rows loaded")
            
            conn.close()
            logger.info("Data loading completed successfully!")
            
        except Exception as e:
            logger.error(f"Error loading data to Snowflake: {str(e)}")
            raise
    
    def generate_tenant_hierarchy(self) -> pd.DataFrame:
        """Generate parent-child account relationships for NDR calculations"""
        logger.info("Generating tenant hierarchy...")
        
        # Create parent accounts (large enterprise customers)
        parent_accounts = []
        for i in range(1, self.num_parent_accounts + 1):
            parent_id = f"PARENT_{i:03d}"
            parent_accounts.append({
                'parent_account_id': parent_id,
                'parent_tenant_id': f"TENANT_{parent_id}",
                'parent_name': f"Enterprise Corp {i}",
                'parent_start_date': self.start_date + timedelta(days=random.randint(0, 365))
            })
        
        # Create child accounts under parents
        child_accounts = []
        for i in range(1, self.num_child_accounts + 1):
            parent_account = random.choice(parent_accounts)
            child_id = f"CHILD_{i:03d}"
            child_accounts.append({
                'child_account_id': child_id,
                'parent_account_id': parent_account['parent_account_id'],
                'child_tenant_id': f"TENANT_{child_id}",
                'ndr_parent': parent_account['parent_account_id'],
                'parent_start_date': parent_account['parent_start_date']
            })
        
        return pd.DataFrame(child_accounts)
    
    def generate_customer_segments(self, hierarchy_df: pd.DataFrame = None) -> pd.DataFrame:
        """Generate customer segmentation data for NDR analysis"""
        logger.info("Generating customer segments...")
        
        # Generate hierarchy if not provided
        if hierarchy_df is None:
            hierarchy_df = self.generate_tenant_hierarchy()
            
        # Get all unique account IDs
        all_accounts = list(hierarchy_df['parent_account_id'].unique())
        
        segments = []
        for account_id in all_accounts:
            segments.append({
                'parent_account_id': account_id,
                'size_segment': self._weighted_choice(self.size_segments),
                'market_segment': self._weighted_choice(self.market_segments),
                'trade_segment': self._weighted_choice(self.trade_segments),
                'product_category': self._weighted_choice(self.product_categories)
            })
        
        return pd.DataFrame(segments)
    
    def generate_billing_metrics(self, hierarchy_df: pd.DataFrame = None, segments_df: pd.DataFrame = None) -> pd.DataFrame:
        """Generate monthly ARR data for NDR calculations"""
        logger.info("Generating billing metrics...")
        
        # Generate dependencies if not provided
        if hierarchy_df is None:
            hierarchy_df = self.generate_tenant_hierarchy()
        if segments_df is None:
            segments_df = self.generate_customer_segments()
        
        # Generate monthly data points from 2023 to 2025 (for year-over-year comparison)
        billing_data = []
        
        # Create proper month list to avoid invalid months
        months_to_generate = []
        for year in [2023, 2024, 2025]:
            for month in range(1, 13):  # 1-12 for valid months
                months_to_generate.append({
                    'year': year,
                    'month': month,
                    'month_id': year * 100 + month,
                    'billing_month': date(year, month, 1)
                })
        
        for month_data in months_to_generate:
            month_id = month_data['month_id']
            billing_month = month_data['billing_month']
            
            for _, child_account in hierarchy_df.iterrows():
                parent_id = child_account['parent_account_id']
                
                # Get segment info for this parent
                segment_info = segments_df[segments_df['parent_account_id'] == parent_id].iloc[0]
                
                # Base ARR varies by segment
                base_arr = {
                    'SMB': random.randint(5000, 25000),
                    'Mid-Market': random.randint(25000, 100000),
                    'Enterprise': random.randint(100000, 500000)
                }[segment_info['size_segment']]
                
                # Add growth/decline trends 
                # Calculate months from Jan 2023 baseline
                months_from_start = (month_data['year'] - 2023) * 12 + (month_data['month'] - 1)
                growth_factor = 1 + (months_from_start * 0.01)  # 1% monthly growth baseline
                
                # Add some seasonality and randomness
                seasonal_factor = 1 + 0.1 * np.sin(2 * np.pi * month_data['month'] / 12)
                random_factor = random.uniform(0.8, 1.2)
                
                final_arr = base_arr * growth_factor * seasonal_factor * random_factor
                
                billing_data.append({
                    'parent_account_id': parent_id,
                    'child_account_id': child_account['child_account_id'],
                    'ndr_parent': child_account['ndr_parent'],
                    'month_id': month_id,
                    'billing_month': billing_month,
                    'l3m_arr': round(final_arr, 2),
                    'size_segment': segment_info['size_segment'],
                    'market_segment': segment_info['market_segment'],
                    'trade_segment': segment_info['trade_segment'],
                    'product_category': segment_info['product_category']
                })
        
        return pd.DataFrame(billing_data)
    
    def generate_all_data(self) -> Dict[str, pd.DataFrame]:
        """Generate all sample data for the ACME Intelligence demo"""
        logger.info("Starting ACME Intelligence demo data generation...")
        
        # Generate operational data (existing)
        customers_df = self.generate_customers()
        technicians_df = self.generate_technicians(customers_df)
        jobs_df = self.generate_jobs(customers_df, technicians_df)
        reviews_df = self.generate_reviews(jobs_df, customers_df, technicians_df)
        
        # Generate financial data (new for NDR)
        tenant_hierarchy_df = self.generate_tenant_hierarchy()
        customer_segments_df = self.generate_customer_segments(tenant_hierarchy_df)
        billing_metrics_df = self.generate_billing_metrics(tenant_hierarchy_df, customer_segments_df)
        
        # Store original dataframes for summary (before column name changes)
        orig_technicians_df = technicians_df.copy()
        
        # Load to Snowflake
        self.load_data_to_snowflake(
            customers_df, technicians_df, jobs_df, reviews_df,
            tenant_hierarchy_df, customer_segments_df, billing_metrics_df
        )
        
        # Print summary for demo narrative
        logger.info("\n" + "="*60)
        logger.info("ACME INTELLIGENCE DEMO DATA SUMMARY")
        logger.info("="*60)
        logger.info(f"Generated {len(customers_df)} service companies")
        logger.info(f"Generated {len(orig_technicians_df)} technicians")
        logger.info(f"Generated {len(jobs_df)} service jobs")
        logger.info(f"Generated {len(reviews_df)} customer reviews")
        logger.info(f"Generated {len(tenant_hierarchy_df)} tenant relationships")
        logger.info(f"Generated {len(customer_segments_df)} customer segments")
        logger.info(f"Generated {len(billing_metrics_df)} billing records for NDR")
        logger.info("\nUNDERPERFORMING TECHNICIANS FOR DEMO:")
        for tech_id in self.underperforming_technicians:
            tech_info = orig_technicians_df[orig_technicians_df['technician_id'] == tech_id].iloc[0]
            logger.info(f"- {tech_id}: {tech_info['first_name']} {tech_info['last_name']}")
        logger.info("="*60)
        
        return {
            'customers': customers_df,
            'technicians': technicians_df, 
            'jobs': jobs_df,
            'reviews': reviews_df,
            'tenant_hierarchy': tenant_hierarchy_df,
            'customer_segments': customer_segments_df,
            'billing_metrics': billing_metrics_df
        }

def main():
    """Main function to generate and load ACME Services demo data"""
    generator = ACMEServicesDataGenerator(
        num_customers=50,
        num_technicians=25,
        start_date='2024-01-01',
        end_date='2025-12-31'
    )
    
    generator.generate_all_data()
    
    print("\nACME Intelligence demo data generation completed!")
    print("You can now proceed with creating the semantic model and Snowflake Agent.")

if __name__ == "__main__":
    main()
