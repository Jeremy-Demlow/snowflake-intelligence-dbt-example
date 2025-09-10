{{ config(materialized='view') }}

SELECT
    tenant_id,
    sfdc_account_id

FROM {{ source('acme_raw', 'tenant_sfdc_mapping') }}
