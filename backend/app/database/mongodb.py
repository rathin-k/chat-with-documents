from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGODB_URI)

db = client["chat_with_documents"]

#.\venv\Scripts\Activate.ps1