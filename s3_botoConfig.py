import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

# Load from .env if available
load_dotenv()

proxy_definitions = {
    'http': os.getenv("PROXY_HTTP"),
    'https': os.getenv("PROXY_HTTPS")
}

# Boto3 configuration with fallback to default profile
def get_s3_client():
    my_config = Config(
        region_name=os.getenv("AWS_REGION"),
        signature_version='s3v4',
        proxies=proxy_definitions
    )

    # Checking if AWS credentials are present in env, else rely on profile
    if all([
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY")
    ]):
        return boto3.client(
            's3',
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN", None),
            config=my_config
        )
    else:
        # Fallback to AWS CLI profile or IAM role
        session = boto3.Session(profile_name=os.getenv("AWS_PROFILE", "default"))
        return session.client('s3', config=my_config)
