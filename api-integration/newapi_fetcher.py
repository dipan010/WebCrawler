import requests
import os
from datetime import datetime
# from crawlers.items import Item

API_KEY = os.getenv("NEWSAPI_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def fetch_news(query="supply chain OR logistics", page_size = 20):
    # items = Item()
    params = {
        "q"          : query,
        "language"  : "en",
        "pageSize"  : page_size,
        "apiKey"    : API_KEY,
        "sortBy"    : "relevancy, publishedAt",
        "searchIn"  : "title,content",
        "from"      : "2025-01-01",
        "to"        : "2025-02-02"
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
    print(data)
    articles = []
    print("Status Code:", response.status_code)
    print("Response JSON keys:", data.keys())
    print("Total Results:", data.get("totalResults"))

    for article in data.get("articles",[]):
        articles.append({
            "source"        : article["source"],
            "title"         : article["title"],
            "author"        : article["author"],
            "description"   : article["description"],
            "url"           : article["url"],
            "published_at"  : article["publishedAt"],
            "content"       : article["content"],
            "raw"           : article,
            "scraped_at"    : datetime.utcnow().isoformat()
        })
    return articles

if __name__ == "__main__":
    news = fetch_news()
    if not news:
        print("No articles returned.")
    else:
        print(f"\n{len(news)} articles fetched:\n")
        for i, art in enumerate(news, 1):
            print(f"{i}. {art['title']} — {art['url']}")