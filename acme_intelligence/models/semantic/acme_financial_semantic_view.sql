{{
  config(
    materialized='semantic_view'
  )
}}

-- ACME Financial Intelligence Semantic View
-- 
-- This file creates a comprehensive semantic view for ACME Financial analytics,
-- combining NDR calculations, ARR metrics, and customer segmentation to enable 
-- natural language queries through Cortex Analyst.
--
-- To create/update the semantic view, run:
-- dbt run --select acme_financial_semantic_view
--
-- The semantic view provides comprehensive analytics for:
-- - Net Dollar Retention (NDR) analysis
-- - ARR expansion and growth tracking  
-- - Customer segmentation analysis
-- - Financial performance metrics
--
-- This enables natural language queries through Cortex Analyst such as:
-- "What is the latest NDR?"
-- "What is the latest NDR for Enterprise segment customers?"
-- "Show me NDR trends by market segment over the last 6 months"
-- "Which customer segments have the highest ARR expansion?"

TABLES (
    -- Core NDR calculations fact table
    NDR_DATA AS {{ ref('fct_ndr_calculations') }}
      PRIMARY KEY (NDR_PARENT, MONTH_ID)
      WITH SYNONYMS ('ndr_data', 'financial_data', 'ndr_metrics', 'financial_metrics')
      COMMENT = 'NDR calculations with ARR expansion and customer segmentation'
  )

  FACTS (
    -- NDR and ARR facts for cleaner metric expressions
    NDR_DATA.ndr_percentage_fact AS NDR_PERCENTAGE
      COMMENT = 'Net Dollar Retention percentage fact',
    NDR_DATA.current_arr_fact AS L3M_ARR_CURRENT
      COMMENT = 'Current L3M ARR fact',
    NDR_DATA.previous_arr_fact AS L3M_ARR_PREVIOUS_YEAR
      COMMENT = 'Previous year L3M ARR fact',
    NDR_DATA.arr_expansion_fact AS ARR_EXPANSION
      COMMENT = 'ARR expansion amount fact'
  )

  DIMENSIONS (
    -- Account and parent dimensions
    NDR_DATA.NDR_PARENT AS ndr_parent
      WITH SYNONYMS ('parent_account', 'account', 'customer')
      COMMENT = 'NDR parent account grouping',
      
    NDR_DATA.MONTH_ID AS month_id
      WITH SYNONYMS ('month', 'period', 'billing_month')
      COMMENT = 'Month identifier in YYYYMM format',
      
    NDR_DATA.BILLING_MONTH AS billing_month
      WITH SYNONYMS ('month_date', 'period_date', 'billing_date')
      COMMENT = 'Billing month as date for time analysis',
    
    -- Customer segmentation dimensions
    NDR_DATA.SIZE_SEGMENT AS size_segment
      WITH SYNONYMS ('size', 'customer_size', 'segment_size')
      COMMENT = 'Customer size segment (SMB, Mid-Market, Enterprise)',
      
    NDR_DATA.MARKET_SEGMENT AS market_segment
      WITH SYNONYMS ('market', 'market_type', 'customer_market')
      COMMENT = 'Market segment (Residential, Commercial, Industrial)',
      
    NDR_DATA.TRADE_SEGMENT AS trade_segment
      WITH SYNONYMS ('trade', 'trade_type', 'industry_segment')
      COMMENT = 'Trade segment (HVAC, Plumbing, Electrical, Multi-Trade)',
      
    NDR_DATA.PRODUCT_CATEGORY AS product_category
      WITH SYNONYMS ('product', 'product_type', 'category')
      COMMENT = 'Product category (Core Platform, Add-on Modules, Premium Features)'
  )

  METRICS (
    -- NDR metrics using facts
    NDR_DATA.avg_ndr AS AVG(NDR_DATA.ndr_percentage_fact)
      COMMENT = 'Average Net Dollar Retention percentage',
      
    -- ARR metrics using facts
    NDR_DATA.total_current_arr AS SUM(NDR_DATA.current_arr_fact)
      COMMENT = 'Total current ARR across all accounts',
    
    NDR_DATA.total_previous_arr AS SUM(NDR_DATA.previous_arr_fact)
      COMMENT = 'Total previous year ARR for comparison',
      
    NDR_DATA.total_arr_expansion AS SUM(NDR_DATA.arr_expansion_fact)
      COMMENT = 'Total ARR expansion amount',
      
    NDR_DATA.avg_arr_per_account AS AVG(NDR_DATA.current_arr_fact)
      COMMENT = 'Average ARR per account',
    
    -- Expansion and growth metrics using facts
    NDR_DATA.avg_expansion_rate AS AVG(CASE WHEN NDR_DATA.previous_arr_fact > 0 THEN (NDR_DATA.arr_expansion_fact / NDR_DATA.previous_arr_fact) * 100 END)
      COMMENT = 'Average expansion rate percentage',
      
    NDR_DATA.positive_expansion_count AS COUNT(CASE WHEN NDR_DATA.arr_expansion_fact > 0 THEN 1 END)
      COMMENT = 'Number of accounts with positive ARR expansion',
      
    NDR_DATA.negative_expansion_count AS COUNT(CASE WHEN NDR_DATA.arr_expansion_fact < 0 THEN 1 END)
      COMMENT = 'Number of accounts with negative ARR expansion',
    
    -- Count metrics (using dimensions)
    NDR_DATA.account_count AS COUNT(DISTINCT NDR_DATA.ndr_parent)
      COMMENT = 'Number of unique customer accounts',
      
    NDR_DATA.month_count AS COUNT(DISTINCT NDR_DATA.month_id)
      COMMENT = 'Number of unique months in analysis',
      
    -- Segment-specific metrics (using dimensions)
    NDR_DATA.enterprise_accounts AS COUNT(CASE WHEN NDR_DATA.size_segment = 'Enterprise' THEN 1 END)
      COMMENT = 'Number of Enterprise segment accounts',
      
    NDR_DATA.smb_accounts AS COUNT(CASE WHEN NDR_DATA.size_segment = 'SMB' THEN 1 END)
      COMMENT = 'Number of SMB segment accounts',
      
    NDR_DATA.ndr_3month_trend AS AVG(NDR_DATA.avg_ndr) OVER (
      PARTITION BY NDR_DATA.ndr_parent 
      ORDER BY NDR_DATA.month_id 
      ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) COMMENT = '3-month rolling NDR trend per account',
    
    NDR_DATA.ndr_vs_segment_avg AS NDR_DATA.avg_ndr - AVG(NDR_DATA.avg_ndr) OVER (
      PARTITION BY NDR_DATA.size_segment
    ) COMMENT = 'NDR relative to segment average (outperformance)',
    
    NDR_DATA.arr_growth_momentum AS NDR_DATA.total_current_arr - LAG(NDR_DATA.total_current_arr, 1) OVER (
      PARTITION BY NDR_DATA.ndr_parent 
      ORDER BY NDR_DATA.month_id
    ) COMMENT = 'Month-over-month ARR growth momentum'
  )

  COMMENT = 'ACME Financial Intelligence semantic view for NDR analysis, ARR tracking, and customer segmentation'