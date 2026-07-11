import pytest
from s3_ingest.client import S3Client

def test_upload_retry(monkeypatch):
    client = S3Client()

    # Force upload_file to fail
    def fail_upload(*args, **kwargs):
        raise Exception("Simulated failure")

    monkeypatch.setattr(client.s3, "upload_file", fail_upload)

    result = client.upload_file("bucket","key","file.txt",retries=2)
    assert result is False