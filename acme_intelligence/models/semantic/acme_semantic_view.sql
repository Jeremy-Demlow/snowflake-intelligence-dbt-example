{{
  config(
    materialized='semantic_view',
    pre_hook="SELECT 1 FROM {{ ref('fct_technician_performance') }} LIMIT 1"
  )
}}

-- ACME Intelligence Semantic View
-- 
-- This file creates a comprehensive semantic view for ACME Services analytics,
-- combining technician performance data and job information to enable 
-- natural language queries through Cortex Analyst.
--
-- To create/update the semantic view, run:
-- dbt run --select acme_semantic_view
--
-- The semantic view provides comprehensive analytics for:
-- - Technician performance analysis
-- - Job revenue and completion tracking  
-- - Customer satisfaction metrics
-- - Company and industry insights
--
-- This enables natural language queries through Cortex Analyst such as:
-- "Which technicians are underperforming?"
-- "What's our total revenue by specialization?"
-- "Show me technicians with high ratings in HVAC"

CREATE OR REPLACE SEMANTIC VIEW {{ var('dbt_cortex_database') }}.{{ var('semantic_schema') }}.acme_analytics_view

  TABLES (
    -- Core technician performance dimension/fact table
    technician_performance AS {{ var('dbt_cortex_database') }}.{{ var('analytics_schema') }}.FCT_TECHNICIAN_PERFORMANCE
      PRIMARY KEY (TECHNICIAN_ID)
      WITH SYNONYMS ('technician_data', 'performance_data', 'technician_metrics', 'tech_performance')
      COMMENT = 'Technician performance metrics including jobs, revenue, and customer reviews',
      
    -- Individual job records fact table  
    jobs AS {{ var('dbt_cortex_database') }}.{{ var('analytics_schema') }}.FCT_JOBS
      PRIMARY KEY (JOB_ID)  
      WITH SYNONYMS ('job_data', 'service_jobs', 'work_orders', 'service_calls')
      COMMENT = 'Individual job records with details about services performed'
  )

  RELATIONSHIPS (
    -- Link jobs to technicians
    jobs_to_technicians AS
      jobs (TECHNICIAN_ID) REFERENCES technician_performance
  )

  FACTS (
    -- Technician-level facts
    technician_performance.TOTAL_JOBS AS total_jobs
      COMMENT = 'Total number of jobs performed by technician',
    technician_performance.COMPLETED_JOBS AS completed_jobs
      COMMENT = 'Number of completed jobs',
    technician_performance.TOTAL_REVENUE AS total_revenue
      COMMENT = 'Total revenue generated from all jobs',
    technician_performance.REVENUE_2025 AS revenue_2025
      COMMENT = 'Revenue generated in 2025',
    technician_performance.AVG_JOB_REVENUE AS avg_job_revenue
      COMMENT = 'Average revenue per job',
    technician_performance.TOTAL_REVIEWS AS total_reviews
      COMMENT = 'Total number of customer reviews received',
    technician_performance.AVG_RATING AS avg_rating
      COMMENT = 'Average customer rating (1-5 stars)',
    technician_performance.POSITIVE_REVIEWS AS positive_reviews
      COMMENT = 'Number of positive reviews (4-5 stars)',
    technician_performance.NEGATIVE_REVIEWS AS negative_reviews
      COMMENT = 'Number of negative reviews (1-2 stars)',
    technician_performance.YEARS_EXPERIENCE AS years_experience
      COMMENT = 'Years of experience in the field',
    technician_performance.REVENUE_PER_REVIEW AS revenue_per_review
      COMMENT = 'Average revenue generated per customer review'
  )

  DIMENSIONS (
    -- Technician identification dimensions
    technician_performance.TECHNICIAN_ID AS technician_id
      WITH SYNONYMS ('tech_id', 'technician', 'tech')
      COMMENT = 'Unique identifier for technician',
    
    technician_performance.TECHNICIAN_NAME AS technician_name
      WITH SYNONYMS ('technician', 'tech_name', 'name', 'full_name')
      COMMENT = 'Full name of the technician',
      
    technician_performance.FIRST_NAME AS first_name
      WITH SYNONYMS ('fname', 'given_name')
      COMMENT = 'Technician first name',
      
    technician_performance.LAST_NAME AS last_name
      WITH SYNONYMS ('lname', 'surname', 'family_name')
      COMMENT = 'Technician last name',
    
    -- Technician skill and performance dimensions
    technician_performance.SPECIALIZATION AS specialization
      WITH SYNONYMS ('specialty', 'trade', 'skill', 'expertise')
      COMMENT = 'Technical specialization (HVAC, Plumbing, Electrical, etc.)',
      
    technician_performance.CERTIFICATION_LEVEL AS certification_level
      WITH SYNONYMS ('cert_level', 'certification', 'level')
      COMMENT = 'Certification level (Junior, Senior, Expert)',
    
    technician_performance.IS_UNDERPERFORMING AS is_underperforming
      WITH SYNONYMS ('underperforming', 'poor_performance', 'low_rating')
      COMMENT = 'Flag indicating if technician has average rating below 3 stars',
      
    technician_performance.PERFORMANCE_CATEGORY AS performance_category
      WITH SYNONYMS ('performance', 'rating_category', 'performance_level')
      COMMENT = 'Performance rating category (Excellent, Good, Average, Poor, Very Poor, No Reviews)',
    
    -- Company and business dimensions
    technician_performance.COMPANY_NAME AS company_name
      WITH SYNONYMS ('company', 'customer', 'client', 'business')
      COMMENT = 'Name of the service company',
      
    technician_performance.INDUSTRY AS industry
      WITH SYNONYMS ('vertical', 'sector', 'business_type')
      COMMENT = 'Industry vertical (HVAC, Plumbing, Electrical, Roofing)',
      
    technician_performance.COMPANY_SIZE AS company_size
      WITH SYNONYMS ('size', 'company_tier')
      COMMENT = 'Company size classification (Small, Medium, Large)',
      
    technician_performance.SUBSCRIPTION_TIER AS subscription_tier
      WITH SYNONYMS ('plan', 'subscription', 'tier')
      COMMENT = 'ACME Services subscription level (Basic, Pro, Enterprise)',
      
    -- Temporal dimensions
    technician_performance.LAST_UPDATED AS last_updated
      WITH SYNONYMS ('updated', 'refresh_date', 'data_date')
      COMMENT = 'Last update timestamp'
  )

  METRICS (
    -- Revenue metrics
    technician_performance.TOTAL_REVENUE_SUM AS SUM(technician_performance.TOTAL_REVENUE)
      COMMENT = 'Total revenue generated across all technicians',
    
    technician_performance.REVENUE_2025_SUM AS SUM(technician_performance.REVENUE_2025)
      COMMENT = 'Total revenue in 2025',
      
    technician_performance.AVG_JOB_REVENUE_AVG AS AVG(technician_performance.AVG_JOB_REVENUE)
      COMMENT = 'Average job revenue across all technicians',
    
    -- Performance and rating metrics
    technician_performance.AVG_RATING_AVG AS AVG(technician_performance.AVG_RATING)
      COMMENT = 'Average rating across all technicians',
    
    technician_performance.POSITIVE_REVIEWS_SUM AS SUM(technician_performance.POSITIVE_REVIEWS)
      COMMENT = 'Total number of positive reviews',
      
    technician_performance.NEGATIVE_REVIEWS_SUM AS SUM(technician_performance.NEGATIVE_REVIEWS)
      COMMENT = 'Total number of negative reviews',
      
    technician_performance.TOTAL_REVIEWS_SUM AS SUM(technician_performance.TOTAL_REVIEWS)
      COMMENT = 'Total number of reviews across all technicians',
    
    -- Count metrics
    technician_performance.TECHNICIAN_COUNT AS COUNT(DISTINCT technician_performance.TECHNICIAN_ID)
      COMMENT = 'Number of unique technicians',
      
    technician_performance.UNDERPERFORMING_COUNT AS COUNT(CASE WHEN technician_performance.IS_UNDERPERFORMING = 1 THEN 1 END)
      COMMENT = 'Number of underperforming technicians',
      
    technician_performance.TOTAL_JOBS_SUM AS SUM(technician_performance.TOTAL_JOBS)
      COMMENT = 'Total number of jobs across all technicians'
  )

  COMMENT = 'ACME Intelligence semantic view for analyzing technician performance, job revenue, and customer satisfaction'
