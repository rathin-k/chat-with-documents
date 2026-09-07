import os

from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId

from app.utils.dependencies import get_current_user
from app.database.mongodb import documents_collection
from app.services.vector_service import delete_document_chunks


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


@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    current_user=Depends(get_current_user)
):

    user_id = current_user["sub"]

    # Find the document and verify ownership
    try:
        document = documents_collection.find_one({
            "_id": ObjectId(document_id),
            "user_id": user_id
        })
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid document ID"
        )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # Delete PDF file
    if os.path.exists(document["filepath"]):
        os.remove(document["filepath"])

    # Delete ChromaDB chunks
    delete_document_chunks(
        document_id,
        user_id
    )

    # Delete MongoDB record
    documents_collection.delete_one({
        "_id": ObjectId(document_id),
        "user_id": user_id
    })

    return {
        "message": "Document deleted successfully"
    }