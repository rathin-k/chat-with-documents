from fastapi import APIRouter, UploadFile, File, Depends

from app.utils.dependencies import get_current_user

from app.services.upload_service import save_file

from app.services.pdf_service import extract_text

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

    text = extract_text(
      saved_document["filepath"]
    )  

    return {
      "message": "File uploaded and processed successfully",
      "document_id": saved_document["document_id"],
      "filename": file.filename,
      "user": current_user["email"],
      "text": text
    }