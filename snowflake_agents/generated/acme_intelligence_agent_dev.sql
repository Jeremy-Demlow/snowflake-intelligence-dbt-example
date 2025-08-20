-- ACME Intelligence Agent - Generated from YAML Configuration
-- Scalable, maintainable agent deployment

CREATE OR REPLACE AGENT DEV_SNOWFLAKE_INTELLIGENCE.AGENTS.ACME_INTELLIGENCE_AGENT
WITH PROFILE = '{"display_name": "ACME Intelligence Agent"}'  
COMMENT = 'ACME Intelligence Agent for analyzing technician performance and business metrics'
FROM SPECIFICATION $${
  "models": {
    "orchestration": ""
  },
  "instructions": {
    "response": "You are a ACME business analyst with access to both operational and financial data,  plus company documents. Help users understand technician performance, analyze financial  metrics like NDR, and provide actionable insights.",
    "orchestration": "Use 'Query Operational Data' for questions about technicians, jobs, and operational revenue.  Use 'Query Financial Metrics' for NDR, ARR expansion, customer segments, and financial analytics.  Use 'Search Documents' for company policies and strategic context.",
    "sample_questions": [
      {
        "question": "What is our total job revenue so far this year?"
      },
      {
        "question": "Which technicians have an average rating below 3 stars?"
      },
      {
        "question": "What is the latest NDR across all customers?"
      },
      {
        "question": "What is the latest NDR for Enterprise segment customers?"
      },
      {
        "question": "Show me NDR trends by market segment over the last 6 months"
      },
      {
        "question": "Which customer segments have the highest ARR expansion?"
      },
      {
        "question": "What does our annual report say about customer trust?"
      }
    ]
  },
  "tools": [
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Operational Data",
        "description": "Analyze technician performance, job revenue, ratings, and operational business metrics"
      }
    },
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Financial Metrics",
        "description": "Analyze NDR, ARR expansion, customer segments, and financial performance metrics"
      }
    },
    {
      "tool_spec": {
        "type": "cortex_search",
        "name": "Search ACME Services Documents",
        "description": "Search company documents, annual reports, and policies for strategic context"
      }
    },
    {
      "tool_spec": {
        "type": "generic",
        "name": "Send_Email",
        "description": "Send emails to recipients with subject and HTML content. Always use HTML formatted content.",
        "input_schema": {
          "type": "object",
          "properties": {
            "recipient": {
              "description": "Email address of the recipient",
              "type": "string"
            },
            "subject": {
              "description": "Subject line of the email",
              "type": "string"
            },
            "text": {
              "description": "HTML content of the email",
              "type": "string"
            }
          },
          "required": [
            "recipient",
            "subject",
            "text"
          ]
        }
      }
    },
    {
      "tool_spec": {
        "type": "generic",
        "name": "Web_scrape",
        "description": "Scrape and analyze websites for competitive intelligence and market research",
        "input_schema": {
          "type": "object",
          "properties": {
            "url": {
              "description": "The URL of the website to scrape and analyze",
              "type": "string"
            }
          },
          "required": [
            "url"
          ]
        }
      }
    }
  ],
  "tool_resources": {
    "Query Operational Data": {
      "semantic_view": "ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE"
      }
    },
    "Query Financial Metrics": {
      "semantic_view": "ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_financial_analytics_view",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE"
      }
    },
    "Search ACME Services Documents": {
      "name": "ACME_INTELLIGENCE.SEARCH.acme_document_search",
      "max_results": 5,
      "title_column": "TITLE",
      "id_column": "RELATIVE_PATH"
    },
    "Send_Email": {
      "type": "procedure",
      "identifier": "AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL",
      "name": "SEND_MAIL(VARCHAR, VARCHAR, VARCHAR)",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE",
        "query_timeout": 0
      }
    },
    "Web_scrape": {
      "type": "procedure",
      "identifier": "AGENT_TOOLS_CENTRAL.AGENT_TOOLS.WEB_SCRAPE",
      "name": "WEB_SCRAPE(VARCHAR)",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE",
        "query_timeout": 0
      }
    }
  }
}$$;