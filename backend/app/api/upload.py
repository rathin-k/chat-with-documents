from fastapi import APIRouter, UploadFile, File, Depends

from app.utils.dependencies import get_current_user

from app.services.upload_service import save_file

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/")
def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user)
):
    saved_document = save_file(
       file,
       current_user["sub"]
    )

    return {
      "message": "File uploaded successfully",
      "document_id": saved_document["document_id"],
      "filename": file.filename,
      "user": current_user["email"]
    }