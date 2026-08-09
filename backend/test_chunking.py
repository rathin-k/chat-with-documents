from app.services.pdf_service import extract_text
from app.services.chunking_service import chunk_text


text = extract_text(
    "uploads/Assignment No. 1 CA.pdf"
)

chunks = chunk_text(text)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\n--------------------")
    print("CHUNK", i + 1)
    print("--------------------")
    print(chunk)