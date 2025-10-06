{{
    config(
        materialized='table',
        schema='search'
    )
}}

-- Step 2: Document Chunking with Rich Metadata
-- Split AI-parsed documents into optimal chunks while preserving business metadata
SELECT
    spd.relative_path,
    spd.file_url,
    spd.title,
    spd.document_type,
    spd.document_year,
    spd.content_length,
    spd.page_count,
    spd.content,  -- Original full content
    
    -- Chunked content for search optimization
    (
        spd.title || ':\n'
        || COALESCE('Section: ' || c.value['headers']['header_1'] || '\n', '')
        || COALESCE('Subsection: ' || c.value['headers']['header_2'] || '\n', '')
        || c.value['chunk']
    ) AS chunk,
    
    'English' AS language,
    LENGTH(c.value['chunk']) AS chunk_length,
    c.index AS chunk_index
    
FROM
    {{ ref('stg_parsed_documents') }} spd,
    LATERAL FLATTEN(
        SNOWFLAKE.CORTEX.SPLIT_TEXT_MARKDOWN_HEADER(
            spd.EXTRACTED_LAYOUT,
            OBJECT_CONSTRUCT('#', 'header_1', '##', 'header_2'),
            2000, -- chunks of 2000 characters (tutorial recommendation)
            300   -- 300 character overlap (tutorial recommendation)
        )
    ) c
