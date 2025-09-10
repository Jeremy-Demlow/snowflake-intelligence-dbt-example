{{ config(materialized='view') }}

SELECT
    id,
    _tenant_id,
    _tenant_name,
    account_id,  -- ADD NEW COLUMN
    contract_id, -- ADD NEW COLUMN  
    trans_date,
    description,
    amount,
    tax,
    type,
    balancetype,
    active,
    isexported,
    sku,
    itemprice,
    quantity

FROM {{ source('acme_raw', 'acme_billing_data') }}
