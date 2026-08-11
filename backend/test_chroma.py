from app.services.pdf_service import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import store_chunks


document_id = "test-document-001"

filename = "Assignment No. 1 CA.pdf"

text = extract_text(
    "uploads/Assignment No. 1 CA.pdf"
)

chunks = chunk_text(text)

embeddings = generate_embeddings(chunks)

store_chunks(
    chunks,
    embeddings,
    document_id,
    filename
)

print("Stored", len(chunks), "chunks in ChromaDB")