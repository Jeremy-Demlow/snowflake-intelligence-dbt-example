{{ config(materialized='view') }}

SELECT
    id,
    name,
    product_code,
    product_category_c,
    family,
    is_active

FROM {{ source('acme_raw', 'products') }}
