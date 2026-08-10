from app.services.pdf_service import extract_text
from app.services.chunking_service import chunk_text
from app.services.embedding_service import generate_embeddings


text = extract_text(
    "uploads/Assignment No. 1 CA.pdf"
)

chunks = chunk_text(text)

embeddings = generate_embeddings(chunks)

print("Number of chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)