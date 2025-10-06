{% macro create_acme_document_search() %}
  -- Standalone operation to create/update document search service
  -- Avoids post-hook connection issues while using your excellent macro design
  
  {% set search_table = target.database ~ '.SEARCH.search_documents' %}
  
  {{ create_cortex_search_service(
      service_name='acme_document_search',
      source_table=search_table,
      search_column='chunk',
      attributes='relative_path, file_url, title, document_type, document_year, language, content_length, page_count'
  ) }}
  
{% endmacro %}

{% macro refresh_all_search_services() %}
  -- Operation to refresh all search services
  {{ create_acme_document_search() }}
  
  -- Add more search services here as needed:
  -- {{ create_contract_search() }}
  -- {{ create_invoice_search() }}
  
{% endmacro %}
