{{ config(materialized='view') }}

SELECT
    id,
    contract_id,
    account_id,
    opportunity_id,
    type,
    status,
    order_number,
    master_order_c,
    is_master_order_c,
    has_child_orders,
    is_migrated_c,
    created_date

FROM {{ source('acme_raw', 'orders') }}
