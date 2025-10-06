{{ config(
    materialized='table',
    cluster_by=['warehouse_name', 'query_date']
) }}

-- Query Performance Fact Table
-- Pulls from ACCOUNT_USAGE and materializes for semantic view use

WITH query_performance AS (
    SELECT 
        qh.query_id,
        qh.warehouse_name,
        qh.warehouse_size,
        qh.database_name,
        qh.user_name,
        qh.query_type,
        qh.execution_status,
        DATE(qh.start_time) as query_date,
        qh.start_time,
        qh.end_time,
        qh.total_elapsed_time,
        qh.execution_time,
        qh.compilation_time,
        qh.queued_overload_time,
        qh.queued_provisioning_time,
        qh.queued_repair_time,
        qh.bytes_spilled_to_local_storage,
        qh.bytes_spilled_to_remote_storage,
        qh.bytes_scanned,
        qh.partitions_scanned,
        qh.partitions_total,
        qh.percentage_scanned_from_cache,
        qh.credits_used_cloud_services,
        -- Get credit attribution data
        qa.credits_attributed_compute,
        qa.credits_used_query_acceleration,
        -- Performance indicators (pre-calculated for semantic view)
        CASE WHEN qh.bytes_spilled_to_remote_storage > 0 THEN 1 ELSE 0 END as has_remote_spilling,
        CASE WHEN qh.bytes_spilled_to_local_storage > 0 THEN 1 ELSE 0 END as has_local_spilling,
        CASE WHEN (qh.queued_overload_time + qh.queued_provisioning_time + qh.queued_repair_time) > 0 THEN 1 ELSE 0 END as has_queue_time,
        CASE WHEN qh.total_elapsed_time > 60000 THEN 1 ELSE 0 END as is_slow_query
    FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY qh
    LEFT JOIN SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY qa 
        ON qh.query_id = qa.query_id
    WHERE qh.start_time >= DATEADD('day', -30, CURRENT_TIMESTAMP())  -- Last 30 days
      AND qh.warehouse_name IS NOT NULL
      AND qh.execution_status = 'SUCCESS'
)

SELECT * FROM query_performance
