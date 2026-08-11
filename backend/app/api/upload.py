from fastapi import APIRouter, UploadFile, File, Depends

from app.utils.dependencies import get_current_user

from app.services.upload_service import save_file

from app.services.pdf_service import extract_text

from app.services.chunking_service import chunk_text

from app.services.embedding_service import generate_embeddings

from app.services.vector_service import store_chunks

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

    chunks = chunk_text(text)

    embeddings = generate_embeddings(chunks)

    store_chunks(
     chunks,
     embeddings,
     saved_document["document_id"],
     file.filename
    )
    
    return {
      "message": "File uploaded and processed successfully",
      "document_id": saved_document["document_id"],
      "filename": file.filename,
      "user": current_user["email"],
      "chunk_count": len(chunks)
    }