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

def normalize_date(published: str) -> str:
    try:
        dt = parser.parse(published)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    except Exception:
        return ""

def transform_article(article: Dict[str, Any]) -> Dict[str, Any]:
    transformed = {
        "title": clean_text(article.get("title", "")),
        "description": clean_text(article.get("description", "")),
        "content": clean_text(article.get("content", "")),
        "author": clean_text(article.get("author", "")),
        "source": article.get("source"),
        "source_name": article.get("source", {}).get("name") if isinstance(article.get("source"), dict) else article.get("source", ""),
        "url": article.get("url", ""),
        "published": normalize_date(article.get("published_at") or article.get("publishedAt", "")),
        "tags": article.get("tags", []),
        "images": article.get("images", []),
        "scraped_at": article.get("scraped_at", datetime.utcnow().isoformat()),
        "raw": article.get("raw", article)  # retaining the original for debugging/tracking
    }
    return transformed if transformed["url"] else None #Only return this article for further processing if it has a valid URL.