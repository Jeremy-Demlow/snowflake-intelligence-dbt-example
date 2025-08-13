{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('acme_raw', 'customers') }}
),

renamed as (
    select
        customer_id,
        company_name,
        industry,
        company_size,
        location_state,
        location_city,
        signup_date,
        subscription_tier,
        monthly_revenue,
        created_at,
        updated_at
    from source
)

select * from renamed
