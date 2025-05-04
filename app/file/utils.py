from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from uuid import uuid4


class S3Client:
    def __init__(
        self,
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

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file: bytes, filename: str):
        object_name = f"{uuid4()}_{filename}"
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )
            return object_name
        except Exception as e:
            raise Exception(f"Failed to upload file: {e}")

    async def download_file(self, object_name: str):
        try:
            async with self.get_client() as client:
                url = await client.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": object_name,
                    },
                    ExpiresIn=900,
                )
                return url
        except Exception as e:
            raise Exception(f"Failed to generate pre-signed URL: {e}")
