{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('acme_raw', 'technicians') }}
),

renamed as (
    select
        technician_id,
        customer_id,
        first_name,
        last_name,
        first_name || ' ' || last_name as full_name,
        hire_date,
        specialization,
        certification_level,
        years_experience,
        is_active,
        created_at,
        updated_at
    from source
)

select * from renamed
