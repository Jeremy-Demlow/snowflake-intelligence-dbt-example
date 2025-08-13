{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('acme_raw', 'jobs') }}
),

renamed as (
    select
        job_id,
        customer_id,
        technician_id,
        job_type,
        job_status,
        scheduled_date,
        completed_date,
        job_revenue,
        job_duration_hours,
        service_address,
        job_description,
        created_at,
        updated_at,
        
        -- Add calculated fields
        case 
            when completed_date is not null and scheduled_date is not null
            then datediff('day', scheduled_date, completed_date)
            else null
        end as days_to_complete,
        
        case
            when job_status = 'Completed' then 1
            else 0
        end as is_completed,
        
        extract(year from scheduled_date) as scheduled_year,
        extract(month from scheduled_date) as scheduled_month
        
    from source
)

select * from renamed
