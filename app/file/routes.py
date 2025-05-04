from fastapi import APIRouter, UploadFile, HTTPException, Response, Form
import httpx
from urllib.parse import quote
from app.file.models import File
from app.file.utils import S3Client
from app.config import (
    aws_access_key,
    aws_secret_key,
    aws_endpoint,
    aws_bucket_name,
)

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    user: str = Form(...),
) -> dict:
    try:
        client = S3Client(
            access_key=aws_access_key,
            secret_key=aws_secret_key,
            endpoint_url=aws_endpoint,
            bucket_name=aws_bucket_name,
        )
        s3_object = await client.upload_file(file.file, file.filename)
        doc = File(
            name=file.filename,
            user=user,
            type=file.content_type,
            size=file.size,
            metadata=file.headers,
            s3_object=s3_object,
        )
        await doc.insert()
        return {"response": "File uploaded successfully", "id": str(doc.id)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dl/{file_id}")
async def download_file(file_id: str) -> Response:
    try:
        file = await File.get(file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        client = S3Client(
            access_key=aws_access_key,
            secret_key=aws_secret_key,
            endpoint_url=aws_endpoint,
            bucket_name=aws_bucket_name,
        )
        object_link = await client.download_file(file.s3_object)
        async with httpx.AsyncClient() as s3_client:
            s3_response = await s3_client.get(object_link)
            if s3_response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to download file")

            content = s3_response.content
            content_type = s3_response.headers.get(
                "Content-Type", "application/octet-stream"
            )
            content_disposition = f'attachment; filename="{quote(file.name)}"'

            return Response(
                content=content,
                media_type=content_type,
                headers={
                    "Content-Disposition": content_disposition,
                    "Content-Length": str(len(content)),
                },
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
