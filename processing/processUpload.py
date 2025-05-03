import json, logging
from utils.schema_validator import is_valid_article
from utils.uploader import upload_article
from processing.transform import transform_article

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_articles(filepath: str, source: str):
    with open(filepath) as f:
        articles = json.load(f)

    seen_urls = set()
    failed_articles = []


    for article in articles:
        url = article.get("url")
        if not url or url in seen_urls:
            logger.warning(f"Skipping duplicate or missing URL: {url}")
            failed_articles.append(article)
            continue
        
        transformed = transform_article(article)
        if is_valid_article(transformed):
            upload_article(article, source)
        seen_urls.add(url)
        
    if failed_articles:
        logger.warning(f"{len(failed_articles)} article(s) failed during processing.")
        with open(f"failed_{source}.json", "w") as f:
            json.dump(failed_articles, f, indent=2)


if __name__ == "__main__":
    process_articles("output/articles_output.json", source="newsapi")