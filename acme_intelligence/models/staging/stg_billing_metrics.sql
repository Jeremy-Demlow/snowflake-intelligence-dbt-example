{{ config(materialized='view') }}

/*
Staging model for billing metrics data
Contains monthly ARR data for NDR calculations
*/

SELECT
    parent_account_id,
    child_account_id,
    ndr_parent,
    month_id,
    billing_month,
    l3m_arr,
    size_segment,
    market_segment,
    trade_segment,
    product_category
FROM {{ source('acme_raw', 'billing_metrics') }}
