import boto3, hashlib, json, uuid
from datetime import datetime
from s3_botoConfig import get_s3_client
from typing import Union
import os

BUCKET = "bucket-byte8"
s3_client = get_s3_client()

def _generate_key(prefix: str, source: str, url: Union[str, None] = None) -> str:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    suffix = hashlib.md5(url.encode()).hexdigest() if url else str(uuid.uuid4())
    return f"{prefix}/{source}/{timestamp}/{suffix}.json"

def upload_article(article: dict, source: str, prefix: str = "validated"):
    """
    Generic upload. Caller chooses 'raw' or 'validated'.
    """
    url = article.get("url")
    key = _generate_key(prefix, source, url)
    s3_client.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(article),
        ContentType="application/json"
    )
    print(f"Uploaded to s3://{BUCKET}/{key}")

def upload_raw_file(filepath: str, source: str):
    """
    Batch upload of raw articles from a local JSON file.
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, "r") as f:
        articles = json.load(f)

    for article in articles:
        upload_article(article, source, prefix="raw")

    print(f"Uploaded {len(articles)} raw articles from {filepath}")
