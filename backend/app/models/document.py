from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    document_id: str
    filename: str
    uploaded_at: datetime