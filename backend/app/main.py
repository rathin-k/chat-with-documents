from fastapi import FastAPI
from app.config import settings
from app.api.database import router as database_router

app = FastAPI()

app.include_router(database_router)

@app.get("/")
def root():
    return {
        "upload_dir": settings.UPLOAD_DIR
    }