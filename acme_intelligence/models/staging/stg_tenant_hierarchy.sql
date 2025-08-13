{{ config(materialized='view') }}

/*
Staging model for tenant hierarchy data
Maps parent and child accounts for NDR calculations
*/

SELECT
    child_account_id,
    parent_account_id,
    child_tenant_id,
    ndr_parent,
    parent_start_date
FROM {{ source('acme_raw', 'tenant_hierarchy') }}
