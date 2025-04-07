import boto3
import json
from datetime import datetime

def write_to_s3(data, bucket):
    s3 = boto3.client('s3')
    now = datetime.utcnow()
    key = f"api-data/{now:%Y/%m/%d/%H}/data.json"

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )
    return f"s3://{bucket}/{key}"
