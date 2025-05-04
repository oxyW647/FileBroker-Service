from pydantic import BaseModel
from typing import Optional


class CreateFile(BaseModel):
    name: str
    user: str
    type: str
    size: int
    s3_object: str
    metadata: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "example.txt",
                "user": "user123",
                "type": "text/plain",
                "size": 1024,
                "s3_object": "s3://bucket-name/example.txt",
                "metadata": {
                    "description": "This is an example file",
                    "tags": ["example", "test"],
                },
            }
        }
