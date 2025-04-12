from abc import ABC, abstractmethod
from datetime import datetime, timezone
import uuid
import logging

from utils import argumentparser

from config import RDSConfigurationProvider
from audit_logger import log_audit
from s3_writer import write_to_s3
from data_source import DataSource

from sources.example_api import ExampleAPIClient
from sources.s3_source import S3FileFetcher


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_ingestion(source_client: DataSource, args):

    cfg = RDSConfigurationProvider(pipeline_name=args.pipeline_id)
    job_id = args.job_id
    start_time = datetime.now(timezone.utc)

    try:
        s3_path = None
        for file_key, file_obj in source_client.fetch_data(config=cfg):
            s3_path = write_to_s3(file_obj, cfg.get("target_bucket"), metadata={"file_key": file_key})
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
    args = argumentparser()

    source = args.source
    if source == "example_api":
        client = ExampleAPIClient(args.conn_conf, args.private_key)
    elif source == 's3':
        client = S3FileFetcher(args.conn_conf, args.private_key)
    else:
        raise ValueError(f"Unsupported source: {source}")

    run_ingestion(client, args)

if __name__ == "__main__":
    handler()
