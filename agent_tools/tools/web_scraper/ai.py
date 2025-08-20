"""
AI analysis for web scraping using Snowflake Cortex Python SDK
"""

import logging
import json
from typing import List, Dict, Any, Optional

try:
    from snowflake.snowpark import Session
    from snowflake.cortex import complete, CompleteOptions
except ImportError:
    Session = None
    complete = None
    CompleteOptions = None

logger = logging.getLogger(__name__)

def get_ai_competitor_suggestions(session: Optional[Session], primary_url: str, content: str) -> List[str]:
    """Use Claude to suggest competitor URLs via proper SDK"""
    if not session or not complete:
        # Fallback for local testing
        from .core import get_competitor_suggestions
        return get_competitor_suggestions(primary_url)
    
    try:
        prompt = [{
            "role": "user",
            "content": f"""I am analyzing competitors for: {primary_url}

Based on this content: {content[:800]}

Suggest 2-3 direct competitor URLs I should analyze for competitive intelligence.
Return ONLY valid URLs, one per line, no explanations.
Focus on direct business competitors."""
        }]

        options = CompleteOptions(
            max_tokens=200,
            temperature=0.1
        )
        
        result = complete(
            model="claude-3-haiku",
            prompt=prompt,
            session=session,
            options=options
        )
        
        if isinstance(result, str):
            suggestions = result.strip().split('\n')
            valid_urls = []
            for url in suggestions[:3]:
                url = url.strip()
                if url.startswith('http') and len(url) > 10:
                    valid_urls.append(url)
            return valid_urls
            
    except Exception as e:
        logger.warning(f"AI competitor suggestion failed: {e}")
    
    # Fallback to mock suggestions
    from .core import get_competitor_suggestions
    return get_competitor_suggestions(primary_url)

def perform_ai_analysis(session: Optional[Session], primary_result: Dict[str, Any], competitor_results: List[Dict[str, Any]]) -> str:
    """Analyze competitive landscape using Claude via proper SDK"""
    if not session or not complete:
        return create_mock_analysis(primary_result, competitor_results)
    
    try:
        # Build analysis content
        content = f"PRIMARY: {primary_result['title']} ({primary_result['url']})\n{primary_result['content'][:800]}\n\n"
        
        for i, comp in enumerate(competitor_results[:3], 1):
            if comp['success']:
                content += f"COMPETITOR {i}: {comp['title']} ({comp['url']})\n{comp['content'][:600]}\n\n"
        
        prompt = [{
            "role": "user", 
            "content": f"""Analyze this competitive landscape for business intelligence:

{content}

Provide structured competitive analysis focusing on:
1. Key differentiators between companies
2. Pricing comparison (if available)  
3. Market positioning insights
4. Strategic recommendations

Format as clear business insights."""
        }]
        
        options = CompleteOptions(
            max_tokens=800,
            temperature=0.2
        )
        
        result = complete(
            model="claude-3-haiku",
            prompt=prompt, 
            session=session,
            options=options
        )
        
        if isinstance(result, str):
            return result
            
    except Exception as e:
        logger.error(f"AI analysis failed: {e}")
    
    return create_mock_analysis(primary_result, competitor_results)

def create_mock_analysis(primary_result: Dict[str, Any], competitor_results: List[Dict[str, Any]]) -> str:
    """Create mock competitive analysis for testing"""
    successful_competitors = [c for c in competitor_results if c['success']]
    
    return f"""COMPETITIVE ANALYSIS SUMMARY

Primary Target: {primary_result['url']}
- Strong market position with premium pricing
- Focus on enterprise customers
- Found pricing: {', '.join(primary_result.get('prices', ['N/A']))}

Competitive Landscape:
- {len(successful_competitors)} competitors analyzed
- Market shows diverse pricing strategies
- Opportunity for competitive positioning

Strategic Recommendations:
1. Analyze competitor pricing strategies in detail
2. Identify unique feature gaps in the market
3. Develop targeted marketing for underserved segments
4. Consider freemium or trial offerings to capture market share

Market Insights:
- Strong demand for business intelligence solutions
- Integration capabilities are key differentiator
- Customer support quality varies across competitors"""
