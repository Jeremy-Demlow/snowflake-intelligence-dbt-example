{{ config(materialized='table') }}

/*
Customer segments dimension table
Provides clean segmentation data for NDR analysis
*/

SELECT
    parent_account_id,
    size_segment,
    market_segment,
    trade_segment,
    product_category,
    -- Create composite segment for analysis
    CONCAT(size_segment, ' - ', market_segment, ' - ', trade_segment) AS segment_composite
FROM {{ ref('stg_customer_segments') }}
