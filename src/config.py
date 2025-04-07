import os

def get_config():
    return {
        "api_url": os.getenv("API_URL", "https://jsonplaceholder.typicode.com/posts"),
        "api_key": os.getenv("API_KEY", ""),
        "s3_bucket": os.getenv("S3_BUCKET", "my-bucket"),
        "source": os.getenv("SOURCE", "example_api")
    }
