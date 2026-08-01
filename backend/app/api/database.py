from fastapi import APIRouter
from app.database.mongodb import db

router = APIRouter()

@router.get("/db-test")
def db_test():
    return {
        "database": db.name,
        "status": "Connected"
    }