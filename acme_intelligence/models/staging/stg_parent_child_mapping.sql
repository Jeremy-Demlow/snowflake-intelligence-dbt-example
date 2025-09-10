{{ config(materialized='view') }}

SELECT
    snapshot_date,
    tenant_account_id,
    parent_account_name_current,
    parent_tenant_id_current,
    parent_child_flag,
    fpa_parent_id

FROM {{ source('acme_raw', 'parent_child_mapping') }}
