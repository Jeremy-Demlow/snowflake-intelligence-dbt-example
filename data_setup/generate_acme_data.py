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
    """Generates realistic ACME Services data for the intelligence demo with financial contract data"""
    
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
        
        # Financial data configuration
        self.num_products = 50  # Product catalog
        self.num_opportunities = 100  # Sales opportunities
        self.num_contracts_per_customer = 2  # Average contracts per customer
        self.avg_order_items_per_contract = 3  # Average line items per contract
        
        # ACME Platform SKU mapping (from the provided SQL)
        self.acme_product_skus = {
            1: 'Enterprise Plus Office User',
            2: 'Professional Plus Office User', 
            4: 'Team Plus Office User',
            8: 'Mobile Office User',
            32: 'Premium Mobile User',
            64: 'Standard Office User',
            128: 'Standard Mobile User',
            256: 'Professional Office User',
            512: 'Professional Mobile User',
            1025: 'Enterprise Plus Office User - ProRated',
            1026: 'Professional Plus Office User - ProRated',
            1280: 'Professional Office User - ProRated',
            1536: 'Professional Mobile User - ProRated',
            2097152: 'Managed Services',
            2098176: 'Managed Services - ProRated',
            1295: 'Marketing Pro - Contacts',
            1297: 'Dispatch Pro',
            1338: 'Project Tracking',
            1360: 'Sales Pro'
        }
        
        # Contract statuses that affect business questions
        self.contract_statuses = {
            'Activated': 0.70,  # Active contracts
            'Expired': 0.15,    # Churned contracts  
            'Terminated': 0.10, # Churned contracts
            'Draft': 0.05       # Not yet active
        }
        
        # Order statuses
        self.order_statuses = {
            'Activated': 0.75,
            'Expired': 0.15,
            'Terminated': 0.10
        }
        
        # Product families for proper categorization
        self.product_families = {
            'Recurring Revenue': 0.85,  # Monthly/annual subscriptions
            'Non-Recurring Revenue': 0.15  # One-time fees
        }
        
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
                              billing_metrics_df: pd.DataFrame, sf_products_df: pd.DataFrame,
                              sf_accounts_df: pd.DataFrame, opportunities_df: pd.DataFrame,
                              contracts_df: pd.DataFrame, orders_df: pd.DataFrame,
                              order_items_df: pd.DataFrame, sf_invoices_df: pd.DataFrame,
                              st_billing_df: pd.DataFrame, parent_child_mapping_df: pd.DataFrame,
                              tenant_sfdc_mapping_df: pd.DataFrame, documents_df: pd.DataFrame):
        """Load all generated data into Snowflake"""
        logger.info("Connecting to Snowflake and loading data...")
        
        try:
            # Connect using Snow CLI configuration
            conn = SnowflakeConnection.from_snow_cli('snowflake_intelligence')
            
            # Ensure we're in the right database and schema
            conn.execute("USE DATABASE ACME_INTELLIGENCE")
            conn.execute("USE SCHEMA RAW")
            
            # Create financial tables first (if they don't exist)
            logger.info("Setting up financial data tables...")
            self._create_financial_tables(conn)
            
            # Clear existing data safely (only if tables exist)
            logger.info("Clearing existing data...")
            self._safe_clear_tables(conn, [
                "REVIEWS", "JOBS", "TECHNICIANS", "CUSTOMERS",
                "BILLING_METRICS", "CUSTOMER_SEGMENTS", "TENANT_HIERARCHY",
                "PRODUCTS", "ACCOUNTS", "OPPORTUNITIES", "CONTRACTS", 
                "ORDERS", "ORDER_ITEMS", "INVOICES", "ACME_BILLING_DATA",
                "PARENT_CHILD_MAPPING", "TENANT_SFDC_MAPPING"
            ])
            
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
            
            # Load new financial data
            logger.info(f"Loading {len(sf_products_df)} products...")
            sf_products_df.columns = sf_products_df.columns.str.upper()
            conn.session.write_pandas(
                sf_products_df,
                table_name="PRODUCTS",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(sf_accounts_df)} accounts...")
            sf_accounts_df.columns = sf_accounts_df.columns.str.upper()
            conn.session.write_pandas(
                sf_accounts_df,
                table_name="ACCOUNTS",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(opportunities_df)} opportunities...")
            opportunities_df.columns = opportunities_df.columns.str.upper()
            conn.session.write_pandas(
                opportunities_df,
                table_name="OPPORTUNITIES",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(contracts_df)} contracts...")
            contracts_df.columns = contracts_df.columns.str.upper()
            conn.session.write_pandas(
                contracts_df,
                table_name="CONTRACTS",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(orders_df)} orders...")
            orders_df.columns = orders_df.columns.str.upper()
            conn.session.write_pandas(
                orders_df,
                table_name="ORDERS",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(order_items_df)} order items...")
            order_items_df.columns = order_items_df.columns.str.upper()
            conn.session.write_pandas(
                order_items_df,
                table_name="ORDER_ITEMS",
                auto_create_table=False,
                overwrite=False
            )
            
            if not sf_invoices_df.empty:
                logger.info(f"Loading {len(sf_invoices_df)} SFDC invoices...")
                sf_invoices_df.columns = sf_invoices_df.columns.str.upper()
                conn.session.write_pandas(
                    sf_invoices_df,
                    table_name="INVOICES",
                    auto_create_table=False,
                    overwrite=False
                )
            
            logger.info(f"Loading {len(st_billing_df)} ACME Platform billing records...")
            st_billing_df.columns = st_billing_df.columns.str.upper()
            conn.session.write_pandas(
                st_billing_df,
                table_name="ACME_BILLING_DATA",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(parent_child_mapping_df)} parent-child mappings...")
            parent_child_mapping_df.columns = parent_child_mapping_df.columns.str.upper()
            conn.session.write_pandas(
                parent_child_mapping_df,
                table_name="PARENT_CHILD_MAPPING",
                auto_create_table=False,
                overwrite=False
            )
            
            logger.info(f"Loading {len(tenant_sfdc_mapping_df)} tenant-SFDC mappings...")
            tenant_sfdc_mapping_df.columns = tenant_sfdc_mapping_df.columns.str.upper()
            conn.session.write_pandas(
                tenant_sfdc_mapping_df,
                table_name="TENANT_SFDC_MAPPING",
                auto_create_table=False,
                overwrite=False
            )
            
            # Load document content
            logger.info(f"Loading {len(documents_df)} document(s)...")
            documents_df.columns = documents_df.columns.str.upper()
            conn.session.write_pandas(
                documents_df,
                table_name="STG_PARSED_DOCUMENTS",
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
                UNION ALL
                SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
                UNION ALL
                SELECT 'ACCOUNTS', COUNT(*) FROM ACCOUNTS
                UNION ALL
                SELECT 'OPPORTUNITIES', COUNT(*) FROM OPPORTUNITIES
                UNION ALL
                SELECT 'CONTRACTS', COUNT(*) FROM CONTRACTS
                UNION ALL
                SELECT 'ORDERS', COUNT(*) FROM ORDERS
                UNION ALL
                SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
                UNION ALL
                SELECT 'INVOICES', COUNT(*) FROM INVOICES
                UNION ALL
                SELECT 'ACME_BILLING_DATA', COUNT(*) FROM ACME_BILLING_DATA
                UNION ALL
                SELECT 'PARENT_CHILD_MAPPING', COUNT(*) FROM PARENT_CHILD_MAPPING
                UNION ALL
                SELECT 'TENANT_SFDC_MAPPING', COUNT(*) FROM TENANT_SFDC_MAPPING
                UNION ALL
                SELECT 'STG_PARSED_DOCUMENTS', COUNT(*) FROM STG_PARSED_DOCUMENTS
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
    
    def generate_products(self) -> pd.DataFrame:
        """Generate product catalog"""
        logger.info(f"Generating {self.num_products} products...")
        
        # Base product names for ACME Platform
        base_products = [
            'Professional Office User', 'Professional Mobile User', 'Enterprise Plus Office User',
            'Team Plus Office User', 'Managed Services', 'Marketing Pro - Contacts',
            'Dispatch Pro', 'Project Tracking', 'Sales Pro', 'Pricebook Pro',
            'ACME Phones Basic Seat', 'ACME Phones Advanced Seat',
            'Fleet Pro Track', 'Fleet Pro View', 'Payroll Pro', 'Contact Center Pro - Hub'
        ]
        
        products = []
        for i in range(self.num_products):
            product_id = f"PROD_{str(i+1).zfill(3)}"
            
            # Use base products and add variations
            if i < len(base_products):
                product_name = base_products[i]
            else:
                base_name = random.choice(base_products)
                product_name = f"{base_name} - Premium"
            
            product_family = self._weighted_choice(self.product_families)
            
            # Product categories for financial analysis
            if 'Office User' in product_name or 'Mobile User' in product_name:
                category = 'Core Platform'
                acme_product_code = random.choice([1, 2, 4, 8, 256, 512])
            elif 'Managed Services' in product_name:
                category = 'Core Platform' 
                acme_product_code = 2097152
            elif 'Marketing' in product_name:
                category = 'Add-on Modules'
                acme_product_code = 1295
            elif any(x in product_name for x in ['Dispatch', 'Project', 'Sales']):
                category = 'Add-on Modules'
                acme_product_code = random.choice([1297, 1338, 1360])
            else:
                category = 'Premium Features'
                acme_product_code = random.choice(list(self.acme_product_skus.keys()))
            
            product = {
                'id': product_id,
                'name': product_name,
                'product_code': f"PC{str(i+1).zfill(3)}",
                'product_category_c': category,
                'acme_product_code_c': acme_product_code,
                'family': product_family,
                'is_deleted': False,
                'is_active': True,
                'created_date': datetime.now() - timedelta(days=random.randint(100, 1000)),
                'unit_price': round(random.uniform(25, 500), 2)
            }
            
            products.append(product)
        
        return pd.DataFrame(products)
    
    def generate_accounts(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Generate extended SFDC account data from existing customers"""
        logger.info("Generating SFDC account data...")
        
        accounts = []
        
        for _, customer in customers_df.iterrows():
            # Create primary account
            account_id = f"ACC_{customer['customer_id'].split('_')[1]}"
            tenant_id = random.randint(1000, 9999)
            
            account = {
                'id': account_id,
                'tenant_id_c': tenant_id,
                'tenant_name_c': customer['company_name'],
                'name': customer['company_name'],
                'parent_id': None,  # Will be set for child accounts
                'customer_status_picklist_c': 'Active',
                'billing_enabled_c': random.choice(['Salesforce', 'Schedule Engine', None]),
                'billing_comparison_status_c': 'Validated',
                'data_validated_c': True,
                'test_account_c': False,
                'product_billed_in_sf_c': random.choice([True, False]),
                'is_deleted': False,
                'created_date': customer['signup_date'],
                'industry': customer['industry']
            }
            
            accounts.append(account)
        
        return pd.DataFrame(accounts)
    
    def generate_opportunities(self, accounts_df: pd.DataFrame) -> pd.DataFrame:
        """Generate sales opportunities"""
        logger.info(f"Generating {self.num_opportunities} opportunities...")
        
        opportunities = []
        stage_weights = {'Closed Won': 0.6, 'Closed Lost': 0.2, 'Proposal': 0.1, 'Negotiation': 0.1}
        
        for i in range(self.num_opportunities):
            opp_id = f"OPP_{str(i+1).zfill(5)}"
            account = accounts_df.sample(1).iloc[0]
            
            stage = self._weighted_choice(stage_weights)
            amount = round(random.uniform(5000, 50000), 2)
            
            # Create date within last 2 years
            created_date = datetime.now().date() - timedelta(days=random.randint(30, 730))
            close_date = created_date + timedelta(days=random.randint(30, 180))
            
            opportunity = {
                'id': opp_id,
                'account_id': account['id'],
                'name': f"{account['name']} - Service Contract {i+1}",
                'stage_name': stage,
                'amount': amount,
                'close_date': close_date,
                'created_date': created_date,
                'is_won': stage == 'Closed Won',
                'is_closed': stage in ['Closed Won', 'Closed Lost'],
                'probability': 100 if stage == 'Closed Won' else 0 if stage == 'Closed Lost' else random.randint(25, 75)
            }
            
            opportunities.append(opportunity)
        
        return pd.DataFrame(opportunities)
    
    def generate_contracts_and_orders(self, opportunities_df: pd.DataFrame, 
                                    accounts_df: pd.DataFrame, 
                                    products_df: pd.DataFrame) -> tuple:
        """Generate contracts, orders, and order items"""
        logger.info("Generating contracts, orders, and order items...")
        
        # Filter to won opportunities
        won_opps = opportunities_df[opportunities_df['is_won']]
        
        contracts = []
        orders = []
        order_items = []
        
        contract_counter = 1
        order_counter = 1
        order_item_counter = 1
        
        for _, opp in won_opps.iterrows():
            # Create contract
            contract_id = f"CONTRACT_{str(contract_counter).zfill(5)}"
            contract_status = self._weighted_choice(self.contract_statuses)
            
            # Contract dates
            contract_start = opp['close_date']
            contract_end = contract_start + timedelta(days=365)  # 1 year contracts
            
            contract = {
                'id': contract_id,
                'account_id': opp['account_id'],
                'opportunity_id': opp['id'],
                'status': contract_status,
                'start_date': contract_start,
                'end_date': contract_end,
                'term': 12,  # months
                'created_date': opp['close_date']
            }
            contracts.append(contract)
            
            # Create 1-3 orders per contract
            num_orders = random.randint(1, 3)
            
            for order_num in range(num_orders):
                order_id = f"ORDER_{str(order_counter).zfill(5)}"
                order_status = self._weighted_choice(self.order_statuses) if contract_status == 'Activated' else contract_status
                
                order_type = 'New' if order_num == 0 else random.choice(['Amendment', 'Renewal', 'Upsell'])
                
                order = {
                    'id': order_id,
                    'contract_id': contract_id,
                    'account_id': opp['account_id'],
                    'opportunity_id': opp['id'],
                    'status': order_status,
                    'type': order_type,
                    'order_number': f"ORD-{order_counter:05d}",
                    'created_date': contract_start + timedelta(days=order_num * 30),
                    'activated_date': contract_start + timedelta(days=order_num * 30 + 1),
                    'master_order_c': order_id if order_num == 0 else f"ORDER_{str(order_counter - order_num).zfill(5)}",
                    'is_master_order_c': order_num == 0,
                    'has_child_orders': num_orders > 1 and order_num == 0,
                    'is_migrated_c': False
                }
                orders.append(order)
                
                # Create order items (products on this order)
                num_items = random.randint(1, self.avg_order_items_per_contract)
                
                for item_num in range(num_items):
                    product = products_df.sample(1).iloc[0]
                    order_item_id = f"ORDER_ITEM_{str(order_item_counter).zfill(5)}"
                    
                    # Quantities and pricing
                    quantity = random.randint(1, 10)
                    unit_price = product['unit_price'] * random.uniform(0.8, 1.2)  # Some price variation
                    
                    # Commitment calculation - core products have minimums
                    if 'User' in product['name'] or 'Managed Services' in product['name']:
                        min_committed_quantity = quantity
                    else:
                        min_committed_quantity = max(1, int(quantity * 0.8))  # 80% commitment for add-ons
                    
                    # Exit ramp logic (10% of items are exit ramps)
                    is_exit_ramp = random.random() < 0.1
                    
                    order_item = {
                        'id': order_item_id,
                        'order_id': order_id,
                        'contract_id': contract_id,
                        'product_id': product['id'],
                        'product_code': product['product_code'],
                        'quantity': quantity,
                        'unit_price': round(unit_price, 2),
                        'total_price': round(quantity * unit_price, 2),
                        'min_committed_quantity': min_committed_quantity,
                        'total_min_commitment': round(min_committed_quantity * unit_price, 2),
                        'start_date': order['created_date'],
                        'end_date': contract_end,
                        'billing_day_of_month': random.randint(1, 28),
                        'created_date': order['created_date'],
                        'is_exit_ramp': is_exit_ramp,
                        'exit_ramp_c': is_exit_ramp,
                        'product_family': product['family']
                    }
                    order_items.append(order_item)
                    order_item_counter += 1
                
                order_counter += 1
            
            contract_counter += 1
        
        return pd.DataFrame(contracts), pd.DataFrame(orders), pd.DataFrame(order_items)
    
    def generate_sfdc_invoices(self, order_items_df: pd.DataFrame, accounts_df: pd.DataFrame,
                           products_df: pd.DataFrame, contracts_df: pd.DataFrame) -> pd.DataFrame:
        """Generate SFDC billing invoices and invoice lines linked to contracts"""
        logger.info("Generating SFDC invoices with proper contract linkage...")
        
        invoices = []
        invoice_lines = []
        invoice_counter = 1
        line_counter = 1
        
        # Create a mapping of order_id to contract_id for proper linking
        order_to_contract = {}
        for _, contract in contracts_df.iterrows():
            for _, order in order_items_df.iterrows():
                if order['order_id'].startswith('ORDER_') and contract['id'].startswith('CONTRACT_'):
                    # Link orders to contracts based on account_id
                    if hasattr(order, 'account_id') or 'account_id' in order:
                        order_account = order.get('account_id', None)
                        contract_account = contract.get('account_id', None)
                        if order_account == contract_account:
                            order_to_contract[order['order_id']] = contract['id']
                            break
        
        # Generate invoices for order items with contract linkage
        for _, order_item in order_items_df.iterrows():
            # Generate monthly invoices for active recurring items
            if order_item['product_family'] == 'Recurring Revenue':
                contract_id = order_to_contract.get(order_item['order_id'])
                if not contract_id:
                    # If no contract link, skip or create a default contract reference
                    continue
                    
                start_month = order_item['start_date']
                end_month = min(order_item['end_date'], datetime.now().date())
                
                current_month = start_month.replace(day=1)
                while current_month <= end_month.replace(day=1):
                    invoice_id = f"SF_INV_{str(invoice_counter).zfill(5)}"
                    
                    # Calculate invoice amounts with variance (80-120% of expected)
                    base_amount = order_item['unit_price'] * order_item['quantity']
                    variance_factor = random.uniform(0.75, 1.3)  # More realistic variance for better patterns
                    subtotal = base_amount * variance_factor
                    
                    tax_rate = 0.08  # 8% tax
                    tax_amount = subtotal * tax_rate
                    total_amount = subtotal + tax_amount
                    
                    # Invoice status
                    invoice_status = random.choice(['Posted', 'Draft']) if current_month <= datetime.now().date().replace(day=1) else 'Draft'
                    payment_status = 'Paid' if invoice_status == 'Posted' and random.random() < 0.9 else 'Unpaid'
                    
                    invoice = {
                        'id': invoice_id,
                        'blng_account_c': order_item['order_id'],  # Keep order link
                        'contract_id': contract_id,  # ADD CONTRACT LINK
                        'blng_invoice_date_c': current_month,
                        'blng_total_amount_c': round(total_amount, 2),
                        'blng_tax_amount_c': round(tax_amount, 2),
                        'blng_invoice_status_c': invoice_status,
                        'blng_payment_status_c': payment_status,
                        'invoice_long_description_c': f"Monthly billing for {current_month.strftime('%B %Y')} - Contract: {contract_id}",
                        'is_deleted': False
                    }
                    invoices.append(invoice)
                    
                    # Create invoice line
                    line_id = f"SF_INV_LINE_{str(line_counter).zfill(5)}"
                    invoice_line = {
                        'id': line_id,
                        'blng_invoice_c': invoice_id,
                        'contract_id': contract_id,  # ADD CONTRACT LINK TO LINE
                        'blng_product_c': order_item['product_id'],
                        'blng_unit_price_c': order_item['unit_price'],
                        'blng_quantity_c': order_item['quantity'],
                        'blng_subtotal_c': subtotal,
                        'blng_start_date_c': current_month,
                        'blng_end_date_c': current_month.replace(day=28),  # End of month
                        'blng_tax_amount_c': round(tax_amount, 2),
                        'is_deleted': False
                    }
                    invoice_lines.append(invoice_line)
                    
                    line_counter += 1
                    invoice_counter += 1
                    current_month = (current_month + timedelta(days=32)).replace(day=1)
        
        # Combine invoices and lines into a single structure for simplicity
        # In reality, these would be separate tables
        combined_invoices = []
        for invoice in invoices:
            matching_lines = [line for line in invoice_lines if line['blng_invoice_c'] == invoice['id']]
            for line in matching_lines:
                combined_invoice = {**invoice, **line}
                combined_invoices.append(combined_invoice)
        
        return pd.DataFrame(combined_invoices) if combined_invoices else pd.DataFrame()
    
    def generate_acme_billing_data(self, accounts_df: pd.DataFrame, contracts_df: pd.DataFrame) -> pd.DataFrame:
        """Generate ACME Platform billing data linked to contracts"""
        logger.info("Generating ACME Platform billing data with contract linkage...")
        
        acme_invoices = []
        invoice_counter = 1
        
        # Create account to contract mapping for linkage
        account_contracts = {}
        for _, contract in contracts_df.iterrows():
            account_id = contract['account_id']
            if account_id not in account_contracts:
                account_contracts[account_id] = []
            account_contracts[account_id].append(contract['id'])
        
        # Generate monthly billing ONLY for accounts that have contracts
        accounts_with_contracts = set(contracts_df['account_id'].unique())
        logger.info(f"Found {len(accounts_with_contracts)} accounts with contracts out of {len(accounts_df)} total accounts")
        
        for _, account in accounts_df.iterrows():
            account_id = account['id']
            
            # ONLY generate billing for accounts that have contracts
            if account_id not in accounts_with_contracts:
                continue
                
            if account['billing_enabled_c'] == 'Schedule Engine' or random.random() < 0.7:  # Higher probability for accounts with contracts
                tenant_id = account['tenant_id_c']
                
                # Get contracts for this account (guaranteed to exist)
                contracts_for_account = account_contracts.get(account_id, [])
                primary_contract = contracts_for_account[0] if contracts_for_account else None
                
                # Generate 6 months of billing history
                for month_offset in range(6):
                    trans_date = datetime.now().date().replace(day=1) - timedelta(days=30 * month_offset)
                    
                    # Generate invoice for random ACME Platform products
                    selected_skus = random.sample(list(self.acme_product_skus.keys()), random.randint(1, 3))
                    
                    for sku in selected_skus:
                        invoice_id = f"ACME_INV_{str(invoice_counter).zfill(5)}"
                        
                        quantity = random.randint(1, 10)
                        base_item_price = round(random.uniform(25, 200), 2)
                        # Add realistic variance (75-130%) for more business-like patterns
                        variance_factor = random.uniform(0.75, 1.3)
                        item_price = round(base_item_price * variance_factor, 2)
                        amount = quantity * item_price
                        tax = round(amount * 0.08, 2)
                        
                        acme_invoice = {
                            '_tenant_id': tenant_id,
                            '_tenant_name': account['tenant_name_c'],
                            'account_id': account_id,  # ADD ACCOUNT LINK
                            'contract_id': primary_contract,  # ADD CONTRACT LINK
                            'id': invoice_id,
                            'trans_date': trans_date,
                            'description': f"Monthly billing - {self.acme_product_skus[sku]}" + (f" - Contract: {primary_contract}" if primary_contract else ""),
                            'amount': amount,
                            'tax': tax,
                            'type': 0,  # Regular invoice
                            'balancetype': 0,  # Standard balance
                            'active': True,
                            'isexported': True,
                            # Invoice item details
                            'invoice_id': invoice_id,
                            'sku': sku,
                            'itemprice': item_price,
                            'quantity': quantity
                        }
                        acme_invoices.append(acme_invoice)
                        invoice_counter += 1
        
        return pd.DataFrame(acme_invoices)
    
    def generate_mapping_tables(self, accounts_df: pd.DataFrame, 
                              tenant_hierarchy_df: pd.DataFrame) -> tuple:
        """Generate parent-child mapping and tenant-SFDC ID mapping tables"""
        logger.info("Generating mapping tables...")
        
        # FPA Parent-Child Mapping
        parent_child_mapping = []
        snapshot_date = datetime.now().date()
        
        for _, child in tenant_hierarchy_df.iterrows():
            mapping = {
                'snapshot_date': snapshot_date,
                'tenant_account_id': child['child_account_id'],
                'parent_account_name_current': child['ndr_parent'],
                'parent_tenant_id_current': child['parent_account_id'],
                'parent_child_flag': 'Child',
                'fpa_parent_id': child['parent_account_id']
            }
            parent_child_mapping.append(mapping)
        
        # Add parent records
        parent_accounts = tenant_hierarchy_df['parent_account_id'].unique()
        for parent_id in parent_accounts:
            mapping = {
                'snapshot_date': snapshot_date,
                'tenant_account_id': parent_id,
                'parent_account_name_current': parent_id,
                'parent_tenant_id_current': parent_id,
                'parent_child_flag': 'Parent',
                'fpa_parent_id': parent_id
            }
            parent_child_mapping.append(mapping)
        
        # Tenant ID to SFDC ID Mapping
        tenant_sfdc_mapping = []
        for _, account in accounts_df.iterrows():
            mapping = {
                'tenant_id': account['tenant_id_c'],
                'sfdc_account_id': account['id'],
                'id_valid_from': account['created_date'],
                'id_valid_to': None  # Active mapping
            }
            tenant_sfdc_mapping.append(mapping)
        
        return pd.DataFrame(parent_child_mapping), pd.DataFrame(tenant_sfdc_mapping)
    
    def generate_documents(self) -> pd.DataFrame:
        """Generate document content including ACME Annual Report for Cortex Search"""
        import os
        
        documents_data = []
        
        # Include the ACME Annual Report
        annual_report_path = os.path.join(os.path.dirname(__file__), 'acme_annual_report.txt')
        try:
            with open(annual_report_path, 'r', encoding='utf-8') as f:
                annual_report_content = f.read()
                
            documents_data.append({
                'relative_path': 'acme_stg/acme_annual_report.txt',
                'file_url': f'@ACME_INTELLIGENCE.RAW.ACME_STG/acme_annual_report.txt',
                'title': 'ACME Services Annual Report 2024',
                'document_type': 'annual_report',
                'document_year': '2024',
                'content': annual_report_content,
                'parsed_at': datetime.now()
            })
            
            logger.info(f"✅ Loaded ACME Annual Report ({len(annual_report_content)} characters)")
            
        except FileNotFoundError:
            logger.warning(f"⚠️ ACME Annual Report not found at {annual_report_path}")
            # Create a minimal document entry anyway
            documents_data.append({
                'relative_path': 'acme_stg/acme_annual_report.txt',
                'file_url': f'@ACME_INTELLIGENCE.RAW.ACME_STG/acme_annual_report.txt',
                'title': 'ACME Services Annual Report 2024',
                'document_type': 'annual_report',
                'document_year': '2024',
                'content': 'ACME Services Annual Report 2024\n\nThis document provides comprehensive information about ACME Services performance, customer trust initiatives, and business intelligence insights for the field service management industry.',
                'parsed_at': datetime.now()
            })
        
        return pd.DataFrame(documents_data)
    
    def _create_financial_tables(self, conn):
        """Create financial data tables in Snowflake"""
        logger.info("Creating financial data tables...")
        
        # Product Catalog
        conn.execute("""
            CREATE TABLE IF NOT EXISTS PRODUCTS (
                id STRING PRIMARY KEY,
                name STRING NOT NULL,
                product_code STRING,
                product_category_c STRING,
                acme_product_code_c NUMBER,
                family STRING,
                is_deleted BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_date TIMESTAMP,
                unit_price NUMBER(10,2)
            ) COMMENT = 'Product catalog'
        """)
        
        # SFDC Accounts (extended)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ACCOUNTS (
                id STRING PRIMARY KEY,
                tenant_id_c NUMBER,
                tenant_name_c STRING,
                name STRING NOT NULL,
                parent_id STRING,
                customer_status_picklist_c STRING,
                billing_enabled_c STRING,
                billing_comparison_status_c STRING,
                data_validated_c BOOLEAN,
                test_account_c BOOLEAN,
                product_billed_in_sf_c BOOLEAN,
                is_deleted BOOLEAN DEFAULT FALSE,
                created_date DATE,
                industry STRING
            ) COMMENT = 'Extended SFDC account data'
        """)
        
        # Opportunities
        conn.execute("""
            CREATE TABLE IF NOT EXISTS OPPORTUNITIES (
                id STRING PRIMARY KEY,
                account_id STRING NOT NULL,
                name STRING NOT NULL,
                stage_name STRING,
                amount NUMBER(12,2),
                close_date DATE,
                created_date DATE,
                is_won BOOLEAN,
                is_closed BOOLEAN,
                probability NUMBER(3,0)
            ) COMMENT = 'Sales opportunities'
        """)
        
        # Contracts
        conn.execute("""
            CREATE TABLE IF NOT EXISTS CONTRACTS (
                id STRING PRIMARY KEY,
                account_id STRING NOT NULL,
                opportunity_id STRING,
                status STRING,
                start_date DATE,
                end_date DATE,
                term NUMBER,
                created_date DATE
            ) COMMENT = 'Sales contracts'
        """)
        
        # Orders  
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ORDERS (
                id STRING PRIMARY KEY,
                contract_id STRING NOT NULL,
                account_id STRING NOT NULL,
                opportunity_id STRING,
                status STRING,
                type STRING,
                order_number STRING,
                created_date DATE,
                activated_date DATE,
                master_order_c STRING,
                is_master_order_c BOOLEAN,
                has_child_orders BOOLEAN,
                is_migrated_c BOOLEAN
            ) COMMENT = 'Sales orders'
        """)
        
        # Order Items
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ORDER_ITEMS (
                id STRING PRIMARY KEY,
                order_id STRING NOT NULL,
                contract_id STRING NOT NULL,
                product_id STRING NOT NULL,
                product_code STRING,
                quantity NUMBER,
                unit_price NUMBER(10,2),
                total_price NUMBER(12,2),
                min_committed_quantity NUMBER,
                total_min_commitment NUMBER(12,2),
                start_date DATE,
                end_date DATE,
                billing_day_of_month NUMBER,
                created_date DATE,
                is_exit_ramp BOOLEAN,
                exit_ramp_c BOOLEAN,
                product_family STRING
            ) COMMENT = 'Order line items with commitment data'
        """)
        
        # SFDC Invoices (combined invoices and lines)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS INVOICES (
                id STRING,
                blng_account_c STRING,
                contract_id STRING,
                blng_invoice_date_c DATE,
                blng_total_amount_c NUMBER(12,2),
                blng_tax_amount_c NUMBER(12,2),
                blng_invoice_status_c STRING,
                blng_payment_status_c STRING,
                invoice_long_description_c TEXT,
                is_deleted BOOLEAN,
                blng_invoice_c STRING,
                blng_product_c STRING,
                blng_unit_price_c NUMBER(10,2),
                blng_quantity_c NUMBER,
                blng_subtotal_c NUMBER(12,2),
                blng_start_date_c DATE,
                blng_end_date_c DATE
            ) COMMENT = 'SFDC billing invoices with line items linked to contracts'
        """)
        
        # ACME Platform Billing Data
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ACME_BILLING_DATA (
                _tenant_id NUMBER,
                _tenant_name STRING,
                account_id STRING,
                contract_id STRING,
                id STRING,
                trans_date DATE,
                description STRING,
                amount NUMBER(12,2),
                tax NUMBER(12,2),
                type NUMBER,
                balancetype NUMBER,
                active BOOLEAN,
                isexported BOOLEAN,
                invoice_id STRING,
                sku NUMBER,
                itemprice NUMBER(10,2),
                quantity NUMBER
            ) COMMENT = 'ACME Platform billing data linked to contracts'
        """)
        
        # Parent Child Mapping
        conn.execute("""
            CREATE TABLE IF NOT EXISTS PARENT_CHILD_MAPPING (
                snapshot_date DATE,
                tenant_account_id STRING,
                parent_account_name_current STRING,
                parent_tenant_id_current STRING,
                parent_child_flag STRING,
                fpa_parent_id STRING
            ) COMMENT = 'Parent-child account mapping'
        """)
        
        # Tenant SFDC ID Mapping
        conn.execute("""
            CREATE TABLE IF NOT EXISTS TENANT_SFDC_MAPPING (
                tenant_id NUMBER,
                sfdc_account_id STRING,
                id_valid_from DATE,
                id_valid_to DATE
            ) COMMENT = 'Tenant ID to Salesforce Account ID mapping'
        """)
        
        logger.info("Financial tables created successfully")
    
    def _safe_clear_tables(self, conn, table_names: list):
        """Safely clear tables - only if they exist"""
        for table_name in table_names:
            try:
                # Check if table exists first
                check_sql = f"""
                SELECT COUNT(*) as table_exists 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = '{table_name}' 
                  AND TABLE_SCHEMA = 'RAW' 
                  AND TABLE_CATALOG = 'ACME_INTELLIGENCE'
                """
                
                # For now, just try to delete and ignore errors if table doesn't exist
                result = conn.execute(f"DELETE FROM {table_name}")
                if result:
                    logger.debug(f"Cleared existing data from {table_name}")
                    
            except Exception as e:
                # Table doesn't exist or other issue - that's fine, continue
                logger.debug(f"Skipping {table_name} (table may not exist): {str(e)[:100]}")
                continue
    
    def generate_all_data(self) -> Dict[str, pd.DataFrame]:
        """Generate all sample data for the ACME Intelligence demo"""
        logger.info("Starting ACME Intelligence demo data generation...")
        
        # Generate operational data (existing)
        customers_df = self.generate_customers()
        technicians_df = self.generate_technicians(customers_df)
        jobs_df = self.generate_jobs(customers_df, technicians_df)
        reviews_df = self.generate_reviews(jobs_df, customers_df, technicians_df)
        
        # Generate financial data (NDR + Contracts)
        tenant_hierarchy_df = self.generate_tenant_hierarchy()
        customer_segments_df = self.generate_customer_segments(tenant_hierarchy_df)
        billing_metrics_df = self.generate_billing_metrics(tenant_hierarchy_df, customer_segments_df)
        
        # Generate contract and invoice data (new)
        sf_products_df = self.generate_products()
        sf_accounts_df = self.generate_accounts(customers_df)
        opportunities_df = self.generate_opportunities(sf_accounts_df)
        contracts_df, orders_df, order_items_df = self.generate_contracts_and_orders(
            opportunities_df, sf_accounts_df, sf_products_df)
        sf_invoices_df = self.generate_sfdc_invoices(order_items_df, sf_accounts_df, sf_products_df, contracts_df)
        st_billing_df = self.generate_acme_billing_data(sf_accounts_df, contracts_df)
        parent_child_mapping_df, tenant_sfdc_mapping_df = self.generate_mapping_tables(
            sf_accounts_df, tenant_hierarchy_df)
        
        # Generate document content
        logger.info("Including ACME Annual Report document...")
        documents_df = self.generate_documents()
        
        # Store original dataframes for summary (before column name changes)
        orig_technicians_df = technicians_df.copy()
        
        # Load to Snowflake  
        self.load_data_to_snowflake(
            customers_df, technicians_df, jobs_df, reviews_df,
            tenant_hierarchy_df, customer_segments_df, billing_metrics_df,
            sf_products_df, sf_accounts_df, opportunities_df, contracts_df,
            orders_df, order_items_df, sf_invoices_df, st_billing_df,
            parent_child_mapping_df, tenant_sfdc_mapping_df, documents_df
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
        logger.info(f"Generated {len(sf_products_df)} products")
        logger.info(f"Generated {len(sf_accounts_df)} SFDC accounts")
        logger.info(f"Generated {len(opportunities_df)} sales opportunities")
        logger.info(f"Generated {len(contracts_df)} contracts")
        logger.info(f"Generated {len(orders_df)} orders")
        logger.info(f"Generated {len(order_items_df)} order items")
        logger.info(f"Generated {len(sf_invoices_df)} SFDC invoices")
        logger.info(f"Generated {len(st_billing_df)} ACME Platform billing records")
        logger.info(f"Generated {len(parent_child_mapping_df)} account mappings")
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
            'billing_metrics': billing_metrics_df,
            # New financial data
            'sf_products': sf_products_df,
            'sf_accounts': sf_accounts_df,
            'opportunities': opportunities_df,
            'contracts': contracts_df,
            'orders': orders_df,
            'order_items': order_items_df,
            'sf_invoices': sf_invoices_df,
            'st_billing': st_billing_df,
            'parent_child_mapping': parent_child_mapping_df,
            'tenant_sfdc_mapping': tenant_sfdc_mapping_df
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
