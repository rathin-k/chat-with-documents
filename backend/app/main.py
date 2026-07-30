from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/")
def root():
    return {
        "upload_dir": settings.UPLOAD_DIR
    }