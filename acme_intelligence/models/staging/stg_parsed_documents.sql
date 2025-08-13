{{
    config(
        materialized='table',
        schema='raw'
    )
}}

-- Parse documents from stage and prepare for Cortex Search
WITH file_content AS (
    SELECT 
        LISTAGG($1, '\n') WITHIN GROUP (ORDER BY metadata$file_row_number) as full_content
    FROM @{{ target.database }}.RAW.ACME_STG/acme_annual_report.txt
),

parsed_content AS (
    SELECT 
        'acme_stg/acme_annual_report.txt' as relative_path,
        BUILD_STAGE_FILE_URL('@{{ target.database }}.RAW.ACME_STG', 'acme_annual_report.txt') as file_url,
        'ACME Services Annual Report 2024' as title,
        'annual_report' as document_type,
        '2024' as document_year,
        full_content as content,
        CURRENT_TIMESTAMP() as parsed_at
    FROM file_content
)

SELECT * FROM parsed_content
