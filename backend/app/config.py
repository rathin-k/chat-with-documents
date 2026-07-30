from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URI = os.getenv("MONGODB_URI")
    JWT_SECRET = os.getenv("JWT_SECRET")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    UPLOAD_DIR = os.getenv("UPLOAD_DIR")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")

settings = Settings()