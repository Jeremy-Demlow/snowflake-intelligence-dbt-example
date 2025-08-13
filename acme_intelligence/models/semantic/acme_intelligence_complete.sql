{{
    config(
        materialized='table',
        post_hook=[
            "{{ create_cortex_search_service() }}"
        ]
    )
}}

-- ACME Intelligence Complete Setup
-- This model creates the complete Snowflake Intelligence solution

-- Verify all dependencies exist
WITH validation AS (
    SELECT 
        'ACME Intelligence Setup Complete' as status,
        COUNT(*) as technician_count,
        SUM(revenue_2025) as total_revenue_2025,
        AVG(avg_rating) as avg_rating,
        SUM(CASE WHEN is_underperforming = 1 THEN 1 ELSE 0 END) as underperforming_count
    FROM {{ ref('fct_technician_performance') }}
),

document_validation AS (
    SELECT 
        COUNT(*) as document_count,
        SUM(LENGTH(content)) as total_content_length
    FROM {{ ref('stg_parsed_documents') }}
)

SELECT 
    v.status,
    v.technician_count,
    v.total_revenue_2025,
    v.avg_rating,
    v.underperforming_count,
    d.document_count,
    d.total_content_length,
    CURRENT_TIMESTAMP() as created_at
FROM validation v
CROSS JOIN document_validation d
