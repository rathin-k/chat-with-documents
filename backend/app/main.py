from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router

from app.config import settings
from app.api.database import router as database_router
from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(database_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(documents_router)

@app.get("/")

def root():
    return {
        "upload_dir": settings.UPLOAD_DIR
    }


#.\venv\Scripts\Activate.ps1
#python -m uvicorn app.main:app --reload