from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional


class File(Document):
    name: str
    user: str
    type: str
    size: int
    s3_object: str
    metadata: Optional[dict] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "files"
        indexes = ["user", "created_at"]
