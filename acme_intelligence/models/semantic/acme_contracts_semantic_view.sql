{{
  config(
    materialized='semantic_view'
  )
}}

-- ACME Contracts Intelligence Semantic View
-- 
-- This file creates a comprehensive semantic view for ACME Contracts analytics,
-- combining contract commitments, invoice data, and churn analysis to enable 
-- natural language queries through Cortex Analyst.
--
-- To create/update the semantic view, run:
-- dbt run --select acme_contracts_semantic_view
--
-- The semantic view provides comprehensive analytics for:
-- - Active contract tracking and analysis
-- - Minimum commitment monitoring  
-- - Churn analysis and identification
-- - Commitment vs. invoice variance analysis
-- - Exit ramp risk assessment
--
-- This enables natural language queries through Cortex Analyst such as:
-- "What is the total number of active contracts for account XYZ?"
-- "What is the total minimum commitment for this month?"
-- "Show me all churned clients"
-- "What's the variance between commitments and invoiced amounts?"
-- "Which accounts have exit ramp commitments?"

TABLES (
    -- Core financial contracts and invoices fact table
    CONTRACTS_DATA AS {{ ref('fct_financial_contracts_invoices_simple') }}
      PRIMARY KEY (COMPOSITE_KEY)
      WITH SYNONYMS ('contracts_data', 'financial_data', 'contract_data', 'invoice_data', 'billing_data')
      COMMENT = 'Financial contracts and invoice data with commitments and actual billing amounts'
  )

  FACTS (
    -- Contract facts for cleaner metric expressions
    CONTRACTS_DATA.IS_ACTIVE_CONTRACT AS is_active_contract
      COMMENT = 'Active contract flag fact',
    CONTRACTS_DATA.TOTAL_MIN_COMMITMENT AS total_min_commitment
      COMMENT = 'Minimum commitment amount fact',
    CONTRACTS_DATA.IS_CHURNED_CONTRACT AS is_churned_contract
      COMMENT = 'Churned contract flag fact',
    CONTRACTS_DATA.COMMITMENT_VARIANCE AS commitment_variance
      COMMENT = 'Commitment vs invoice variance fact',
    CONTRACTS_DATA.INVOICE_AMOUNT AS invoice_amount
      COMMENT = 'Invoiced amount fact',
    CONTRACTS_DATA.EXIT_RAMP_COMMITMENT_AMOUNT AS exit_ramp_commitment_amount
      COMMENT = 'Exit ramp commitment amount fact',
    CONTRACTS_DATA.MIN_COMMITTED_QUANTITY AS min_committed_quantity
      COMMENT = 'Minimum committed quantity fact',
    CONTRACTS_DATA.BILLED_QUANTITY AS billed_quantity
      COMMENT = 'Actual billed quantity fact'
  )

  DIMENSIONS (
    -- Account and contract dimensions
    CONTRACTS_DATA.ACCOUNT_ID AS account_id
      WITH SYNONYMS ('account', 'customer_id', 'client_id')
      COMMENT = 'Unique account identifier',
      
    CONTRACTS_DATA.TENANT_ID AS tenant_id
      WITH SYNONYMS ('tenant')
      COMMENT = 'Tenant identifier',
      
    CONTRACTS_DATA.TENANT_NAME AS tenant_name
      WITH SYNONYMS ('tenant', 'client_name', 'customer')
      COMMENT = 'Tenant/client name',
      
    CONTRACTS_DATA.ACCOUNT_NAME AS account_name
      WITH SYNONYMS ('account', 'customer_name', 'client', 'company')
      COMMENT = 'Account/customer name',
      
    CONTRACTS_DATA.CONTRACT_ID AS contract_id
      WITH SYNONYMS ('contract')
      COMMENT = 'Unique contract identifier',
      
    CONTRACTS_DATA.CONTRACT_STATUS AS contract_status
      WITH SYNONYMS ('status', 'contract_state')
      COMMENT = 'Current contract status (Activated, Expired, etc.)',
      
    CONTRACTS_DATA.CONTRACT_CATEGORY AS contract_category
      WITH SYNONYMS ('category', 'contract_type')
      COMMENT = 'Contract category (Active, Exit Ramp, Expired, Other)',
      
    CONTRACTS_DATA.CONTRACT_START_DATE AS contract_start_date
      WITH SYNONYMS ('start_date', 'contract_start')
      COMMENT = 'Contract start date',
      
    CONTRACTS_DATA.CONTRACT_END_DATE AS contract_end_date
      WITH SYNONYMS ('end_date', 'contract_end', 'expiry_date')
      COMMENT = 'Contract end date',
    
    -- Product dimensions
    CONTRACTS_DATA.PRODUCT_ID AS product_id
      WITH SYNONYMS ('product')
      COMMENT = 'Product identifier',
      
    CONTRACTS_DATA.PRODUCT_NAME AS product_name
      WITH SYNONYMS ('product', 'service')
      COMMENT = 'Product or service name',
      
    CONTRACTS_DATA.PRODUCT_FAMILY AS product_family
      WITH SYNONYMS ('product_category', 'service_category')
      COMMENT = 'Product family/category',
    
    -- Time dimensions
    CONTRACTS_DATA.TRANS_DATE AS trans_date
      WITH SYNONYMS ('date', 'invoice_date', 'billing_date', 'transaction_date')
      COMMENT = 'Transaction/invoice date',
    
    -- Status dimensions
    CONTRACTS_DATA.ACCOUNT_STATUS AS account_status
      WITH SYNONYMS ('customer_status', 'status')
      COMMENT = 'Current account status',
      
    CONTRACTS_DATA.EXIT_RAMP_C AS exit_ramp_c
      WITH SYNONYMS ('exit_ramp', 'at_risk', 'exit_flag', 'exit_ramp_flag')
      COMMENT = 'Flag indicating if contract is marked for exit ramp'
  )

  METRICS (
    -- Question 1: Total number of active contracts for a given account(s)
    CONTRACTS_DATA.total_active_contracts AS SUM(CONTRACTS_DATA.is_active_contract)
      WITH SYNONYMS ('active_contracts', 'total_active', 'active_count')
      COMMENT = 'Total number of active contracts',
    
    -- Question 2: Total minimum commitment for a month for a given account(s)
    CONTRACTS_DATA.total_min_commitment_sum AS SUM(CONTRACTS_DATA.total_min_commitment)
      WITH SYNONYMS ('total_commitment', 'total_minimum', 'commitment_sum', 'min_commitment')
      COMMENT = 'Total minimum commitment amount across all contracts',
      
    -- Question 3: Total churned clients
    CONTRACTS_DATA.total_churned_clients AS SUM(CONTRACTS_DATA.is_churned_contract)
      WITH SYNONYMS ('churned_count', 'total_churned', 'churn_count', 'churned_clients')
      COMMENT = 'Total number of churned contracts/clients',
      
    -- Question 4: Min commitment vs invoiced amount for a given account(s)
    CONTRACTS_DATA.total_commitment_variance AS SUM(CONTRACTS_DATA.commitment_variance)
      WITH SYNONYMS ('total_variance', 'variance_sum', 'commitment_vs_invoice', 'billing_variance')
      COMMENT = 'Total variance between commitments and invoiced amounts',
      
    CONTRACTS_DATA.total_invoiced_amount AS SUM(CONTRACTS_DATA.invoice_amount)
      WITH SYNONYMS ('total_invoiced', 'total_billed', 'invoice_sum', 'invoiced_amount')
      COMMENT = 'Total invoiced/billed amount',
      
    -- Question 5: Exit ramp commitment for a given account(s)
    CONTRACTS_DATA.total_exit_ramp_commitment AS SUM(CONTRACTS_DATA.exit_ramp_commitment_amount)
      WITH SYNONYMS ('total_exit_ramp', 'at_risk_revenue', 'exit_ramp_sum', 'exit_commitment')
      COMMENT = 'Total commitment amount for exit ramp contracts (at-risk revenue)',
      
    -- Additional useful metrics
    CONTRACTS_DATA.contract_count AS COUNT(DISTINCT CONTRACTS_DATA.contract_id)
      WITH SYNONYMS ('total_contracts', 'contract_count')
      COMMENT = 'Total number of unique contracts',
      
    CONTRACTS_DATA.account_count AS COUNT(DISTINCT CONTRACTS_DATA.account_id)
      WITH SYNONYMS ('total_accounts', 'customer_count', 'client_count')
      COMMENT = 'Total number of unique accounts/customers',
      
    CONTRACTS_DATA.avg_commitment_per_contract AS AVG(CONTRACTS_DATA.total_min_commitment)
      WITH SYNONYMS ('average_commitment', 'avg_min_commitment')
      COMMENT = 'Average minimum commitment amount per contract',
      
    -- Performance metrics
    CONTRACTS_DATA.commitment_fulfillment_rate AS AVG(CASE WHEN CONTRACTS_DATA.total_min_commitment > 0 THEN (CONTRACTS_DATA.invoice_amount / CONTRACTS_DATA.total_min_commitment) * 100 END)
      WITH SYNONYMS ('fulfillment_rate', 'commitment_rate', 'billing_rate')
      COMMENT = 'Average commitment fulfillment rate percentage',
      
    CONTRACTS_DATA.over_committed_accounts AS COUNT(CASE WHEN CONTRACTS_DATA.commitment_variance > 0 THEN 1 END)
      WITH SYNONYMS ('over_committed', 'exceeded_commitment')
      COMMENT = 'Number of accounts that exceeded their minimum commitment',
      
    CONTRACTS_DATA.under_committed_accounts AS COUNT(CASE WHEN CONTRACTS_DATA.commitment_variance < 0 THEN 1 END)
      WITH SYNONYMS ('under_committed', 'missed_commitment')
      COMMENT = 'Number of accounts that fell short of their minimum commitment',
      
    -- Risk metrics
    CONTRACTS_DATA.exit_ramp_account_count AS COUNT(CASE WHEN CONTRACTS_DATA.exit_ramp_c = TRUE THEN 1 END)
      WITH SYNONYMS ('at_risk_accounts', 'exit_ramp_count')
      COMMENT = 'Number of accounts flagged for exit ramp',
      
    CONTRACTS_DATA.churn_rate AS (SUM(CONTRACTS_DATA.is_churned_contract) / COUNT(DISTINCT CONTRACTS_DATA.contract_id)) * 100
      WITH SYNONYMS ('churn_percentage', 'churn_rate')
      COMMENT = 'Churn rate as percentage of total contracts'
  )

  COMMENT = 'ACME Contracts Intelligence semantic view for analyzing contracts, commitments, invoices, and churn'
