{{
    config(
        materialized='table'
    )
}}

with job_details as (
    select
        j.job_id,
        j.customer_id,
        j.technician_id,
        j.job_type,
        j.job_status,
        j.scheduled_date,
        j.completed_date,
        j.job_revenue,
        j.job_duration_hours,
        j.service_address,
        j.job_description,
        j.days_to_complete,
        j.is_completed,
        j.scheduled_year,
        j.scheduled_month,
        
        -- Customer details
        c.company_name,
        c.industry,
        c.company_size,
        c.subscription_tier,
        c.location_state,
        c.location_city,
        
        -- Technician details
        t.full_name as technician_name,
        t.first_name as technician_first_name,
        t.last_name as technician_last_name,
        t.specialization,
        t.certification_level,
        t.years_experience,
        
        -- Job categorization
        case
            when j.job_revenue >= 1000 then 'High Value'
            when j.job_revenue >= 500 then 'Medium Value'
            when j.job_revenue >= 200 then 'Low Value'
            else 'Minimal Value'
        end as revenue_category,
        
        case
            when j.job_duration_hours >= 6 then 'Long Duration'
            when j.job_duration_hours >= 3 then 'Medium Duration'
            when j.job_duration_hours >= 1 then 'Short Duration'
            else 'Quick Job'
        end as duration_category
        
    from {{ ref('stg_jobs') }} j
    left join {{ ref('stg_customers') }} c on j.customer_id = c.customer_id
    left join {{ ref('stg_technicians') }} t on j.technician_id = t.technician_id
),

job_reviews as (
    select
        r.job_id,
        r.rating as job_rating,
        r.review_sentiment,
        r.review_source,
        r.review_date,
        r.is_positive_review,
        r.is_negative_review
    from {{ ref('stg_reviews') }} r
),

final as (
    select
        jd.*,
        
        -- Review information
        jr.job_rating,
        jr.review_sentiment,
        jr.review_source,
        jr.review_date,
        jr.is_positive_review,
        jr.is_negative_review,
        
        -- Has review flag
        case
            when jr.job_id is not null then 1
            else 0
        end as has_review,
        
        current_timestamp() as last_updated
        
    from job_details jd
    left join job_reviews jr on jd.job_id = jr.job_id
)

select * from final
