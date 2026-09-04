from pymongo import MongoClient
from app.config import settings


client = MongoClient(settings.MONGODB_URI)

db = client["chat_with_documents"]

users_collection = db["users"]
documents_collection = db["documents"]

conversations_collection = db["conversations"]
messages_collection = db["messages"]