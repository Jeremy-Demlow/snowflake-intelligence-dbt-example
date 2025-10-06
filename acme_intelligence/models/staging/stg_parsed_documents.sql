{{
    config(
        materialized='table',
        schema='raw'
    )
}}

-- Step 1: SCALABLE Document Parsing using DIRECTORY() auto-discovery
-- Upload any document to stage → automatically discovered and processed!
WITH stage_documents AS (
    SELECT 
        relative_path,
        file_url,
        last_modified,
        size
    FROM DIRECTORY('@{{ target.database }}.RAW.ACME_DOCUMENTS')
    WHERE (
        LOWER(relative_path) LIKE '%.pdf' OR 
        LOWER(relative_path) LIKE '%.docx' OR 
        LOWER(relative_path) LIKE '%.pptx' OR 
        LOWER(relative_path) LIKE '%.txt' OR
        LOWER(relative_path) LIKE '%.txt.gz'  -- Handle compressed text files too
    )
),

parsed_documents AS (
    SELECT
        sd.relative_path,
        sd.file_url,
        
        -- Smart title extraction from filename
        INITCAP(
            REPLACE(
                REPLACE(SPLIT_PART(sd.relative_path, '/', -1), '_', ' '),
                REGEXP_SUBSTR(SPLIT_PART(sd.relative_path, '/', -1), '\\.[^.]*$'), ''
            )
        ) AS title,
        
        -- Dynamic document type detection
        CASE
            WHEN LOWER(sd.relative_path) LIKE '%annual_report%' THEN 'annual_report'
            WHEN LOWER(sd.relative_path) LIKE '%safety%' OR LOWER(sd.relative_path) LIKE '%policy%' THEN 'policy'
            WHEN LOWER(sd.relative_path) LIKE '%manual%' OR LOWER(sd.relative_path) LIKE '%installation%' THEN 'manual'
            WHEN LOWER(sd.relative_path) LIKE '%training%' OR LOWER(sd.relative_path) LIKE '%guide%' THEN 'training'
            WHEN LOWER(sd.relative_path) LIKE '%service%' OR LOWER(sd.relative_path) LIKE '%standard%' THEN 'standards'
            ELSE 'document'
        END AS document_type,
        
        -- Extract year from filename
        COALESCE(
            REGEXP_SUBSTR(sd.relative_path, '20[0-9]{2}'),
            YEAR(CURRENT_DATE())::STRING
        ) AS document_year,
        
        -- AI_PARSE_DOCUMENT extraction
        AI_PARSE_DOCUMENT(
            TO_FILE('@{{ target.database }}.RAW.ACME_DOCUMENTS', sd.relative_path),
            {'mode': 'LAYOUT'}
        ) as parsed_result
        
    FROM stage_documents sd
)

SELECT
    relative_path,
    file_url,
    title,
    document_type,
    document_year,
    TO_VARCHAR(parsed_result:content) AS extracted_layout,
    parsed_result:metadata:pageCount::INT AS page_count,
    LENGTH(TO_VARCHAR(parsed_result:content)) AS content_length,
    TO_VARCHAR(parsed_result:content) AS content,
    CURRENT_TIMESTAMP() AS parsed_at
FROM parsed_documents
WHERE parsed_result:content IS NOT NULL
