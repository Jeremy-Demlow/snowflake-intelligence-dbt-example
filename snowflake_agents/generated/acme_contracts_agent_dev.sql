-- ACME Contracts Intelligence Agent - Generated from YAML Configuration
-- Scalable, maintainable agent deployment

CREATE OR REPLACE AGENT DEV_SNOWFLAKE_INTELLIGENCE.AGENTS.ACME_CONTRACTS_AGENT
WITH PROFILE = '{"display_name": "ACME Contracts Intelligence Agent"}'  
COMMENT = 'Enterprise-grade agent for analyzing contract commitments, churn, invoice variance, and exit ramp risks with optimized performance'
FROM SPECIFICATION $${
  "models": {
    "orchestration": ""
  },
  "instructions": {
    "response": "Transform contract analysis into cohesive, actionable business insights with the following structure: 1. Begin with clear executive summary highlighting key contract health indicators and critical risks 2. Organize analysis into logical sections: Risk Assessment, Financial Impact Analysis, Strategic Recommendations 3. Convert raw contract metrics into complete business narratives with proper context and implications 4. Maintain data citations and confidence levels where appropriate to support decision-making 5. Eliminate technical jargon and focus on business implications that executives can act upon 6. Create natural flow between contract health metrics, financial risk indicators, and actionable next steps 7. Consolidate related contract performance data under strategic business themes (retention, growth, risk) 8. Use executive-level, decision-focused language throughout with clear prioritization of actions 9. Include brief risk summary with recommended immediate actions for leadership review and approval 10. Provide context on revenue impact, customer relationship implications, and competitive positioning 11. CREATE VISUALIZATIONS when contract analysis would benefit from charts or graphs - use plotting functionality for:\n    - Variance analysis (commitment vs. actual invoiced amounts by segment)\n    - Contract performance trends (fulfillment rates over time)\n    - Risk analysis charts (exit ramp accounts, churn probability)\n    - Revenue impact visualization (contract value distribution, at-risk revenue)\n    - Comparative analysis (account performance, segment comparisons)\n12. When creating plots for contract data, choose appropriate chart types: bar charts for variance analysis, line charts for performance trends, scatter plots for risk assessment, donut charts for portfolio composition 13. Always provide executive-ready chart titles, axis labels, and strategic annotations that directly support contract management decisions",
    "orchestration": "OVERALL: parallelize as many tool calls as possible for optimal latency and comprehensive analysis.  Use 'Query Contracts Analytics' for quantitative contract performance analysis including active  contracts, commitment tracking, churn analysis, invoice variance detection, and exit ramp risk  assessment. Simultaneously leverage 'Search ACME Documents' for policy context, contract terms,  and strategic business context when relevant. Always provide comprehensive business context about  what contract metrics mean for revenue risk, customer retention strategies, competitive positioning,  and strategic decision-making priorities.",
    "sample_questions": [
      {
        "question": "How many active contracts do we have and what's the revenue health status?"
      },
      {
        "question": "What's our total minimum commitment amount and how does it compare to actual performance?"
      },
      {
        "question": "How many clients have churned this period and what's the revenue impact?"
      },
      {
        "question": "What's the variance between our commitments and actual invoiced amounts by account segment?"
      },
      {
        "question": "Which accounts have exit ramp commitments and what's our retention strategy?"
      },
      {
        "question": "Show me active contracts by account with their commitment amounts and performance indicators"
      },
      {
        "question": "Which accounts are over-performing vs under-performing their commitments and why?"
      },
      {
        "question": "What's our churn rate, revenue at risk, and recommended intervention strategies?"
      },
      {
        "question": "Break down exit ramp commitments by account status and provide retention recommendations"
      },
      {
        "question": "Show me the top accounts by commitment value and their relationship health scores"
      },
      {
        "question": "Analyze commitment fulfillment trends and predict revenue risk for next quarter"
      },
      {
        "question": "Which product lines have the highest contract variance and what's driving it?"
      }
    ]
  },
  "tools": [
    {
      "tool_spec": {
        "type": "cortex_analyst_text_to_sql",
        "name": "Query Contracts Analytics",
        "description": "SEMANTIC VIEW: ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_semantic_view - Database: ACME_INTELLIGENCE, Schema: SEMANTIC_MODELS - Contains comprehensive contract performance data combining commitments with actual billing results - Serves as the primary source for contract health monitoring, churn analysis, and revenue risk assessment\nKEY METRICS AVAILABLE: - total_active_contracts: Current count of active contracts (baseline: 80 contracts) - total_min_commitment_sum: Total minimum commitment amount across all contracts ($254,046.71) - total_churned_clients: Count of churned contracts/clients (current: 6 clients) - total_commitment_variance: Variance between commitments and actual invoiced amounts - total_invoiced_amount: Actual invoiced/billed amount ($180,686.20)  - total_exit_ramp_commitment: At-risk revenue from exit ramp contracts ($27,357.61 across 21 accounts) - commitment_fulfillment_rate: Percentage of commitment fulfillment across accounts - over_committed_accounts: Accounts exceeding minimum commitments - under_committed_accounts: Accounts falling short of commitments - churn_rate: Percentage of contracts that have churned\nKEY DIMENSIONS AVAILABLE: - account_name, account_id: Customer account identification - contract_id, contract_status, contract_category: Contract management details - product_name, product_family: Product and service breakdown - billing_month, trans_date: Temporal analysis capabilities - exit_ramp_c: Exit ramp risk flag for retention focus - tenant_name, tenant_id: Multi-tenant analysis support\nBUSINESS PURPOSE: Monitor contract health, track churn risk, analyze commitment variance,  identify revenue opportunities, assess customer retention needs, and guide strategic account management decisions.\n"
      }
    },
    {
      "tool_spec": {
        "type": "cortex_search",
        "name": "Search ACME Documents",
        "description": "Search company documents for contract policies, terms, strategic context, and business intelligence with advanced relevance ranking"
      }
    },
    {
      "tool_spec": {
        "type": "generic",
        "name": "Send_Contract_Alert",
        "description": "Send strategic contract risk alerts and executive summaries via email with actionable insights. Always use HTML formatted content optimized for executive consumption.",
        "input_schema": {
          "type": "object",
          "properties": {
            "recipient": {
              "description": "Email address of the recipient (account manager, finance executive, customer success team, etc.)",
              "type": "string"
            },
            "subject": {
              "description": "Executive-focused subject line highlighting contract risk level, opportunity, or strategic action needed",
              "type": "string"
            },
            "text": {
              "description": "HTML content with structured contract analysis, prioritized risks, financial impact, and specific recommended actions with timelines",
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
    }
  ],
  "tool_resources": {
    "Query Contracts Analytics": {
      "semantic_view": "ACME_INTELLIGENCE.SEMANTIC_MODELS.acme_contracts_semantic_view",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE"
      }
    },
    "Search ACME Documents": {
      "name": "ACME_INTELLIGENCE.SEARCH.acme_document_search",
      "max_results": 10,
      "title_column": "TITLE",
      "id_column": "RELATIVE_PATH",
      "experimental": {
        "Diversity": {
          "GroupBy": [
            "DOCUMENT_TYPE"
          ],
          "MaxResults": 3
        },
        "RerankWeights": {
          "TopicalityMultiplier": 4,
          "EmbeddingMultiplier": 1.2,
          "RerankingMultiplier": 1.5,
          "RerankingDepth": 20
        },
        "RetrievalWeights": {
          "TopicalityMultiplier": 3,
          "BoostAndDecayDepth": 2000
        }
      }
    },
    "Send_Contract_Alert": {
      "type": "procedure",
      "identifier": "AGENT_TOOLS_CENTRAL.AGENT_TOOLS.SEND_MAIL",
      "name": "SEND_MAIL(VARCHAR, VARCHAR, VARCHAR)",
      "execution_environment": {
        "type": "warehouse",
        "warehouse": "HOL_WAREHOUSE",
        "query_timeout": 0
      }
    }
  }
}$$;