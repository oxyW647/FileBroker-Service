from fastapi import FastAPI
from app.database import init_db
from app.file.routes import router as file_router

app = FastAPI()

app.include_router(file_router, prefix="/file", tags=["files"])


@app.on_event("startup")
async def startup():
    await init_db()
