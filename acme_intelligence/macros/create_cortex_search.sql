{% macro create_cortex_search_service() %}
  
  {% set search_service_sql %}
    CREATE OR REPLACE CORTEX SEARCH SERVICE {{ target.database }}.SEARCH.acme_document_search
        ON content
        ATTRIBUTES relative_path, file_url, title, document_type
        WAREHOUSE = {{ target.warehouse }}
        TARGET_LAG = '1 day'
        AS (
            SELECT
                relative_path,
                file_url,
                title,
                document_type,
                content
            FROM {{ target.database }}.RAW.STG_PARSED_DOCUMENTS
        )
  {% endset %}

  {% if execute %}
    {{ log("Creating Cortex Search service...", info=True) }}
    {% do run_query(search_service_sql) %}
    {{ log("Cortex Search service created successfully!", info=True) }}
  {% endif %}

{% endmacro %}

-- Agent creation moved to snowflake_agents/ directory
-- Agents should be managed independently from dbt pipeline
