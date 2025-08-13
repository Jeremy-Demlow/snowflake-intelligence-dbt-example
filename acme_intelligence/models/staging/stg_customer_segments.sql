{{ config(materialized='view') }}

/*
Staging model for customer segmentation data
Contains size, market, trade, and product category segments for NDR analysis
*/

SELECT
    parent_account_id,
    size_segment,
    market_segment,
    trade_segment,
    product_category
FROM {{ source('acme_raw', 'customer_segments') }}
