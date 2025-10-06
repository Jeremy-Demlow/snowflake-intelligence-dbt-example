{{
  config(
    materialized='semantic_view'
  )
}}

-- Snowflake Performance Coach Semantic View - Using OUR materialized table
-- This works because we're using a table WE control, not ACCOUNT_USAGE directly

CREATE OR REPLACE SEMANTIC VIEW {{ target.database }}.SEMANTIC_MODELS.snowflake_usage_analytics_view

  TABLES (
    -- Our materialized performance table (following your working pattern!)
    PERF_DATA AS {{ ref('fct_query_performance') }}
      PRIMARY KEY (query_id)
      WITH SYNONYMS ('performance_data', 'query_data', 'usage_data')
      COMMENT = 'Query performance data with credit attribution and optimization indicators'
  )

  FACTS (
    -- Performance timing facts
    PERF_DATA.total_elapsed_time AS total_elapsed_time,
    PERF_DATA.execution_time AS execution_time,
    PERF_DATA.compilation_time AS compilation_time,
    PERF_DATA.queued_overload_time AS queued_overload_time,
    PERF_DATA.queued_provisioning_time AS queued_provisioning_time,
    PERF_DATA.queued_repair_time AS queued_repair_time,
    -- Spilling facts
    PERF_DATA.bytes_spilled_to_local_storage AS bytes_spilled_to_local_storage,
    PERF_DATA.bytes_spilled_to_remote_storage AS bytes_spilled_to_remote_storage,
    -- Credit facts (the gold from QUERY_ATTRIBUTION_HISTORY!)
    PERF_DATA.credits_attributed_compute AS credits_attributed_compute,
    PERF_DATA.credits_used_query_acceleration AS credits_used_query_acceleration,
    PERF_DATA.credits_used_cloud_services AS credits_used_cloud_services,
    -- Data scanning facts
    PERF_DATA.bytes_scanned AS bytes_scanned,
    PERF_DATA.partitions_scanned AS partitions_scanned,
    PERF_DATA.partitions_total AS partitions_total,
    PERF_DATA.percentage_scanned_from_cache AS percentage_scanned_from_cache,
    -- Pre-calculated performance indicators
    PERF_DATA.has_remote_spilling AS has_remote_spilling,
    PERF_DATA.has_local_spilling AS has_local_spilling,
    PERF_DATA.has_queue_time AS has_queue_time,
    PERF_DATA.is_slow_query AS is_slow_query
  )

  DIMENSIONS (
    -- Warehouse coaching dimensions
    PERF_DATA.warehouse_name AS warehouse_name
      WITH SYNONYMS ('warehouse')
      COMMENT = 'Warehouse used for query execution',
      
    PERF_DATA.warehouse_size AS warehouse_size
      WITH SYNONYMS ('size')
      COMMENT = 'Warehouse size - optimization target for scaling',
      
    PERF_DATA.database_name AS database_name
      WITH SYNONYMS ('database')
      COMMENT = 'Database accessed - clustering analysis context',
      
    PERF_DATA.user_name AS user_name
      WITH SYNONYMS ('user')
      COMMENT = 'User executing queries - workload analysis',
      
    PERF_DATA.query_type AS query_type
      WITH SYNONYMS ('type')
      COMMENT = 'Type of query executed',
      
    PERF_DATA.execution_status AS execution_status
      WITH SYNONYMS ('status')
      COMMENT = 'Query execution status',
      
    PERF_DATA.query_date AS query_date
      WITH SYNONYMS ('date')
      COMMENT = 'Query execution date for trend analysis',
      
    PERF_DATA.query_id AS query_id
      WITH SYNONYMS ('id')
      COMMENT = 'Unique query identifier for deep analysis'
  )

  METRICS (
    -- === BASIC PERFORMANCE METRICS ===
    PERF_DATA.total_queries AS COUNT(*)
      WITH SYNONYMS ('query_count', 'total_count')
      COMMENT = 'Total queries analyzed for performance coaching',
      
    -- === CREDIT COACHING METRICS (the key value!) ===
    PERF_DATA.total_compute_credits AS SUM(PERF_DATA.credits_attributed_compute)
      WITH SYNONYMS ('compute_credits', 'cost_baseline')
      COMMENT = 'Total compute credits - primary cost optimization target',
      
    PERF_DATA.avg_compute_credits AS AVG(PERF_DATA.credits_attributed_compute)
      WITH SYNONYMS ('average_compute_credits', 'credit_efficiency')
      COMMENT = 'Average compute credits per query - cost efficiency indicator',
      
    PERF_DATA.total_acceleration_credits AS SUM(PERF_DATA.credits_used_query_acceleration)
      WITH SYNONYMS ('acceleration_credits', 'qas_credits')
      COMMENT = 'Total query acceleration credits - QAS optimization opportunities',
      
    -- === SPILLING COACH METRICS (Gen 2 upgrade indicators) ===
    PERF_DATA.queries_with_remote_spilling AS SUM(PERF_DATA.has_remote_spilling)
      WITH SYNONYMS ('remote_spill_queries', 'critical_performance_issues')
      COMMENT = 'Queries with remote spilling - CRITICAL: immediate Gen 2 upgrade needed',
      
    PERF_DATA.queries_with_local_spilling AS SUM(PERF_DATA.has_local_spilling)
      WITH SYNONYMS ('local_spill_queries', 'memory_pressure_queries')
      COMMENT = 'Queries with local spilling - warehouse undersizing indicator',
      
    PERF_DATA.total_local_spill_gb AS SUM(PERF_DATA.bytes_spilled_to_local_storage) / 1024 / 1024 / 1024
      WITH SYNONYMS ('local_spill_volume_gb')
      COMMENT = 'Total local spilling in GB - warehouse sizing optimization',
      
    PERF_DATA.total_remote_spill_gb AS SUM(PERF_DATA.bytes_spilled_to_remote_storage) / 1024 / 1024 / 1024
      WITH SYNONYMS ('remote_spill_volume_gb')
      COMMENT = 'Total remote spilling in GB - critical performance degradation',
      
    -- === QUEUE TIME COACH METRICS ===
    PERF_DATA.queries_with_queue_time AS SUM(PERF_DATA.has_queue_time)
      WITH SYNONYMS ('queued_queries', 'contention_queries')
      COMMENT = 'Queries with queue time - warehouse contention indicator',
      
    PERF_DATA.avg_queue_time_ms AS AVG(PERF_DATA.queued_overload_time + PERF_DATA.queued_provisioning_time + PERF_DATA.queued_repair_time)
      WITH SYNONYMS ('average_queue_time')
      COMMENT = 'Average queue time - concurrency optimization indicator',
      
    -- === PERFORMANCE COACH METRICS ===
    PERF_DATA.slow_queries AS SUM(PERF_DATA.is_slow_query)
      WITH SYNONYMS ('slow_query_count', 'optimization_candidates')
      COMMENT = 'Queries over 1 minute - primary optimization targets',
      
    PERF_DATA.avg_execution_time_ms AS AVG(PERF_DATA.execution_time)
      WITH SYNONYMS ('average_execution_time')
      COMMENT = 'Average execution time - performance baseline',
      
    -- === DATA EFFICIENCY COACH METRICS ===
    PERF_DATA.avg_cache_hit_rate AS AVG(PERF_DATA.percentage_scanned_from_cache)
      WITH SYNONYMS ('cache_efficiency')
      COMMENT = 'Average cache hit rate - query optimization indicator'
  )

  COMMENT = 'Performance and cost coaching semantic view with actionable warehouse optimization insights'
