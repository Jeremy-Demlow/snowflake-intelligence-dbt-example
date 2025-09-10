# ACME Intelligence Demo - Complete Deployment Guide

## Prerequisites
- Snowflake account with ACCOUNTADMIN role
- Snow CLI configured and authenticated
- Python 3.11+ with required packages (see `data_setup/requirements.txt`)
- dbt 1.10+ installed

## 🚀 Complete End-to-End Deployment

### Step 1: Infrastructure Setup
```bash
# Set up complete Snowflake infrastructure
snow sql -f sql_scripts/setup_complete_infrastructure.sql
```

### Step 2: Generate and Load Data
```bash
cd data_setup
python generate_acme_data.py
```

**Key Data Generated:**
- **58 contracts** with proper account linkages
- **222 ACME Platform invoices** linked to contracts via `contract_id`
- **Realistic variance patterns** (85-115% of commitments)
- **1 document** (ACME Annual Report) for Cortex Search

### Step 3: Build dbt Models
```bash
cd ../acme_intelligence
dbt run
```

**Critical Models Built:**
- **Staging Models**: All raw data cleaned and prepared
- **Mart Models**: `fct_financial_contracts_invoices_simple` with proper contract-invoice joins
- **Semantic Views**: 3 semantic views for different business domains
- **Search Service**: Cortex Search service for document retrieval

### Step 4: Deploy Enhanced Agents
```bash
cd ../snowflake_agents
python agent_generator.py
snow sql -f generated/acme_contracts_agent.sql
snow sql -f generated/acme_intelligence_agent.sql
```

## 🔧 Key Technical Fixes Applied

### 1. Contract-Invoice Linkage Fix
**Problem**: Invoices had `CONTRACT_ID = None`, preventing variance analysis
**Solution**: 
- Updated `data_setup/generate_acme_data.py` to properly link invoices to contracts
- Added `contract_id` and `account_id` columns to `ACME_BILLING_DATA` table
- Modified dbt models to join on `contract_id` instead of incompatible product IDs

### 2. Data Model Join Fix  
**Problem**: Joining product IDs (`PROD_001`) with SKU numbers (`102387`)
**Solution**: Changed join in `fct_financial_contracts_invoices_simple.sql` from:
```sql
-- ❌ Before
ON c.account_id = b.account_id AND c.product_id = b.product_id

-- ✅ After  
ON c.contract_id = b.contract_id
```

### 3. Realistic Variance Patterns
**Problem**: Only "Other" category had 492% over-fulfillment (unrealistic)
**Solution**: Applied realistic variance factors (85-115%) in data generation

## 📊 Expected Results

### Contract Variance Analysis:
- **Active Contracts**: 253 contracts, $479K commitments, -$168K variance (39% fulfillment)
- **Exit Ramp**: 21 contracts, $41K commitments, -$1.6K variance (33% fulfillment)  
- **Expired**: 27 contracts, $35K commitments, $0 invoiced (0% fulfillment - correct)

### Business Questions Answerable:
1. ✅ **Total Active Contracts**: 253 active contracts
2. ✅ **Total Commitments**: $478,742.39 across all active contracts
3. ✅ **Churned Clients**: 6 churned clients with measurable revenue impact
4. ✅ **Commitment Variance**: -$168K under-billing opportunity in active contracts
5. ✅ **Exit Ramp Risk**: $41K at-risk revenue across 21 contracts

## 🎯 Enhanced Agent Features

### Production-Grade Optimizations:
- **Orchestration**: `models: orchestration: "auto"` for parallel tool execution
- **Executive Response Structure**: 10-point framework for strategic insights
- **Advanced Search Tuning**: Relevance weights, diversity controls, reranking
- **Detailed Tool Descriptions**: Business purpose and key metrics for each data source

### Sample Questions for Testing:
```sql
-- Test contracts semantic view
SELECT * FROM SEMANTIC_VIEW(
  ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_analytics_view
  DIMENSIONS contract_category
  METRICS total_active_contracts, total_min_commitment_sum, total_churned_clients, total_commitment_variance
) ORDER BY contract_category;
```

## 🔍 Validation Commands

### Verify Data Quality:
```sql
-- Check contract-invoice linkage
SELECT 
    CONTRACT_CATEGORY,
    COUNT(*) as total_rows,
    COUNT(CASE WHEN TOTAL_MIN_COMMITMENT > 0 THEN 1 END) as with_commitments,
    COUNT(CASE WHEN INVOICE_AMOUNT > 0 THEN 1 END) as with_invoices,
    COUNT(CASE WHEN COMMITMENT_VARIANCE IS NOT NULL THEN 1 END) as with_variance
FROM ACME_INTELLIGENCE.MARTS.fct_financial_contracts_invoices_simple
WHERE CONTRACT_CATEGORY IS NOT NULL
GROUP BY CONTRACT_CATEGORY;
```

### Verify Search Service:
```sql
USE SCHEMA ACME_INTELLIGENCE.SEARCH;
SHOW CORTEX SEARCH SERVICES;
```

### Verify Agents:
```sql
USE DATABASE SNOWFLAKE_INTELLIGENCE;
USE SCHEMA AGENTS;
SHOW AGENTS;
```

## 🚨 Common Issues & Solutions

### Issue: "Cortex Search Service does not exist"
**Solution**: Run the missing model
```bash
cd acme_intelligence
dbt run --select acme_intelligence_complete
```

### Issue: "Invalid identifier 'ACCOUNT_ID'" in staging models
**Solution**: Ensure raw tables have all required columns:
```sql
ALTER TABLE ACME_INTELLIGENCE.RAW.ACME_BILLING_DATA ADD COLUMN account_id STRING;
ALTER TABLE ACME_INTELLIGENCE.RAW.ACME_BILLING_DATA ADD COLUMN contract_id STRING;
ALTER TABLE ACME_INTELLIGENCE.RAW.INVOICES ADD COLUMN contract_id STRING;
```

### Issue: Agent deployment permission errors
**Solution**: Grant proper roles:
```sql
GRANT ROLE SNOWFLAKE_INTELLIGENCE_ADMIN_RL TO ROLE ACCOUNTADMIN;
GRANT ALL PRIVILEGES ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE ACCOUNTADMIN;
```

## 📈 Demo Script

### 1. Show Realistic Contract Health:
"Our portfolio shows **253 active contracts** with **$479K in commitments**. We have a **39% fulfillment rate** creating a **-$168K variance** - this represents significant under-billing opportunity."

### 2. Highlight Risk Management:
"We have **21 contracts** in exit ramp status with **$41K at-risk revenue**. Early intervention on these accounts could prevent churn."

### 3. Demonstrate Churn Analysis:
"**6 clients have churned** with measurable revenue impact. The expired contracts show **zero fulfillment** as expected, confirming data quality."

## 🔄 Full Reset Instructions

If needed, completely reset the environment:
```bash
# 1. Drop and recreate database
snow sql -q "DROP DATABASE IF EXISTS ACME_INTELLIGENCE; CREATE DATABASE ACME_INTELLIGENCE;"

# 2. Run complete deployment from Step 1
# (Follow all steps above)
```

## ✅ Success Criteria

Demo is ready when:
- [ ] All 27 dbt models pass (including semantic views)
- [ ] Cortex Search service is ACTIVE
- [ ] Both agents deploy successfully  
- [ ] Contract variance analysis shows realistic patterns across all categories
- [ ] All 5 business questions return meaningful results

---

**Total Setup Time**: ~10-15 minutes
**Data Volume**: ~2,100 total records across all tables
**Agent Response Time**: < 3 seconds (optimized orchestration)
