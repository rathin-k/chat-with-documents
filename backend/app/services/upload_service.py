import os
import shutil
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from app.database.mongodb import documents_collection
from app.config import settings


def save_file(file: UploadFile, user_id: str):

    original_filename = Path(file.filename).name

    unique_filename = f"{uuid.uuid4()}_{original_filename}"

    file_path = os.path.join(
        settings.UPLOAD_DIR,
        unique_filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = {
        "user_id": user_id,
        "filename": original_filename,
        "filepath": file_path,
        "uploaded_at": datetime.now(timezone.utc)
    }

    result = documents_collection.insert_one(document)

    return {
        "document_id": str(result.inserted_id),
        "filepath": file_path
    }