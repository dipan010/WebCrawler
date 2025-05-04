import sys
from pathlib import Path

# Dynamically add the project root to sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import settings  

import json, logging
from utils.schema_validator import is_valid_article
from utils.uploader import upload_article
from transform import transform_article

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
        if not transformed:
            logger.warning(f"Transformation failed or missing URL: {article.get('title', 'Untitled')}")
            failed_articles.append(article)
            continue

        if is_valid_article(transformed):
            upload_article(transformed, source, prefix="validated")
        else:
            logger.warning(f"Article did not pass validation: {article.get('title', 'Untitled')}")
            failed_articles.append(article)

        seen_urls.add(url)
        
    if failed_articles:
        logger.warning(f"{len(failed_articles)} article(s) failed during processing.")
        failed_path = f"/app/output/failed_{source}.json"
        with open(f"failed_{source}.json", "w") as f:
            json.dump(failed_articles, f, indent=2)
        logger.info(f"Failed articles written to: {failed_path}")

if __name__ == "__main__":
    process_articles("output/articles_output.json", source="newsapi")