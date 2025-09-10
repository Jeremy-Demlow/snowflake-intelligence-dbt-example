-- acme Intelligence Demo - Complete Infrastructure Setup
-- Creates database, schemas, tables, stages, role, and all components
-- This script sets up everything needed for the demo in a scalable way

USE ROLE ACCOUNTADMIN;

-- ========================================
-- 1. DATABASE AND SCHEMA SETUP
-- ========================================

-- Create database and core schemas
CREATE DATABASE IF NOT EXISTS ACME_INTELLIGENCE;
USE DATABASE ACME_INTELLIGENCE;

-- Core data schemas
CREATE SCHEMA IF NOT EXISTS RAW COMMENT = 'Raw data from source systems';
CREATE SCHEMA IF NOT EXISTS STAGING COMMENT = 'Cleaned and transformed staging data'; 
CREATE SCHEMA IF NOT EXISTS MARTS COMMENT = 'Business logic and fact/dimension tables';

-- Intelligence schemas (scalable for multiple use cases)
CREATE SCHEMA IF NOT EXISTS SEMANTIC_MODELS COMMENT = 'Semantic views for Cortex Analyst';
CREATE SCHEMA IF NOT EXISTS SEARCH COMMENT = 'Cortex Search services for document retrieval';




-- ========================================
-- 2. ROLE AND PERMISSIONS SETUP
-- ========================================

-- Create dedicated role for ACME Intelligence demo
CREATE OR REPLACE ROLE ACME_INTELLIGENCE_DEMO 
COMMENT = 'Role for ACME Intelligence demo with proper permissions';

-- Grant basic privileges
GRANT USAGE ON WAREHOUSE HOL_WAREHOUSE TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT USAGE ON DATABASE acme_INTELLIGENCE TO ROLE ACME_INTELLIGENCE_DEMO;

-- Grant schema privileges
GRANT USAGE ON SCHEMA ACME_INTELLIGENCE.RAW TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT USAGE ON SCHEMA ACME_INTELLIGENCE.STAGING TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT USAGE ON SCHEMA ACME_INTELLIGENCE.MARTS TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT USAGE ON SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT USAGE ON SCHEMA ACME_INTELLIGENCE.SEARCH TO ROLE ACME_INTELLIGENCE_DEMO;


-- Grant creation privileges for Intelligence components
GRANT CREATE SEMANTIC VIEW ON SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT CREATE CORTEX SEARCH SERVICE ON SCHEMA ACME_INTELLIGENCE.SEARCH TO ROLE ACME_INTELLIGENCE_DEMO;


-- Grant role to current user
SET current_user_name = CURRENT_USER();
GRANT ROLE ACME_INTELLIGENCE_DEMO TO USER IDENTIFIER($current_user_name);

-- ========================================
-- 3. STAGES AND FILE STORAGE
-- ========================================

USE SCHEMA RAW;

-- Create stage for documents with directory listing enabled
CREATE STAGE IF NOT EXISTS ACME_STG 
    FILE_FORMAT = (TYPE = 'CSV') 
    COMMENT = 'Stage for acme documents and files';

-- Enable directory listing for Cortex parsing
ALTER STAGE ACME_INTELLIGENCE.RAW.ACME_STG SET DIRECTORY = (ENABLE = TRUE);

-- ========================================
-- 4. RAW DATA TABLES
-- ========================================

CREATE OR REPLACE TABLE CUSTOMERS (
    customer_id STRING PRIMARY KEY,
    company_name STRING NOT NULL,
    industry STRING,
    company_size STRING,
    location_state STRING,
    location_city STRING,
    signup_date DATE,
    subscription_tier STRING,
    monthly_revenue DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) COMMENT = 'Customer master data';

CREATE OR REPLACE TABLE TECHNICIANS (
    technician_id STRING PRIMARY KEY,
    customer_id STRING NOT NULL,
    first_name STRING NOT NULL,
    last_name STRING NOT NULL,
    hire_date DATE,
    specialization STRING,
    certification_level STRING,
    years_experience INTEGER,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) COMMENT = 'Technician master data';

CREATE OR REPLACE TABLE JOBS (
    job_id STRING PRIMARY KEY,
    customer_id STRING NOT NULL,
    technician_id STRING NOT NULL,
    job_type STRING,
    job_status STRING,
    scheduled_date DATE,
    completed_date DATE,
    job_revenue DECIMAL(10,2),
    job_duration_hours DECIMAL(4,2),
    service_address STRING,
    job_description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) COMMENT = 'Job transaction data';

CREATE OR REPLACE TABLE REVIEWS (
    review_id STRING PRIMARY KEY,
    job_id STRING NOT NULL,
    customer_id STRING NOT NULL,
    technician_id STRING NOT NULL,
    rating INTEGER,
    review_text TEXT,
    review_source STRING,
    review_date DATE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
) COMMENT = 'Customer review and rating data';

-- Table for parsed documents (will be populated by dbt)
CREATE OR REPLACE TABLE STG_PARSED_DOCUMENTS (
    relative_path STRING,
    file_url STRING,
    title STRING,
    document_type STRING,
    document_year STRING,
    content TEXT,
    parsed_at TIMESTAMP
) COMMENT = 'Parsed document content for Cortex Search';

-- ========================================
-- NDR/FINANCIAL DATA TABLES
-- ========================================

-- Tenant hierarchy for parent-child account relationships
CREATE OR REPLACE TABLE TENANT_HIERARCHY (
    child_account_id STRING NOT NULL,
    parent_account_id STRING NOT NULL,
    child_tenant_id STRING,
    ndr_parent STRING NOT NULL,
    parent_start_date DATE
) COMMENT = 'Parent-child account relationships for NDR calculations';

-- Customer segmentation data
CREATE OR REPLACE TABLE CUSTOMER_SEGMENTS (
    parent_account_id STRING PRIMARY KEY,
    size_segment STRING NOT NULL,
    market_segment STRING NOT NULL,
    trade_segment STRING NOT NULL,
    product_category STRING NOT NULL
) COMMENT = 'Customer segmentation data for NDR analysis';

-- Monthly billing metrics for NDR calculations
CREATE OR REPLACE TABLE BILLING_METRICS (
    parent_account_id STRING NOT NULL,
    child_account_id STRING NOT NULL,
    ndr_parent STRING NOT NULL,
    month_id NUMBER NOT NULL,
    billing_month DATE NOT NULL,
    l3m_arr NUMBER(15,2) NOT NULL,
    size_segment STRING,
    market_segment STRING,
    trade_segment STRING,
    product_category STRING
) COMMENT = 'Monthly ARR data for NDR calculations';

-- ========================================
-- FINANCIAL CONTRACT & INVOICE TABLES (NEW)
-- ========================================

-- Product Catalog (50 ACME Platform products)
CREATE OR REPLACE TABLE PRODUCTS (
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
) COMMENT = 'ACME Platform product catalog for contract analysis';

-- Extended SFDC Accounts  
CREATE OR REPLACE TABLE ACCOUNTS (
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
) COMMENT = 'Extended SFDC account data for sales pipeline';

-- Sales Pipeline: Opportunities → Contracts → Orders → Order Items
CREATE OR REPLACE TABLE OPPORTUNITIES (
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
) COMMENT = 'Sales opportunities feeding contract pipeline';

CREATE OR REPLACE TABLE CONTRACTS (
    id STRING PRIMARY KEY,
    account_id STRING NOT NULL,
    opportunity_id STRING,
    status STRING,
    start_date DATE,
    end_date DATE,
    term NUMBER,
    created_date DATE
) COMMENT = 'Sales contracts - answers business question 1 (active contracts)';

CREATE OR REPLACE TABLE ORDERS (
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
) COMMENT = 'Sales orders with amendment/renewal tracking';

CREATE OR REPLACE TABLE ORDER_ITEMS (
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
) COMMENT = 'Order line items - answers business questions 2,4,5 (commitments, variance, exit ramps)';

-- Dual Billing Systems: SFDC + ACME Platform
CREATE OR REPLACE TABLE INVOICES (
    id STRING,
    blng_account_c STRING,
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
    blng_end_date_c DATE,
    contract_id STRING
) COMMENT = 'SFDC billing invoices for commitment vs invoiced analysis';

CREATE OR REPLACE TABLE ACME_BILLING_DATA (
    _tenant_id NUMBER,
    _tenant_name STRING,
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
    quantity NUMBER,
    account_id STRING,
    contract_id STRING
) COMMENT = 'ACME Platform billing data for dual billing analysis';

-- Account Mapping for Enterprise Relationships
CREATE OR REPLACE TABLE PARENT_CHILD_MAPPING (
    snapshot_date DATE,
    tenant_account_id STRING,
    parent_account_name_current STRING,
    parent_tenant_id_current STRING,
    parent_child_flag STRING,
    fpa_parent_id STRING
) COMMENT = 'Parent-child account mapping for enterprise churn analysis';

CREATE OR REPLACE TABLE TENANT_SFDC_MAPPING (
    tenant_id NUMBER,
    sfdc_account_id STRING,
    id_valid_from DATE,
    id_valid_to DATE
) COMMENT = 'Tenant ID to Salesforce Account ID mapping';

-- ========================================
-- 5. GRANT PERMISSIONS ON TABLES
-- ========================================

-- Grant table privileges to demo role
GRANT SELECT ON ALL TABLES IN SCHEMA ACME_INTELLIGENCE.RAW TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA ACME_INTELLIGENCE.RAW TO ROLE ACME_INTELLIGENCE_DEMO;

-- Grant stage privileges
GRANT READ ON STAGE ACME_INTELLIGENCE.RAW.ACME_STG TO ROLE ACME_INTELLIGENCE_DEMO;

-- Grant future privileges (for dbt-created objects)
GRANT SELECT ON ALL TABLES IN SCHEMA ACME_INTELLIGENCE.STAGING TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT SELECT ON ALL TABLES IN SCHEMA ACME_INTELLIGENCE.MARTS TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT SELECT ON ALL TABLES IN SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS TO ROLE ACME_INTELLIGENCE_DEMO;

-- Grant future privileges for dbt objects
GRANT SELECT ON FUTURE TABLES IN SCHEMA ACME_INTELLIGENCE.STAGING TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT SELECT ON FUTURE TABLES IN SCHEMA ACME_INTELLIGENCE.MARTS TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT SELECT ON FUTURE TABLES IN SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS TO ROLE ACME_INTELLIGENCE_DEMO;

-- ========================================
-- 6. INTELLIGENCE COMPONENT PERMISSIONS
-- ========================================

-- Grant permissions for semantic views (for Cortex Analyst access)
GRANT SELECT ON ALL SEMANTIC VIEWS IN SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT SELECT ON FUTURE SEMANTIC VIEWS IN SCHEMA ACME_INTELLIGENCE.SEMANTIC_MODELS TO ROLE ACME_INTELLIGENCE_DEMO;

-- Grant permissions for search services (for Cortex Search access)
GRANT USAGE ON ALL CORTEX SEARCH SERVICES IN SCHEMA ACME_INTELLIGENCE.SEARCH TO ROLE ACME_INTELLIGENCE_DEMO;
GRANT USAGE ON FUTURE CORTEX SEARCH SERVICES IN SCHEMA ACME_INTELLIGENCE.SEARCH TO ROLE ACME_INTELLIGENCE_DEMO;

-- Grant permissions for agents (for Intelligence Agent access)
-- Note: Individual agents will be granted permissions after creation
-- The following syntax is not supported in some Snowflake versions:
-- GRANT USAGE ON ALL AGENTS IN SCHEMA ACME_INTELLIGENCE.AGENTS TO ROLE ACME_INTELLIGENCE_DEMO;
-- GRANT USAGE ON FUTURE AGENTS IN SCHEMA ACME_INTELLIGENCE.AGENTS TO ROLE ACME_INTELLIGENCE_DEMO;

-- ========================================
-- 7. PUBLIC ACCESS (following best practices)
-- ========================================

-- Allow public access to see agents (following standard pattern)  
GRANT USAGE ON DATABASE acme_INTELLIGENCE TO ROLE PUBLIC;
GRANT USAGE ON DATABASE SNOWFLAKE_INTELLIGENCE TO ROLE PUBLIC;
GRANT USAGE ON SCHEMA SNOWFLAKE_INTELLIGENCE.AGENTS TO ROLE PUBLIC;

-- ========================================
-- 8. VERIFICATION
-- ========================================

SELECT '=== INFRASTRUCTURE SETUP COMPLETE ===' as status;

-- Show created schemas
SHOW SCHEMAS IN DATABASE acme_INTELLIGENCE;

-- Show created tables
SELECT 'RAW TABLES' as category, COUNT(*) as table_count 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_SCHEMA = 'RAW' AND TABLE_CATALOG = 'ACME_INTELLIGENCE'

UNION ALL

SELECT 'TOTAL SCHEMAS' as category, COUNT(*) as table_count
FROM INFORMATION_SCHEMA.SCHEMATA 
WHERE CATALOG_NAME = 'ACME_INTELLIGENCE';

-- Show role grants
SHOW GRANTS TO ROLE ACME_INTELLIGENCE_DEMO;

SELECT '=== READY FOR DATA LOADING AND DBT ===' as next_step;
