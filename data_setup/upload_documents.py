#!/usr/bin/env python3
"""
Upload business documents to Snowflake stage for dbt-native parsing
"""

import os
import logging
from pathlib import Path
from snowflake_connection import SnowflakeConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def upload_documents_to_stage():
    """Upload all business documents to Snowflake stage"""
    
    # Connect to Snowflake
    logger.info("Connecting to Snowflake...")
    conn = SnowflakeConnection.from_snow_cli()
    
    try:
        # Create the stage if it doesn't exist
        logger.info("Creating ACME_DOCUMENTS stage...")
        stage_sql = """
        CREATE STAGE IF NOT EXISTS ACME_INTELLIGENCE.RAW.ACME_DOCUMENTS
        FILE_FORMAT = (
            TYPE = 'CSV'
            FIELD_DELIMITER = NONE
            RECORD_DELIMITER = NONE
            SKIP_HEADER = 0
        )
        COMMENT = 'Stage for ACME Services business documents';
        """
        conn.execute(stage_sql)
        logger.info("✅ Stage created successfully")
        
        # Get list of document files
        documents_dir = Path(__file__).parent / 'documents'
        if not documents_dir.exists():
            logger.error(f"Documents directory not found: {documents_dir}")
            return
            
        document_files = list(documents_dir.glob('*.txt'))
        logger.info(f"Found {len(document_files)} document files to upload")
        
        # Upload each document
        for doc_file in document_files:
            logger.info(f"Uploading {doc_file.name}...")
            
            # Use PUT command to upload file to stage
            put_sql = f"""
            PUT 'file://{doc_file.absolute()}' 
            @ACME_INTELLIGENCE.RAW.ACME_DOCUMENTS
            OVERWRITE = TRUE;
            """
            
            result = conn.execute(put_sql)
            logger.info(f"✅ Uploaded {doc_file.name}")
            
        # Verify uploads
        logger.info("Verifying uploaded files...")
        list_sql = "LIST @ACME_INTELLIGENCE.RAW.ACME_DOCUMENTS;"
        files = conn.execute(list_sql).fetchall()
        
        logger.info(f"📁 Stage contains {len(files)} files:")
        for file_info in files:
            file_name = file_info[0].split('/')[-1]  # Extract filename from full path
            file_size = file_info[1]  # File size in bytes
            logger.info(f"  • {file_name} ({file_size} bytes)")
            
        logger.info("🎉 Document upload completed successfully!")
        
        # Provide next steps
        logger.info("\n" + "="*60)
        logger.info("NEXT STEPS:")
        logger.info("1. Run: dbt run --select stg_parsed_documents")
        logger.info("2. This will parse all documents and create/update the search service")
        logger.info("3. Documents will be automatically indexed for search")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Error uploading documents: {e}")
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    upload_documents_to_stage()
