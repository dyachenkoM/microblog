from contextlib import asynccontextmanager
from typing import BinaryIO

from aiobotocore.session import get_session

from core.config import settings


class S3Client:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 endpoint_url: str,
                 bucket_name: str,
                 ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        self.access_key = access_key
        self.secret_key = secret_key
        self.endpoint_url = endpoint_url

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self,
                          file: BinaryIO,
                          name: str,
                          ):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=name,
                Body=file,
            )
        return f"{self.endpoint_url}/{self.bucket_name}/{name}"


s3_client = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.endpoint_url,
    bucket_name=settings.s3.bucket_name
)
