# 🚀 acme Intelligence - Complete Validation Guide

This guide provides a comprehensive approach to validating your acme Intelligence demo using **SNOWCLI** and **conda acme environment**.

## 🏃‍♂️ Quick Start (3 Steps)

### Step 1: Setup Validation
```bash
./test_setup.sh
```
Checks that all tools (SNOWCLI, conda, dbt) are properly installed and configured.

### Step 2: Quick Connectivity Test
```bash
python run_validation.py
```
Tests basic connectivity to Snowflake and validates environments.

### Step 3: Full End-to-End Validation
```bash
python validate_end_to_end.py
```
Comprehensive validation of the entire pipeline from infrastructure to intelligence.

## 📋 What Gets Validated

### Infrastructure (SNOWCLI)
- ✅ Snowflake database and schemas creation
- ✅ Tables, stages, and permissions setup
- ✅ Role-based access control validation

### Data Pipeline (conda acme)
- ✅ Sample data generation and loading
- ✅ Document upload to Snowflake stage
- ✅ dbt model transformations (staging → marts → semantic)

### Intelligence Components
- ✅ Semantic view creation and testing
- ✅ Cortex Search service deployment
- ✅ Snowflake Intelligence Agent deployment

### Data Quality
- ✅ Row count validation across all tables
- ✅ Data relationship integrity checks
- ✅ Model output verification

## 🛠️ Tool Usage

### SNOWCLI Commands Used
```bash
# Infrastructure setup
snow sql -f sql_scripts/setup_complete_infrastructure.sql

# Document upload
snow stage copy data_setup/acme_annual_report.txt @acme_INTELLIGENCE.RAW.acme_STG

# Agent deployment
snow sql -f snowflake_agents/acme_intelligence_agent_scalable.sql

# Solution validation  
snow sql -f sql_scripts/validate_dbt_solution.sql
```

### conda acme Commands Used  
```bash
# Data generation
conda run -n acme python data_setup/generate_acme_data.py

# dbt operations (SIMPLIFIED!)
conda run -n acme dbt deps
conda run -n acme dbt run  # Handles all 15 models automatically!
conda run -n acme dbt test
```

**Key Innovation:** No more staged dbt runs! Single `dbt run` command handles dependency resolution automatically.

## 🎯 Expected Results

When validation completes successfully, you should see:

### Infrastructure ✅
- Database: `ACME_INTELLIGENCE` 
- Schemas: `RAW`, `STAGING`, `MARTS`, `SEMANTIC_MODELS`, `SEARCH`
- Role: `ACME_INTELLIGENCE_DEMO` with proper permissions

### Data ✅  
- **Customers**: Sample service companies data
- **Technicians**: Field technician information
- **Jobs**: Service job transactions
- **Reviews**: Customer feedback and ratings
- **Documents**: Parsed annual report content

### dbt Models ✅
- **Staging**: Clean source data views
- **Marts**: Business logic and fact tables
- **Semantic**: Intelligence-ready data models

### Intelligence Components ✅
- **Semantic Views**: `acme_analytics_view` + `acme_financial_analytics_view` for Cortex Analyst
- **Search Service**: `acme_document_search` for document retrieval  
- **Agent**: `acme_intelligence_agent` (deployed in `SNOWFLAKE_INTELLIGENCE.AGENTS`)

## 🧪 Manual Testing

### Test Semantic View
```sql
SELECT * FROM SEMANTIC_VIEW(
    ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view
    METRICS technician_count, total_revenue_sum, avg_rating_avg
);
```

### Test Underperforming Technicians
```sql
SELECT * FROM SEMANTIC_VIEW(
    ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view
    DIMENSIONS technician_name, is_underperforming  
    FACTS avg_rating, revenue_2025
) WHERE is_underperforming = 1;
```

### Test Intelligence Agent
```sql
SHOW AGENTS IN SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS;
```

### Expected Results
- **Technicians**: 25 total
- **Total Revenue**: $195,768
- **2025 Revenue**: $82,132  
- **Underperforming**: 2 technicians (< 3 stars)

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. SNOWCLI Connection Issues
```bash
# Test connection
snow connection test

# Add new connection
snow connection add

# List connections
snow connection list
```

#### 2. conda Environment Issues
```bash
# Create environment
conda create -n acme python=3.9

# Install dbt
conda activate acme
pip install dbt-snowflake

# Test environment
conda run -n acme python --version
```

#### 3. dbt Connection Issues
```bash
cd acme_intelligence
conda run -n acme dbt debug
```
Check `~/.dbt/profiles.yml` for correct Snowflake connection details.

#### 4. Permission Issues
```sql
-- Grant additional permissions if needed
GRANT ROLE acme_INTELLIGENCE_DEMO TO USER <your_username>;
```

## 📁 File Structure

```
snowflake-intelligence-dbt-example/
├── 🔧 Validation Scripts
│   ├── test_setup.sh                    # Prerequisites check
│   ├── run_validation.py                # Quick connectivity tests  
│   ├── validate_end_to_end.py          # Full pipeline validation
│   └── deploy_acme_intelligence.py  # Complete deployment
│
├── 💾 SQL Scripts (SNOWCLI)
│   ├── setup_complete_infrastructure.sql
│   ├── validate_dbt_solution.sql
│   └── grant_user_access.sql
│
├── 🏗️ dbt Project (conda acme)
│   └── acme_intelligence/
│       ├── dbt_project.yml
│       └── models/
│           ├── staging/
│           ├── marts/
│           └── semantic/
│
├── 📊 Data Setup (conda acme)  
│   ├── generate_acme_data.py
│   └── acme_annual_report.txt
│
└── 🧠 Intelligence Components (SNOWCLI)
    └── snowflake_agents/
```

## ✅ Success Criteria

Your acme Intelligence demo is working correctly when:

1. **All validation scripts pass** without critical errors
2. **dbt models build successfully** in all layers (staging, marts, semantic)
3. **Semantic views return data** when queried with Cortex Analyst syntax
4. **Intelligence agents are deployed** and show up in `SHOW AGENTS`
5. **Data quality checks pass** with expected row counts and relationships

## 🚀 Next Steps

After successful validation:

1. **Demo the solution** using the semantic view queries
2. **Test the intelligence agent** with natural language questions
3. **Explore Cortex Search** functionality with the document corpus
4. **Scale the solution** by adding more data sources or use cases

## 📞 Support

If you encounter issues:
1. Check the validation output for specific error messages
2. Review the troubleshooting section above
3. Verify all prerequisites are installed correctly
4. Test individual components using the manual testing queries

---

🎉 **Happy validating!** The combination of SNOWCLI and conda acme environment provides a robust, scalable approach to building and validating Snowflake intelligence solutions.
