{{ config(materialized='view') }}

SELECT
    id,
    order_id,
    product_id,
    product_code,
    quantity,
    unit_price,
    total_price,
    min_committed_quantity,
    total_min_commitment,
    start_date,
    end_date,
    billing_day_of_month,
    exit_ramp_c,
    product_family,
    created_date

FROM {{ source('acme_raw', 'order_items') }}
