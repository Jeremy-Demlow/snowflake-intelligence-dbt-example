{{ config(materialized='table') }}

-- Simplified Financial Contracts and Invoices Fact Table
-- Basic version to get us started with the data

WITH

-- Contract data with basic metrics
cte_contracts AS (
    SELECT 
        c.id as contract_id,
        c.account_id,
        c.status as contract_status,
        c.start_date as contract_start_date,
        c.end_date as contract_end_date,
        
        oi.product_id,
        oi.min_committed_quantity,
        oi.total_min_commitment,
        oi.exit_ramp_c,
        
        p.name as product_name,
        p.family as product_family,
        
        a.tenant_id_c,
        a.tenant_name_c,
        a.name as account_name,
        a.customer_status_picklist_c as account_status
        
    FROM {{ ref('stg_contracts') }} c
    LEFT JOIN {{ ref('stg_orders') }} o ON c.id = o.contract_id
    LEFT JOIN {{ ref('stg_order_items') }} oi ON o.id = oi.order_id
    LEFT JOIN {{ ref('stg_products') }} p ON oi.product_id = p.id
    LEFT JOIN {{ ref('stg_accounts') }} a ON c.account_id = a.id
),

-- ACME platform billing data (simplified with contract linkage)
cte_billing AS (
    SELECT
        COALESCE(m.sfdc_account_id, ab._tenant_id::VARCHAR, ab.account_id) AS account_id,
        ab._tenant_id::VARCHAR AS tenant_id,
        ab._tenant_name AS tenant_name,
        ab.contract_id,  -- ADD CONTRACT_ID
        TO_CHAR(ab.trans_date, 'YYYY-MM') AS billing_month,
        ab.trans_date,
        ab.amount AS invoice_amount,
        ab.sku::VARCHAR AS product_id,
        ab.quantity AS billed_quantity,
        ab.active
    FROM {{ ref('stg_acme_billing_data') }} ab
    LEFT JOIN {{ ref('stg_tenant_sfdc_mapping') }} m ON ab._tenant_id::VARCHAR = m.tenant_id::VARCHAR
    WHERE ab.active = true AND ab.isexported = true
),

-- Aggregate billing data by contract for clean contract-level analysis
cte_billing_aggregated AS (
    SELECT
        contract_id,
        account_id,
        tenant_id,
        tenant_name,
        COUNT(*) as billing_record_count,
        SUM(invoice_amount) as total_invoice_amount,
        AVG(invoice_amount) as avg_monthly_invoice,
        SUM(billed_quantity) as total_billed_quantity,
        MIN(trans_date) as first_invoice_date,
        MAX(trans_date) as last_invoice_date,
        COUNT(DISTINCT billing_month) as months_billed
    FROM cte_billing
    WHERE contract_id IS NOT NULL
    GROUP BY contract_id, account_id, tenant_id, tenant_name
),

-- Handle billing without contracts separately
cte_billing_no_contract AS (
    SELECT
        account_id,
        tenant_id, 
        tenant_name,
        SUM(invoice_amount) as total_invoice_amount,
        COUNT(*) as billing_record_count
    FROM cte_billing
    WHERE contract_id IS NULL
    GROUP BY account_id, tenant_id, tenant_name
),

-- Combine contracts with aggregated billing data
cte_combined AS (
    -- Contracts with billing data
    SELECT 
        COALESCE(c.account_id, ba.account_id) AS account_id,
        COALESCE(c.tenant_id_c, ba.tenant_id) AS tenant_id,
        COALESCE(c.tenant_name_c, ba.tenant_name) AS tenant_name,
        c.account_name,
        c.account_status,
        
        -- Contract details
        c.contract_id,
        c.contract_status,
        c.contract_start_date,
        c.contract_end_date,
        
        -- Product details (take first product per contract)
        c.product_id,
        c.product_name,
        c.product_family,
        
        -- Financial metrics (aggregated at contract level)
        SUM(c.min_committed_quantity) as min_committed_quantity,
        SUM(c.total_min_commitment) as total_min_commitment,
        MAX(c.exit_ramp_c) as exit_ramp_c,  -- TRUE if any item is exit ramp
        
        -- Billing details (aggregated)
        ba.total_invoice_amount as invoice_amount,
        ba.total_billed_quantity as billed_quantity,
        ba.months_billed,
        ba.first_invoice_date as trans_date,
        
        -- Calculated metrics
        CASE 
            WHEN MAX(c.exit_ramp_c) = TRUE THEN 'Exit Ramp'
            WHEN c.contract_status = 'Activated' THEN 'Active'
            WHEN c.contract_status = 'Expired' THEN 'Expired'
            ELSE 'Other'
        END as contract_category,
        
        -- Variance calculation (contract-level)
        CASE 
            WHEN SUM(c.total_min_commitment) IS NOT NULL AND ba.total_invoice_amount IS NOT NULL 
            THEN ba.total_invoice_amount - SUM(c.total_min_commitment)
            ELSE NULL
        END as commitment_variance
        
    FROM cte_contracts c
    LEFT JOIN cte_billing_aggregated ba ON c.contract_id = ba.contract_id
    GROUP BY 
        c.contract_id, c.account_id, c.tenant_id_c, c.tenant_name_c, c.account_name, 
        c.account_status, c.contract_status, c.contract_start_date, c.contract_end_date,
        c.product_id, c.product_name, c.product_family,
        ba.account_id, ba.tenant_id, ba.tenant_name, ba.total_invoice_amount, 
        ba.total_billed_quantity, ba.months_billed, ba.first_invoice_date
    
    UNION ALL
    
    -- Billing without contracts (separate category)
    SELECT
        bn.account_id,
        bn.tenant_id,
        bn.tenant_name,
        'Unknown' as account_name,
        NULL as account_status,
        
        -- Contract details
        NULL as contract_id,
        NULL as contract_status, 
        NULL as contract_start_date,
        NULL as contract_end_date,
        
        -- Product details
        NULL as product_id,
        NULL as product_name,
        NULL as product_family,
        
        -- Financial metrics
        NULL as min_committed_quantity,
        NULL as total_min_commitment,
        FALSE as exit_ramp_c,
        
        -- Billing details
        bn.total_invoice_amount as invoice_amount,
        NULL as billed_quantity,
        NULL as months_billed,
        NULL as trans_date,
        
        'Other' as contract_category,
        NULL as commitment_variance
        
    FROM cte_billing_no_contract bn
)

-- Final output with business question metrics
SELECT 
    *,
    
    -- Business question flags for easy aggregation
    CASE 
        WHEN contract_status = 'Activated' 
        AND (contract_end_date IS NULL OR contract_end_date >= CURRENT_DATE()) 
        THEN 1 ELSE 0 
    END as is_active_contract,
    
    CASE 
        WHEN contract_status = 'Expired' 
        AND contract_end_date < CURRENT_DATE()
        THEN 1 ELSE 0 
    END as is_churned_contract,
    
    CASE 
        WHEN exit_ramp_c = TRUE
        THEN COALESCE(total_min_commitment, 0)
        ELSE 0
    END as exit_ramp_commitment_amount,
    
    -- Simple composite key
    MD5(CONCAT(
        COALESCE(account_id, ''), '-',
        COALESCE(contract_id, ''), '-',
        COALESCE(trans_date::VARCHAR, ''), '-',
        COALESCE(product_id, '')
    )) AS composite_key,
    
    CURRENT_TIMESTAMP() as last_updated
    
FROM cte_combined
