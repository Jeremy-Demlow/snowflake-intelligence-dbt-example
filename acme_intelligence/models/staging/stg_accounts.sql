{{ config(materialized='view') }}

SELECT
    id,
    name,
    tenant_id_c,
    tenant_name_c,
    parent_id,
    customer_status_picklist_c,
    billing_enabled_c,
    billing_comparison_status_c,
    data_validated_c,
    product_billed_in_sf_c

FROM {{ source('acme_raw', 'accounts') }}
