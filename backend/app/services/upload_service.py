import os
import shutil
from datetime import datetime

from fastapi import UploadFile

from app.database.mongodb import documents_collection

from app.config import settings

def save_file(file: UploadFile, user_id: str):

    file_path = os.path.join(
      settings.UPLOAD_DIR,
      file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
          file.file,
          buffer
        )

    document = {
      "user_id": user_id,
      "filename": file.filename,
      "filepath": file_path,
      "uploaded_at": datetime.utcnow()
    }

    result = documents_collection.insert_one(document)
    
    return {
     "document_id": str(result.inserted_id),
     "filepath": file_path
    }