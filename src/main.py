from abc import ABC, abstractmethod
from datetime import datetime, timezone
import uuid
import logging

from config import get_config
from audit_logger import log_audit
from s3_writer import write_to_s3
from sources.example_api import ExampleAPIClient
from data_source import DataSource

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_ingestion(source_client: DataSource):
    cfg = get_config()
    job_id = uuid.uuid4().hex
    start_time = datetime.now(timezone.utc)

    try:
        data = source_client.fetch_data()
        s3_path = write_to_s3(data, cfg["s3_bucket"])
        status = "success"
        error = None
    except Exception as e:
        s3_path = None
        status = "error"
        error = str(e)

    log_audit(
        job_id=job_id,
        status=status,
        s3_path=s3_path,
        error=error,
        start_time=start_time
    )

def handler():
    source = get_config()["source"]
    if source == "example_api":
        client = ExampleAPIClient()
    else:
        raise ValueError(f"Unsupported source: {source}")

    run_ingestion(client)

if __name__ == "__main__":
    handler()
