import re
from datetime import datetime
from typing import Dict, Any
from dateutil import parser

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text)     # Collapse whitespace
    return text.strip()

def normalize_date(published_at: str) -> str:
    try:
        dt = parser.parse(published_at)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ""

def transform_article(article: Dict[str, Any]) -> Dict[str, Any]:
    transformed = {
        "title": clean_text(article.get("title", "")),
        "description": clean_text(article.get("description", "")),
        "content": clean_text(article.get("content", "")),
        "author": clean_text(article.get("author", "")),
        "source": article.get("source", {}).get("name") if isinstance(article.get("source"), dict) else article.get("source", ""),
        "url": article.get("url", ""),
        "published_at": normalize_date(article.get("published_at") or article.get("publishedAt", "")),
        "scraped_at": article.get("scraped_at", datetime.utcnow().isoformat()),
        "raw": article.get("raw", article)  # Keep the original for debugging/tracking
    }
    return transformed