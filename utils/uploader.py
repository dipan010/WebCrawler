import boto3, hashlib, json
from datetime import datetime
import os
s3 = boto3.client("s3")
BUCKET = "bucket-byte8"

def hash_article(article: dict) -> str:
    return hashlib.md5(article["url"].encode()).hexdigest()

def upload_article(article: dict, source: str):
    hashed = hash_article(article)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    key = f"articles/{source}/{date}/{hashed}.json"

    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(article),
        ContentType="application/json"
    )
    print(f"Uploaded to s3://{BUCKET}/{key}")