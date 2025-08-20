"""
Core web scraping functionality - clean and focused
"""

import logging
import time
from typing import Dict, Any, List
from urllib.parse import urlparse
import re

logger = logging.getLogger(__name__)

def validate_url(url: str) -> bool:
    """Validate URL format and security"""
    if not url or not isinstance(url, str):
        return False
    
    if not (url.startswith('http://') or url.startswith('https://')):
        return False
    
    parsed = urlparse(url)
    if not parsed.netloc:
        return False
    
    # Security: Block internal networks
    if parsed.hostname in ['localhost', '127.0.0.1'] or (parsed.hostname and parsed.hostname.startswith('192.168.')):
        logger.warning(f"Blocked internal URL: {url}")
        return False
    
    return True

def extract_prices_from_text(text: str) -> List[str]:
    """Extract price patterns from text for competitive analysis"""
    price_patterns = [
        r'\$[\d,]+\.?\d*',
        r'€[\d,]+\.?\d*', 
        r'£[\d,]+\.?\d*',
        r'USD\s*[\d,]+\.?\d*',
        r'EUR\s*[\d,]+\.?\d*'
    ]
    
    prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        prices.extend(matches[:3])  # Limit per pattern
    
    return list(set(prices))[:5]  # Remove duplicates, limit total

def create_mock_scrape_result(url: str) -> Dict[str, Any]:
    """Create realistic mock data for local testing"""
    domain = urlparse(url).netloc
    
    content = f"""
    Welcome to {domain} - Industry leader in business solutions.
    
    Our pricing tiers:
    - Starter Plan: $99/month
    - Professional: $299/month  
    - Enterprise: $599/month
    
    Key features:
    - Advanced analytics dashboard
    - 24/7 customer support
    - API integrations
    - Custom reporting
    - Real-time data sync
    
    Contact our sales team for competitive analysis and market insights.
    Over 10,000+ customers trust our platform for their business intelligence needs.
    """
    
    return {
        'success': True,
        'url': url,
        'title': f"Business Solutions - {domain}",
        'content': content,
        'prices': extract_prices_from_text(content),
        'scraped_at': time.strftime('%Y-%m-%dT%H:%M:%SZ')
    }

def get_competitor_suggestions(primary_url: str) -> List[str]:
    """Mock competitor suggestions for testing"""
    domain = urlparse(primary_url).netloc.replace('www.', '')
    base = domain.split('.')[0]
    
    return [
        f"https://competitor1-{base}.com",
        f"https://alternative-{base}.com", 
        f"https://{base}-rival.com"
    ]
