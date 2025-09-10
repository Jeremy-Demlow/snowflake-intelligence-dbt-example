{{ config(materialized='view') }}

SELECT
    id,
    account_id,
    opportunity_id,
    status,
    start_date,
    end_date,
    term,
    created_date

FROM {{ source('acme_raw', 'contracts') }}
