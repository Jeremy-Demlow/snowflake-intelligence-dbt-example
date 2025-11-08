# ACME Intelligence - Data Generation & Management

**Complete Business Intelligence Demo Data System**

This directory contains a sophisticated data generation system that creates **production-realistic demo data** for the ACME Intelligence platform, designed to showcase **modern business intelligence capabilities** and answer **critical business questions**.

---

## 📊 **Complete Data Architecture**

### **Operational Data (8 tables)**
- **CUSTOMERS** - 50 service companies across various industries
- **TECHNICIANS** - 25 field service technicians with specializations
- **JOBS** - 525 service jobs with revenue and performance data
- **REVIEWS** - 241 customer reviews with sentiment analysis
- **TENANT_HIERARCHY** - 35 parent-child relationships for NDR analysis
- **CUSTOMER_SEGMENTS** - 14 segmentation categories for analytics
- **BILLING_METRICS** - 1,260 monthly ARR records for NDR calculations
- **STG_PARSED_DOCUMENTS** - ACME Annual Report 2024 (4,464 characters) for Cortex Search

### **Financial Data (10 tables)**
- **PRODUCTS** - 50 ACME Platform products with pricing
- **ACCOUNTS** - 50 SFDC accounts with billing configurations
- **OPPORTUNITIES** - 100 sales opportunities in various stages
- **CONTRACTS** - 58 contracts (40 active, 16 churned)
- **ORDERS** - 99 orders with amendment/renewal tracking
- **ORDER_ITEMS** - 202 line items with commitment details
- **INVOICES** - 1,411 SFDC invoices for revenue recognition
- **ACME_BILLING_DATA** - 283 ACME Platform billing records
- **PARENT_CHILD_MAPPING** - 49 enterprise account mappings
- **TENANT_SFDC_MAPPING** - 50 tenant-to-Salesforce mappings

---

## 🚀 **Quick Start - Data Generation**

### **1. Full Data Generation**
```bash
cd data_setup
conda activate service_titan
python generate_acme_data.py
```

### **2. Verify Data Loading**
```bash
# Check all table counts
snow sql -q "
SELECT table_name, 
       (SELECT COUNT(*) FROM ACME_INTELLIGENCE.RAW.||table_name) as row_count
FROM INFORMATION_SCHEMA.TABLES 
WHERE table_schema = 'RAW' AND table_catalog = 'ACME_INTELLIGENCE'
ORDER BY table_name;
"
```

### **3. Test Business Questions**
```bash
# Test all 5 critical business questions
snow sql -q "
SELECT 'Active Contracts' as metric, COUNT(*) as value
FROM ACME_INTELLIGENCE.RAW.CONTRACTS WHERE status = 'Activated'
UNION ALL
SELECT 'Monthly Commitments', ROUND(SUM(total_min_commitment), 2)
FROM ACME_INTELLIGENCE.RAW.ORDER_ITEMS oi
JOIN ACME_INTELLIGENCE.RAW.CONTRACTS c ON oi.contract_id = c.id
WHERE c.status = 'Activated';
"
```

---

## 🔄 **Incremental Data Updates - Keep Your Demo Fresh!**

### **Quick Update (Recommended)**
```bash
cd data_setup
conda activate service_titan
./run_incremental_update.sh
```

This script automatically:
- ✅ Completes jobs that were scheduled but not finished
- ✅ Adds realistic customer reviews (60% review rate)
- ✅ Maintains demo narrative (underperforming technicians)
- ✅ Adds billing data for the current month
- ✅ Updates data through today's date

### **Manual Incremental Update**
```bash
cd data_setup
conda activate service_titan
python update_incremental_data.py
```

### **What Gets Updated?**

The incremental update system:
1. **Completes Scheduled Jobs** - Marks jobs as completed with realistic completion dates
2. **Generates Reviews** - Adds reviews for ~60% of completed jobs
3. **Maintains Narratives** - Ensures TECH_015 and TECH_023 keep poor ratings
4. **Adds Billing Data** - Generates monthly billing records for active contracts

### **When to Run Updates**

Run incremental updates:
- **Weekly**: Keep demo data current for presentations
- **After demos**: Add fresh data for the next demo
- **Monthly**: Ensure billing data stays current
- **Before dbt runs**: So transformed models have latest data

### **Verify Your Update**
```bash
# Check latest data dates
snow sql -c snowflake_intelligence -q "
SELECT 'Jobs' as metric, MAX(completed_date) as latest 
FROM ACME_INTELLIGENCE.RAW.JOBS WHERE job_status = 'Completed'
UNION ALL
SELECT 'Reviews', MAX(review_date) 
FROM ACME_INTELLIGENCE.RAW.REVIEWS
UNION ALL  
SELECT 'Billing', MAX(trans_date)
FROM ACME_INTELLIGENCE.RAW.ACME_BILLING_DATA;
"
```

**Expected Output (as of Oct 20, 2025):**
```
Jobs:    2025-10-18
Reviews: 2025-10-18
Billing: 2025-10-01
```

---

## 🛠 **How the Data Generation Works**

### **System Architecture**

The data generation system uses a **modern Python approach** with:
- **Snowpark** for direct DataFrame loading (no staging complexity)
- **Pandas** for realistic data generation with proper relationships
- **Faker** for realistic names, addresses, and business data
- **Smart algorithms** for creating realistic business scenarios

### **Key Components**

#### **1. `generate_acme_data.py` - Main Generator**
```python
class ACMEServicesDataGenerator:
    def __init__(self, num_customers=50, num_technicians=25, 
                 start_date='2024-01-01', end_date='2025-12-31'):
        # Initialize with configurable parameters
```

**Key Methods:**
- `generate_all_data()` - Full dataset generation
- `generate_customers()` - Customer companies with realistic industries
- `generate_financial_pipeline()` - Complete sales pipeline
- `generate_documents()` - **NEW!** Loads ACME Annual Report for Cortex Search
- `load_data_to_snowflake()` - Direct Snowpark loading

#### **2. `snowflake_connection.py` - Modern Connection**
```python
class SnowflakeConnection:
    def write_pandas(self, df, table_name, overwrite=True):
        # Direct DataFrame write using Snowpark (KISS principle)
        snowpark_df = self.session.create_dataframe(df)
        snowpark_df.write.save_as_table(table_name, mode="overwrite")
```

**Features:**
- **Snow CLI integration** for seamless authentication
- **Direct DataFrame writes** (no staging/COPY INTO complexity)
- **Automatic database/schema creation** with proper permissions
- **Clean error handling** and session management

---

## 🎨 **Customizing Data Generation**

### **Scaling Data Volume**

**Modify in `generate_acme_data.py`:**
```python
# Change these parameters for different data volumes
generator = ACMEServicesDataGenerator(
    num_customers=100,        # Double the customers
    num_technicians=50,       # Double the technicians  
    start_date='2023-01-01',  # Extend time range
    end_date='2025-12-31'
)
```

**Volume Impact:**
- **num_customers**: Affects CUSTOMERS, ACCOUNTS, OPPORTUNITIES, CONTRACTS
- **num_technicians**: Affects TECHNICIANS, JOBS, REVIEWS
- **date_range**: Affects JOBS, BILLING_METRICS, INVOICES temporal spread

### **Adding New Data Types**

**1. Add New Table Generation:**
```python
def generate_new_entity(self):
    """Generate new business entity data"""
    data = []
    for i in range(self.num_entities):
        data.append({
            'id': f'ENT_{i+1:03d}',
            'name': self.fake.company(),
            'created_date': self.fake.date_between(
                start_date=datetime.strptime(self.start_date, '%Y-%m-%d').date(),
                end_date=datetime.strptime(self.end_date, '%Y-%m-%d').date()
            )
        })
    return pd.DataFrame(data)
```

**2. Add to Generation Pipeline:**
```python
def generate_all_data(self):
    # ... existing generation ...
    
    # Add your new entity
    new_entities_df = self.generate_new_entity()
    success = conn.write_pandas(new_entities_df, 'NEW_ENTITIES')
```

**3. Update SQL Schema:**
```sql
-- Add to sql_scripts/setup_complete_infrastructure.sql
CREATE OR REPLACE TABLE NEW_ENTITIES (
    id STRING PRIMARY KEY,
    name STRING NOT NULL,
    created_date DATE
) COMMENT = 'Your new entity description';
```

### **Modifying Business Logic**

**Example: Change Contract Success Rates**
```python
def generate_contracts_and_orders(self, opportunities_df, accounts_df, products_df):
    # Current: ~58% of opportunities become contracts
    # Modify this logic to change success rates
    
    won_opportunities = opportunities_df[
        opportunities_df['is_won'] == True
    ].copy()
    
    # Change this percentage to adjust contract conversion
    contract_conversion_rate = 0.8  # 80% instead of ~58%
```

---

## 🔧 **Infrastructure Management**

### **Complete Database Reset**
```bash
# Drop everything and start fresh
snow sql -q "USE ROLE ACCOUNTADMIN; DROP DATABASE IF EXISTS ACME_INTELLIGENCE CASCADE;"

# Recreate infrastructure
snow sql -f sql_scripts/setup_complete_infrastructure.sql

# Regenerate all data
python generate_acme_data.py
```

### **Schema Management**
The system creates these schemas:
- **RAW** - Source system data (your generated data lives here)
- **STAGING** - Cleaned/transformed data (for dbt models)
- **MARTS** - Business logic layer (for dbt analytics)
- **SEMANTIC_MODELS** - Cortex Analyst semantic views
- **SEARCH** - Cortex Search services

### **Permissions**
All tables have proper permissions for the `ACME_INTELLIGENCE_DEMO` role with:
- **Full CRUD** on RAW schema
- **SELECT** access on all other schemas
- **Semantic view creation** permissions
- **Cortex Search** usage permissions

---

## 🎯 **Built-in Demo Narratives**

### **Underperforming Technicians**
The system automatically identifies underperforming technicians for compelling demos:
- **John Taylor (TECH_015)**
- **Christopher Martin (TECH_023)**

These technicians have **statistically lower performance** across multiple metrics for realistic coaching scenarios.

### **Financial Performance Patterns**
- **High-performing accounts** with consistent growth
- **At-risk accounts** with declining metrics
- **Exit ramp scenarios** with specific contract provisions
- **Revenue recognition** patterns across dual billing systems

---

## 📈 **Business Intelligence Capabilities**

### **NDR (Net Dollar Retention) Analysis**
```sql
-- Monthly NDR calculation using generated data
SELECT 
    billing_month,
    ndr_parent,
    SUM(l3m_arr) as total_arr,
    LAG(SUM(l3m_arr), 3) OVER (PARTITION BY ndr_parent ORDER BY billing_month) as l3m_arr_prior
FROM ACME_INTELLIGENCE.RAW.BILLING_METRICS 
GROUP BY billing_month, ndr_parent
ORDER BY billing_month DESC;
```

### **Contract Lifecycle Analytics**
```sql
-- Complete contract to revenue pipeline
SELECT 
    c.status,
    COUNT(*) as contract_count,
    SUM(oi.total_min_commitment) as total_commitments,
    AVG(oi.total_min_commitment) as avg_commitment
FROM ACME_INTELLIGENCE.RAW.CONTRACTS c
JOIN ACME_INTELLIGENCE.RAW.ORDER_ITEMS oi ON c.id = oi.contract_id
GROUP BY c.status
ORDER BY total_commitments DESC;
```

### **Technician Performance Analytics**
```sql
-- Technician performance with demo narrative
SELECT 
    CONCAT(t.first_name, ' ', t.last_name) as technician_name,
    COUNT(j.job_id) as total_jobs,
    AVG(j.job_revenue) as avg_revenue_per_job,
    AVG(r.rating) as avg_customer_rating,
    AVG(j.job_duration_hours) as avg_duration_hours
FROM ACME_INTELLIGENCE.RAW.TECHNICIANS t
JOIN ACME_INTELLIGENCE.RAW.JOBS j ON t.technician_id = j.technician_id  
LEFT JOIN ACME_INTELLIGENCE.RAW.REVIEWS r ON j.job_id = r.job_id
GROUP BY t.technician_id, t.first_name, t.last_name
ORDER BY avg_revenue_per_job DESC;
```

---

## 🔍 **Extending the System**

### **Adding Industry-Specific Data**
```python
# Add specialized industry data generation
def generate_industry_specific_data(self, industry_type):
    if industry_type == 'healthcare':
        return self.generate_healthcare_compliance_data()
    elif industry_type == 'manufacturing': 
        return self.generate_equipment_maintenance_data()
```

### **Integration with External Systems**
```python
# Add external data source integration
def integrate_external_data(self, source_config):
    """Import data from external systems"""
    if source_config['type'] == 'salesforce':
        return self.import_from_salesforce_api(source_config)
    elif source_config['type'] == 'csv':
        return self.import_from_csv_files(source_config)
```

### **Advanced Analytics Features**
```python
# Add machine learning features
def generate_predictive_features(self, base_data):
    """Generate features for ML models"""
    base_data['churn_risk_score'] = self.calculate_churn_risk(base_data)
    base_data['upsell_potential'] = self.calculate_upsell_potential(base_data)
    return base_data
```

---

## 🎉 **Success Metrics**

**After running the full data generation, you'll have:**

✅ **4,278+ data records** across 18 tables  
✅ **Complete business intelligence** answering 5 critical questions  
✅ **ACME Annual Report 2024** automatically loaded for Cortex Search  
✅ **Realistic demo narratives** with underperforming technicians  
✅ **Full contract lifecycle** from opportunity → revenue realization  
✅ **NDR analytics** with parent-child account relationships  
✅ **Dual billing systems** (SFDC + ACME Platform) integration  

**Ready for:**
- **dbt transformations** and analytics models
- **Semantic view creation** for Cortex Analyst  
- **Snowflake Agent** demonstrations
- **Business intelligence** presentations
- **Machine learning** model training
- **Advanced analytics** and reporting

---

## 🆘 **Troubleshooting**

### **Data Loading Issues**
```bash
# Check connection
python -c "from snowflake_connection import SnowflakeConnection; conn = SnowflakeConnection.from_snow_cli(); print('✅ Connection successful' if conn.test_connection() else '❌ Connection failed')"

# Verify permissions  
snow sql -q "SHOW GRANTS TO ROLE ACME_INTELLIGENCE_DEMO;"

# Check table existence
snow sql -q "SHOW TABLES IN SCHEMA ACME_INTELLIGENCE.RAW;"
```

### **Generation Failures**
```bash
# Check Python environment
conda list | grep -E "(pandas|snowflake|faker)"

# Check conda environment is activated
conda info --envs | grep service_titan
```

### **Business Question Validation**
```bash
# Quick validation of all 5 questions
snow sql -f ../validation_queries/business_questions.sql
```

---

**🎯 Your complete business intelligence demo system is ready!**

*This data generation system represents a production-quality approach to creating realistic, comprehensive demo data that supports advanced analytics, machine learning, and business intelligence use cases.*
