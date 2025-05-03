import requests
import os, sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from crawlers.items import Item

API_KEY = "0500c2e672464d08b5db8d0348be270d"
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(query="supply chain OR logistics", page_size=20):
    params = {
        "q": query,
        "language": "en",
        "pageSize": page_size,
        "apiKey": API_KEY,
        "sortBy": "relevancy",
        "searchIn": "title,content",
        "from": "2025-01-01",
        "to": "2025-02-02"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    for article in data.get("articles", []):
        Item(
            url=article["url"],
            title=article["title"],
            author=article["author"],
            published=article["publishedAt"],
            content=article["content"],
            raw_html=str(article),
            scraped_at=datetime.utcnow().isoformat(),
            source=article["source"]["name"]
        )
    return article

if __name__ == "__main__":
    news = fetch_news()
    if not news:
        print("No articles returned.")
    else:
        print(f"\n {len(news)} articles fetched:\n")
        for i, art in enumerate(news, 1):
            print(f"{i}. {art['title']} — {art['url']}")