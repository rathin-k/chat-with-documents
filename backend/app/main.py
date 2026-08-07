from fastapi import FastAPI

from app.config import settings
from app.api.database import router as database_router
from app.api.auth import router as auth_router
from app.api.upload import router as upload_router

app = FastAPI()

app.include_router(database_router)
app.include_router(auth_router)
app.include_router(upload_router)

@app.get("/")

def root():
    return {
        "upload_dir": settings.UPLOAD_DIR
    }


#.\venv\Scripts\Activate.ps1