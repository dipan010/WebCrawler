import boto3, hashlib, json
from datetime import datetime
from s3_botoConfig import get_s3_client
import os

BUCKET = "bucket-byte8"
s3_client = get_s3_client()

def hash_article(article: dict) -> str:
    return hashlib.md5(article["url"].encode()).hexdigest()

def upload_article(article: dict, source: str, is_raw: bool = False):
    """
    Uploads an article to S3 in either raw/ or processed/ based on `is_raw`.
    """
    hashed = hash_article(article)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")

    folder = "raw" if is_raw else "processed"
    key = f"{folder}/{source}/{timestamp}/{hashed}.json"

    s3_client.put_object(
        Bucket  =BUCKET,
        Key     =key,
        Body    =json.dumps(article),
        ContentType ="application/json"
    )
    print(f"Uploaded to s3://{BUCKET}/{key}")