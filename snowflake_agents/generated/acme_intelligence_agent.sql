-- ACME Intelligence Agent - Generated from YAML Configuration
-- Scalable, maintainable agent deployment

CREATE OR REPLACE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.ACME_INTELLIGENCE_AGENT
WITH PROFILE = '{"display_name": "ACME Intelligence Agent"}'  
COMMENT = 'Enterprise-grade comprehensive business intelligence agent for operational, financial, and contracts analysis with optimized performance'
FROM SPECIFICATION $${
  "models": {
    "orchestration": ""
  },
  "instructions": {
    "response": "Transform business intelligence analysis into cohesive, executive-ready insights with the following structure: 1. Begin with clear executive dashboard summary highlighting key performance indicators and critical alerts 2. Organize analysis into strategic sections: Operational Performance, Financial Health, Contract Status, Strategic Recommendations 3. Convert technical metrics into complete business narratives with strategic context and competitive implications 4. Maintain data citations and trend analysis to support strategic decision-making processes 5. Eliminate operational jargon and focus on business outcomes that drive competitive advantage 6. Create natural flow between operational efficiency, financial performance, contract health, and growth opportunities 7. Consolidate related performance indicators under strategic business themes (growth, efficiency, risk, opportunity) 8. Use C-level executive language throughout with clear prioritization of strategic initiatives 9. Include comprehensive business health summary with recommended strategic actions and resource allocation 10. Provide context on market positioning, operational excellence, financial stability, and strategic growth vectors 11. CREATE VISUALIZATIONS when data analysis would benefit from charts or graphs - use plotting functionality for:\n    - Trend analysis (time series data, performance over time)\n    - Comparative analysis (segment performance, variance analysis)\n    - Distribution analysis (customer segments, revenue distribution)\n    - Performance dashboards (KPI tracking, variance from targets)\n    - Risk visualization (churn analysis, performance outliers)\n12. When creating plots, choose the most appropriate chart type: line charts for trends, bar charts for comparisons, scatter plots for relationships, pie charts for distributions 13. Always provide executive-ready chart titles, axis labels, and contextual annotations that support business decision-making",
    "orchestration": "OVERALL: parallelize as many tool calls as possible for optimal latency and comprehensive business intelligence.  Use 'Query Operational Data' for technician performance, job revenue, service quality, and operational efficiency metrics.  Simultaneously use 'Query Financial Metrics' for NDR analysis, ARR expansion, customer segmentation, and financial performance trends.  Concurrently leverage 'Query Contracts Data' for contract health, commitment tracking, churn analysis, and revenue risk assessment.  Use 'Search Documents' for strategic context, policy guidance, and competitive intelligence. Always provide comprehensive  business context that connects operational performance to financial outcomes and strategic positioning.",
    "sample_questions": [
      {
        "question": "What is our comprehensive business health across operations, finance, and contracts?"
      },
      {
        "question": "Which technicians are underperforming and what's the revenue impact?"
      },
      {
        "question": "What is the latest NDR performance and how does it correlate with operational efficiency?"
      },
      {
        "question": "Show me NDR trends by market segment with operational performance context over the last 6 months"
      },
      {
        "question": "Which customer segments have the highest ARR expansion potential and operational capacity?"
      },
      {
        "question": "How many active contracts do we have and how does this align with our service capacity?"
      },
      {
        "question": "What's our total minimum commitment amount versus our operational delivery capability?"
      },
      {
        "question": "Which accounts have exit ramp commitments and what operational interventions can we deploy?"
      },
      {
        "question": "Show me commitment variance by account with technician performance correlations"
      },
      {
        "question": "How many clients have churned and what were the operational warning signals?"
      },
      {
        "question": "What does our annual report say about customer trust and how does it align with our metrics?"
      },
      {
        "question": "Analyze the relationship between technician ratings, contract performance, and financial outcomes"
      },
      {
        "question": "Which geographic regions show the best operational-financial performance correlation?"
      },
      {
        "question": "What's driving contract variance and how can operational excellence improve retention?"
      }
    ]
  },
  "tools": [
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Operational Data",
        "description": "SEMANTIC VIEW: ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_analytics_view - Database: ACME_INTELLIGENCE, Schema: SEMANTIC_MODELS - Contains comprehensive technician performance and operational efficiency metrics - Serves as primary source for service quality monitoring, revenue per technician, and operational excellence tracking\nKEY OPERATIONAL METRICS: - total_jobs: Service job volume and capacity utilization - completed_jobs: Service delivery completion rates and efficiency - total_revenue: Operational revenue generation by technician and service type - revenue_2025: Current year operational performance tracking - avg_job_revenue: Service pricing and value delivery metrics - avg_rating: Customer satisfaction and service quality indicators - positive_reviews: Service quality excellence tracking - negative_reviews: Service improvement opportunity identification - technician_performance: Individual and team operational efficiency\nBUSINESS PURPOSE: Monitor operational excellence, optimize service delivery, track revenue per service unit, identify training needs, guide capacity planning, and ensure customer satisfaction alignment with financial performance.\n"
      }
    },
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Financial Metrics",
        "description": "SEMANTIC VIEW: ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_financial_analytics_view - Database: ACME_INTELLIGENCE, Schema: SEMANTIC_MODELS - Contains comprehensive NDR, ARR expansion, and customer segmentation financial performance data - Serves as primary source for financial health monitoring, growth tracking, and strategic financial planning\nKEY FINANCIAL METRICS: - ndr_percentage: Net Dollar Retention performance and customer expansion tracking - total_current_arr: Annual Recurring Revenue current state and growth trajectory - total_arr_expansion: Revenue expansion opportunities and customer growth potential   - avg_arr_per_account: Customer value optimization and account expansion metrics - customer_segment_performance: Market segment profitability and growth analysis - expansion_opportunities: Revenue growth identification and prioritization\nBUSINESS PURPOSE: Monitor financial health, track revenue expansion, analyze customer value creation, guide pricing strategies, identify growth opportunities, and ensure sustainable financial performance.\n"
      }
    },
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Contracts Data",
        "description": "SEMANTIC VIEW: ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_analytics_view - Database: ACME_INTELLIGENCE, Schema: SEMANTIC_MODELS - Contains comprehensive contract performance, commitment tracking, and revenue risk assessment data - Serves as primary source for contract health monitoring, churn prevention, and revenue assurance\nKEY CONTRACT METRICS: - total_active_contracts: Active contract portfolio health (80 contracts) - total_min_commitment_sum: Total commitment value and revenue security ($254K) - total_churned_clients: Customer retention performance (6 churned clients) - commitment_variance: Contract performance vs expectations analysis - total_exit_ramp_commitment: Revenue at risk identification ($27K at-risk) - contract_health_indicators: Early warning systems for contract issues\nBUSINESS PURPOSE: Monitor contract portfolio health, prevent customer churn, ensure revenue realization, identify expansion opportunities, guide customer success strategies, and optimize contract terms for mutual value.\n"
      }
    },
    {
      "tool_spec": {
        "type": "cortex_search",
        "name": "Search ACME Services Documents",
        "description": "Search company documents, strategic reports, policies, and competitive intelligence with advanced relevance optimization for executive insights"
      }
    },
    {
      "tool_spec": {
        "type": "generic",
        "name": "Send_Email",
        "description": "Send strategic business intelligence summaries and executive reports via email. Always use HTML formatted content optimized for C-level consumption with actionable insights.",
        "input_schema": {
          "type": "object",
          "properties": {
            "recipient": {
              "description": "Email address of the recipient (C-level executive, business unit leader, strategic stakeholder)",
              "type": "string"
            },
            "subject": {
              "description": "Executive-focused subject line highlighting business performance, strategic opportunities, or critical actions needed",
              "type": "string"
            },
            "text": {
              "description": "HTML content with comprehensive business intelligence dashboard, strategic insights, prioritized recommendations, and specific action items with business impact",
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
        "description": "Scrape and analyze websites for competitive intelligence, market research, and strategic positioning analysis with business context integration",
        "input_schema": {
          "type": "object",
          "properties": {
            "url": {
              "description": "The URL of the website to scrape and analyze for competitive intelligence, market trends, or strategic insights",
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
    "Query Contracts Data": {
      "semantic_view": "ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_analytics_view",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE"
      }
    },
    "Search ACME Services Documents": {
      "name": "ACME_INTELLIGENCE.SEARCH.acme_document_search",
      "max_results": 10,
      "title_column": "TITLE",
      "id_column": "RELATIVE_PATH",
      "experimental": {
        "Diversity": {
          "GroupBy": [
            "DOCUMENT_TYPE",
            "BUSINESS_AREA"
          ],
          "MaxResults": 2
        },
        "RerankWeights": {
          "TopicalityMultiplier": 5,
          "EmbeddingMultiplier": 1.3,
          "RerankingMultiplier": 1.6,
          "RerankingDepth": 25
        },
        "RetrievalWeights": {
          "TopicalityMultiplier": 4,
          "BoostAndDecayDepth": 3000
        }
      }
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