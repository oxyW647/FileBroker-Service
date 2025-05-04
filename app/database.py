from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.file.models import File
from app.config import database_url


async def init_db():
    client = AsyncIOMotorClient(database_url)
    database = client["file_storage"]
    await init_beanie(database, document_models=[File])
