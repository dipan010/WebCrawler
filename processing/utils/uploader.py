import boto3, hashlib, json, uuid
from datetime import datetime
from s3_botoConfig import get_s3_client
from utils.schema_validator import is_valid_article
import os

BUCKET = "bucket-byte8"
s3_client = get_s3_client()

def hash_article(article: dict) -> str:
    return hashlib.md5(article["url"].encode()).hexdigest()

def upload_article(article: dict, source: str):
    """
    Uploads an article to S3 in either raw/ or processed/ based on `is_raw`.
    """
    timestamp = datetime.utcnow().strftime("%Y-%m-%d")
    folder = "processed" if is_valid_article(article) else "raw"
    key = f"{folder}/{source}/{timestamp}/{uuid.uuid4()}.json"

    s3_client.put_object(
        Bucket  =BUCKET,
        Key     =key,
        Body    =json.dumps(article),
        ContentType ="application/json"
    )
    print(f"Uploaded to s3://{BUCKET}/{key}")