import json
from utils.validator import is_valid_article
from utils.uploader import upload_article

def process_articles(filepath: str, source: str):
    with open(filepath) as f:
        articles = json.load(f)

    seen_urls = set()
    for article in articles:
        url = article.get("url")
        if not url or url in seen_urls:
            continue

        if is_valid_article(article):
            upload_article(article, source)
            seen_urls.add(url)

if __name__ == "__main__":
    process_articles("output/articles_output.json", source="newsapi")