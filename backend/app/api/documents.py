from fastapi import APIRouter, Depends

from app.utils.dependencies import get_current_user
from app.database.mongodb import documents_collection


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.get("/")
def get_documents(
    current_user=Depends(get_current_user)
):

    user_id = current_user["sub"]

    documents = documents_collection.find(
        {
            "user_id": user_id
        },
        {
            "_id": 1,
            "filename": 1,
            "uploaded_at": 1
        }
    ).sort("uploaded_at", -1)

    result = []

    for document in documents:

        result.append({
            "document_id": str(document["_id"]),
            "filename": document["filename"],
            "uploaded_at": document["uploaded_at"]
        })

    return result