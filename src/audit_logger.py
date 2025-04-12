import logging
from datetime import datetime, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_audit(job_id, status, s3_path, error, start_time):
    end_time = datetime.now(timezone.utc)
    duration = (end_time - start_time).total_seconds()

    log_entry = {
        "job_id": job_id,
        "status": status,
        "s3_path": s3_path,
        "duration_seconds": duration,
        "error": error,
        "timestamp": end_time.isoformat()
    }

    logger.info(f"AUDIT_LOG: {log_entry}")
