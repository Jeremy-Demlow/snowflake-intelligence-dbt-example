{% macro create_cortex_search_service(
    service_name=none,
    source_table=none,
    search_schema=none,
    target_lag=none,
    search_column=none,
    attributes=none
) %}
  -- Allow configuration via dbt variables or parameters
  {% set service_name = service_name or var('cortex_search_service_name', none) %}
  {% set source_table = source_table or var('cortex_search_source_table', none) %}
  {% set search_schema = search_schema or var('cortex_search_schema', 'SEARCH') %}
  {% set target_lag = target_lag or var('cortex_search_target_lag', '1 hour') %}
  {% set search_column = search_column or var('cortex_search_column', 'content') %}
  {% set attributes = attributes or var('cortex_search_attributes', 'relative_path, file_url, title, document_type, content_length, file_size') %}
  
  -- Convert 'this' reference to string if passed from post-hook
  {% if source_table is not string %}
    {% set source_table = source_table | string %}
  {% endif %}
  
  -- Validation
  {% if not service_name %}
    {{ exceptions.raise_compiler_error("service_name must be provided as parameter or set cortex_search_service_name variable") }}
  {% endif %}
  {% if not source_table %}
    {{ exceptions.raise_compiler_error("source_table must be provided as parameter or set cortex_search_source_table variable") }}
  {% endif %}
  
  {% set full_schema = target.database ~ '.' ~ search_schema %}
  {% set full_service_name = full_schema ~ '.' ~ service_name %}
  
  -- Create schema if it doesn't exist
  {% set create_schema_sql %}
    CREATE SCHEMA IF NOT EXISTS {{ full_schema }}
  {% endset %}
  
  {% set search_service_sql %}
    CREATE OR REPLACE CORTEX SEARCH SERVICE {{ full_service_name }}
        ON {{ search_column }}
        ATTRIBUTES {{ attributes }}
        WAREHOUSE = {{ target.warehouse }}
        TARGET_LAG = '{{ target_lag }}'
        AS (
            SELECT *
            FROM {{ source_table }}
            WHERE {{ search_column }} IS NOT NULL
            AND LENGTH(TRIM({{ search_column }})) > 10
        )
  {% endset %}

  {% if execute %}
    {{ log("Creating search schema: " ~ full_schema, info=True) }}
    {% do run_query(create_schema_sql) %}
    
    {{ log("Creating Cortex Search service: " ~ full_service_name, info=True) }}
    {% do run_query(search_service_sql) %}
    {{ log("✅ Search service ready with " ~ target_lag ~ " refresh lag", info=True) }}
  {% endif %}

{% endmacro %}

-- Agent creation moved to snowflake_agents/ directory
-- Agents should be managed independently from dbt pipeline
