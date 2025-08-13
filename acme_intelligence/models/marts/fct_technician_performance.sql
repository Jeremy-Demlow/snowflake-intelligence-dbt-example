{{
    config(
        materialized='table'
    )
}}

with technician_jobs as (
    select
        t.technician_id,
        t.full_name as technician_name,
        t.first_name,
        t.last_name,
        t.specialization,
        t.certification_level,
        t.years_experience,
        t.customer_id,
        c.company_name,
        c.industry,
        c.company_size,
        c.subscription_tier,
        
        -- Job metrics
        count(j.job_id) as total_jobs,
        count(case when j.is_completed = 1 then j.job_id end) as completed_jobs,
        sum(case when j.is_completed = 1 then j.job_revenue else 0 end) as total_revenue,
        avg(case when j.is_completed = 1 then j.job_revenue end) as avg_job_revenue,
        avg(j.days_to_complete) as avg_days_to_complete,
        
        -- Current year metrics
        count(case when j.scheduled_year = 2025 then j.job_id end) as jobs_2025,
        sum(case when j.scheduled_year = 2025 and j.is_completed = 1 then j.job_revenue else 0 end) as revenue_2025
        
    from {{ ref('stg_technicians') }} t
    left join {{ ref('stg_customers') }} c on t.customer_id = c.customer_id
    left join {{ ref('stg_jobs') }} j on t.technician_id = j.technician_id
    group by 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
),

technician_reviews as (
    select
        r.technician_id,
        count(r.review_id) as total_reviews,
        avg(r.rating) as avg_rating,
        count(case when r.is_positive_review = 1 then r.review_id end) as positive_reviews,
        count(case when r.is_negative_review = 1 then r.review_id end) as negative_reviews,
        
        -- Review distribution
        count(case when r.rating = 5 then r.review_id end) as five_star_reviews,
        count(case when r.rating = 4 then r.review_id end) as four_star_reviews,
        count(case when r.rating = 3 then r.review_id end) as three_star_reviews,
        count(case when r.rating = 2 then r.review_id end) as two_star_reviews,
        count(case when r.rating = 1 then r.review_id end) as one_star_reviews
        
    from {{ ref('stg_reviews') }} r
    group by r.technician_id
),

final as (
    select
        tj.*,
        
        -- Review metrics
        coalesce(tr.total_reviews, 0) as total_reviews,
        tr.avg_rating,
        coalesce(tr.positive_reviews, 0) as positive_reviews,
        coalesce(tr.negative_reviews, 0) as negative_reviews,
        coalesce(tr.five_star_reviews, 0) as five_star_reviews,
        coalesce(tr.four_star_reviews, 0) as four_star_reviews,
        coalesce(tr.three_star_reviews, 0) as three_star_reviews,
        coalesce(tr.two_star_reviews, 0) as two_star_reviews,
        coalesce(tr.one_star_reviews, 0) as one_star_reviews,
        
        -- Performance categories
        case
            when tr.avg_rating >= 4.5 then 'Excellent'
            when tr.avg_rating >= 4.0 then 'Good'
            when tr.avg_rating >= 3.0 then 'Average'
            when tr.avg_rating >= 2.0 then 'Poor'
            when tr.avg_rating < 2.0 then 'Very Poor'
            else 'No Reviews'
        end as performance_category,
        
        case
            when tr.avg_rating < 3.0 then 1
            else 0
        end as is_underperforming,
        
        -- Revenue per review (quality indicator)
        case
            when coalesce(tr.total_reviews, 0) > 0
            then tj.total_revenue / tr.total_reviews
            else null
        end as revenue_per_review,
        
        current_timestamp() as last_updated
        
    from technician_jobs tj
    left join technician_reviews tr on tj.technician_id = tr.technician_id
)

select * from final
