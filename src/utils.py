import argparse

def argumentparser():
    parser = argparse.ArgumentParser(description="Parse command-line arguments.")
    parser.add_argument('--pipeline_id', type=str, help='Unique Pipeline ID')
    parser.add_argument('--job_id', type=str, help='Job ID')
    parser.add_argument('--run_id', type=str, help='Run ID')
    parser.add_argument('--conn_conf', type=str, help='Encrypted connection configuration')
    parser.add_argument('--private_key', type=str, help='Fernet Decryption keys')
    parser.add_argument('--source', type=str, help='Source layer')
    parser.add_argument('--target', type=str, help='target layer')
    # Debug flags - must have defaults
    parser.add_argument('--debug_flag', type=bool, help='True if the process is run in debug mode', default=False)

    return parser