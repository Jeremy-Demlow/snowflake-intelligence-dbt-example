{{ config(materialized='table') }}

-- Financial Contracts and Invoices Fact Table
-- Adapts complex enterprise financial logic to ACME Intelligence data
-- Combines contract commitments with actual invoiced amounts

WITH

-- Parent-child account mapping
cte_parent_child_mapping AS (
    SELECT DISTINCT
        snapshot_date,
        tenant_account_id,
        parent_account_name_current,
        parent_tenant_id_current,
        parent_child_flag,
        fpa_parent_id
    FROM {{ ref('stg_parent_child_mapping') }}
    WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM {{ ref('stg_parent_child_mapping') }})
),

-- Contract base with account details
cte_contract_base AS (
    SELECT 
        c.id as contract_id,
        c.account_id,
        c.opportunity_id,
        c.status as contract_status,
        c.start_date as contract_start_date,
        c.end_date as contract_end_date,
        c.term as contract_term,
        
        o.id as order_id,
        o.type as order_type,
        o.status as order_status,
        o.order_number,
        o.master_order_c,
        o.is_master_order_c,
        o.has_child_orders,
        o.is_migrated_c,
        o.created_date as order_created_date,
        
        oi.id as order_item_id,
        oi.product_id,
        oi.product_code,
        oi.quantity,
        oi.unit_price,
        oi.total_price,
        oi.min_committed_quantity,
        oi.total_min_commitment,
        oi.start_date as order_item_start_date,
        oi.end_date as order_item_end_date,
        oi.billing_day_of_month,
        oi.exit_ramp_c,
        oi.product_family,
        
        p.name as product_name,
        p.product_category_c,
        p.family as sf_product_family,
        
        a.tenant_id_c,
        a.tenant_name_c,
        a.name as account_name,
        a.customer_status_picklist_c as account_status,
        a.billing_enabled_c,
        a.product_billed_in_sf_c
        
    FROM {{ ref('stg_contracts') }} c
    LEFT JOIN {{ ref('stg_orders') }} o ON c.id = o.contract_id
    LEFT JOIN {{ ref('stg_order_items') }} oi ON o.id = oi.order_id
    LEFT JOIN {{ ref('stg_products') }} p ON oi.product_id = p.id
    LEFT JOIN {{ ref('stg_accounts') }} a ON c.account_id = a.id
),

-- Salesforce invoice data
cte_sf_invoices AS (
    SELECT
        i.blng_account_c AS account_id,
        DATE_TRUNC('month', i.blng_invoice_date_c)::DATE AS billing_month,
        i.blng_invoice_date_c AS trans_date,
        i.blng_start_date_c AS start_date,
        i.blng_end_date_c AS end_date,
        i.blng_total_amount_c AS invoice_total_amount,
        i.blng_tax_amount_c AS invoice_tax_amount,
        i.id AS invoice_id,
        i.blng_product_c AS product_id,
        i.blng_unit_price_c AS unit_price,
        i.blng_quantity_c AS gross_invoiced_quantity,
        i.blng_subtotal_c AS gross_invoiced_amount,
        i.blng_invoice_status_c AS payment_status,
        'Salesforce' as invoice_source
    FROM {{ ref('stg_invoices') }} i
    WHERE i.blng_invoice_status_c = 'Posted'
),

-- ACME platform billing data
cte_acme_invoices AS (
    SELECT
        COALESCE(m.sfdc_account_id, ab._tenant_id::VARCHAR) AS account_id,
        DATE_TRUNC('month', ab.trans_date)::DATE AS billing_month,
        ab.trans_date,
        NULL AS start_date,
        NULL AS end_date,
        ab.amount AS invoice_total_amount,
        ab.tax AS invoice_tax_amount,
        ab.id AS invoice_id,
        ab.sku::VARCHAR AS product_id,
        ab.itemprice AS unit_price,
        ab.quantity AS gross_invoiced_quantity,
        ab.amount AS gross_invoiced_amount,
        CASE WHEN ab.active THEN 'Posted' ELSE 'Draft' END AS payment_status,
        'ACME Billing' as invoice_source
    FROM {{ ref('stg_acme_billing_data') }} ab
    LEFT JOIN {{ ref('stg_tenant_sfdc_mapping') }} m ON ab._tenant_id::VARCHAR = m.tenant_id::VARCHAR
    WHERE ab.active = true AND ab.isexported = true
),

-- Combined invoice data
cte_all_invoices AS (
    SELECT * FROM cte_sf_invoices
    UNION ALL  
    SELECT * FROM cte_acme_invoices
),

-- Main combined data logic
cte_combined_data AS (
    SELECT DISTINCT
        COALESCE(ib.account_id, cb.account_id) AS account_id,
        COALESCE(cb.tenant_id_c, ib.account_id) AS tenant_id,
        COALESCE(cb.tenant_name_c, 'Unknown') AS tenant_name,
        COALESCE(cb.account_name, 'Unknown') AS account_name,
        cb.billing_enabled_c,
        cb.product_billed_in_sf_c,
        cb.account_status,
        
        -- Parent account information
        pa.id AS parent_account_id,
        pa.tenant_name_c AS parent_tenant_name,
        pa.name AS parent_account_name,
        pa.customer_status_picklist_c AS parent_account_status,
        
        -- Invoice details
        ib.invoice_source,
        ib.billing_month,
        ib.trans_date,
        ib.invoice_total_amount,
        ib.gross_invoiced_amount,
        ib.payment_status,
        
        -- Contract details  
        cb.contract_id,
        cb.contract_start_date,
        cb.contract_end_date,
        cb.contract_status,
        
        -- Product details
        COALESCE(ib.product_id, cb.product_id) AS product_id,
        COALESCE(cb.product_name, 'Unknown Product') AS product_name,
        cb.sf_product_family,
        
        -- Order details
        cb.order_id,
        cb.order_type,
        cb.master_order_c,
        cb.is_master_order_c,
        cb.is_migrated_c,
        cb.order_created_date,
        
        -- Financial metrics
        cb.unit_price as contract_unit_price,
        cb.min_committed_quantity,
        cb.total_min_commitment,
        ib.unit_price as invoiced_unit_price,
        ib.gross_invoiced_quantity,
        cb.exit_ramp_c,
        
        -- Calculated fields
        CASE 
            WHEN cb.exit_ramp_c = TRUE THEN 'Exit Ramp'
            WHEN cb.contract_status = 'Activated' THEN 'Active'
            WHEN cb.contract_status = 'Expired' THEN 'Expired'  
            ELSE 'Other'
        END as contract_category,
        
        -- Commitment vs Invoice variance
        CASE 
            WHEN cb.total_min_commitment IS NOT NULL AND ib.gross_invoiced_amount IS NOT NULL 
            THEN ib.gross_invoiced_amount - cb.total_min_commitment
            ELSE NULL
        END as commitment_variance
        
    FROM cte_contract_base cb
    FULL OUTER JOIN cte_all_invoices ib 
        ON cb.account_id = ib.account_id 
        AND cb.product_id = ib.product_id
        AND DATE_TRUNC('month', cb.order_item_start_date)::DATE = ib.billing_month
    LEFT JOIN cte_parent_child_mapping pcm ON COALESCE(ib.account_id, cb.account_id) = pcm.tenant_account_id
    LEFT JOIN {{ ref('stg_accounts') }} pa ON pcm.fpa_parent_id = pa.id
)

-- Final output with business metrics
SELECT 
    *,
    
    -- Business question metrics
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
        THEN total_min_commitment
        ELSE NULL
    END as exit_ramp_commitment,
    
    -- Composite key for deduplication
    MD5(CONCAT(
        COALESCE(account_id, ''), '-',
        COALESCE(tenant_id, ''), '-', 
        COALESCE(billing_month::VARCHAR, ''), '-',
        COALESCE(product_id, ''), '-',
        COALESCE(contract_id, ''), '-',
        COALESCE(order_id, '')
    )) AS composite_key,
    
    CURRENT_TIMESTAMP() as last_updated
    
FROM cte_combined_data
