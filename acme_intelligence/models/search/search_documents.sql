{{
    config(
        materialized='table',
        schema='search',
        post_hook="{{ create_cortex_search_service(
            service_name='acme_document_search',
            source_table=this,
            search_column='chunk',
            attributes='relative_path, file_url, title, document_type, document_year, language, content_length, page_count'
        ) }}"
    )
}}

-- Step 3: Search Service Creation with Rich Metadata
-- Create Cortex Search service from chunked documents with full business context
-- Enables filtering by document_type, year, etc. and rich result presentation

SELECT
    chunk,                    -- Search column (chunked content)
    relative_path,           -- File identifier
    file_url,                -- Direct file access URL
    title,                   -- Human-readable document title
    document_type,           -- Business category (policy, manual, annual_report, etc.)
    document_year,           -- Document year for temporal filtering
    language,                -- Language for international filtering
    content_length,          -- Original document size
    page_count,              -- Number of pages
    content,                 -- Full original content for detailed results
    chunk_length,            -- Size of this specific chunk
    chunk_index             -- Position of chunk within document
FROM {{ ref('doc_chunks') }}
