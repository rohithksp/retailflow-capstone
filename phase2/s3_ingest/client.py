import boto3
import logging
import time
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class S3Client:
    def __init__(self, profile="default", region="us-east-1"):
        session = boto3.Session(profile_name=profile, region_name=region)
        self.s3 = session.client("s3")

    def upload_file(self, bucket, key, local_path, retries=3):
        attempt = 0
        while attempt < retries:
            try:
                self.s3.upload_file(local_path, bucket, key)
                logger.info(f"Uploaded {local_path} to s3://{bucket}/{key}")
                return True
            except (ClientError, FileNotFoundError) as e:
                wait = 2 ** attempt
                logger.warning(f"Upload failed (attempt {attempt+1}), retrying in {wait}s...")
                time.sleep(wait)
                attempt += 1
        logger.error(f"Failed to upload {local_path} after {retries} retries")
        return False

    def list_objects(self, bucket, prefix=""):
        try:
            response = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
            return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError as e:
            logger.error(f"List failed: {e}")
            return []

    def download_file(self, bucket, key, local_path):
        try:
            self.s3.download_file(bucket, key, local_path)
            logger.info(f"Downloaded s3://{bucket}/{key} to {local_path}")
        except ClientError as e:
            logger.error(f"Download failed: {e}")

    def generate_presigned_url(self, bucket, key, expiry=3600):
        try:
            url = self.s3.generate_presigned_url("get_object",
                                                 Params={"Bucket": bucket, "Key": key},
                                                 ExpiresIn=expiry)
            logger.info(f"Presigned URL generated for s3://{bucket}/{key}")
            return url
        except ClientError as e:
            logger.error(f"Presigned URL failed: {e}")
            return None
