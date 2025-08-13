{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('acme_raw', 'reviews') }}
),

renamed as (
    select
        review_id,
        job_id,
        customer_id,
        technician_id,
        rating,
        review_text,
        review_source,
        review_date,
        is_verified,
        created_at,
        
        -- Add calculated fields
        case
            when rating >= 4 then 'Positive'
            when rating = 3 then 'Neutral'
            when rating <= 2 then 'Negative'
            else 'Unknown'
        end as review_sentiment,
        
        case
            when rating >= 4 then 1
            else 0
        end as is_positive_review,
        
        case
            when rating <= 2 then 1
            else 0
        end as is_negative_review,
        
        extract(year from review_date) as review_year,
        extract(month from review_date) as review_month
        
    from source
)

select * from renamed
