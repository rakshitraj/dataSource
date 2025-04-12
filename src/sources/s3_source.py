import boto3
from botocore.exceptions import NoCredentialsError
from data_source import DataSource
from cryptography.fernet import Fernet
import json
from config import RDSConfigurationProvider
from typing import Generator


class S3FileFetcher(DataSource):
    def __init__(self, conn_conf, decryption_key):
        """
        Initialize the S3FileFetcher with an S3 client.
        :param config_path: Path to the AWS configuration file.
        :param decryption_key: Fernet decryption key to decrypt the configuration.
        """
        s3_client = self.get_s3_client(conn_conf, decryption_key)
        self.s3_client = self.get_s3_client()
        
    def get_s3_client(self, conn_conf, decryption_key):
        """
        Create and return an S3 client using credentials from the decrypted configuration.
        :param config_path: Path to the AWS configuration file.
        :param decryption_key: Fernet decryption key to decrypt the configuration.
        """

        # Read and decrypt the configuration file
        with open(conn_conf, 'rb') as file:
            encrypted_data = file.read()
        fernet = Fernet(decryption_key)
        decrypted_data = fernet.decrypt(encrypted_data)
        config = json.loads(decrypted_data)

        # Create and return the S3 client
        return boto3.client(
            's3',
            aws_access_key_id=config['aws_access_key'],
            aws_secret_access_key=config['aws_secret_key']
        )
    
    def data_filter(self, file_key) -> bool:
        """
        Determine whether a file should be fetched based on its key.
        :param file_key: The key of the S3 object.
        :return: True if the file should be fetched, False otherwise.
        """
        # Example logic: Fetch only files with a specific extension
        allowed_extensions = ['.txt', '.csv', '.json']
        return isinstance(file_key, str) and any(file_key.endswith(ext) for ext in allowed_extensions)
    
    def paginate_prefix(self, src_bucket, src_prefix=""):
        """
        Paginate through the files in an S3 bucket with an optional prefix.
        """
        paginator = self.s3_client.get_paginator('list_objects_v2')
        try:
            for page in paginator.paginate(Bucket=src_bucket, Prefix=src_prefix):
                if 'Contents' in page:
                    for obj in page['Contents']:
                        yield obj['Key']
        except NoCredentialsError:
            raise Exception("AWS credentials not found")
        except Exception as e:
            raise Exception(f"Failed to list files in S3 bucket: {e}")
        
    def format_data(self, data_object: any) -> any:
        return data_object

    def fetch_data(self, args) -> Generator[tuple[str, any], None, None]:
        """
        Fetch files from an S3 bucket that pass the file format check.
        The bucket name and prefix are retrieved from the ConfigurationProvider.
        :return: A generator yielding tuples with file keys and file contents.
        """
        config = RDSConfigurationProvider(pipeline_name=args.pipeline_id)

        # Source 
        src_bucket = config.get("src_bucket")
        src_prefix = config.get("src_prefix")

        try:
            # Paginate through the bucket
            for file_key in self.paginate_prefix(src_bucket, src_prefix):
                # Check if the file format is allowed
                if self.data_filter(file_key):
                    # Fetch the file content
                    response = self.s3_client.get_object(Bucket=src_bucket, Key=file_key)
                    yield file_key, self.format_data(response['Body'].read())
        except NoCredentialsError:
            raise Exception("AWS credentials not found")
        except Exception as e:
            raise Exception(f"Failed to fetch files from S3: {e}")
