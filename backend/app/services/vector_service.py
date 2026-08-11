import chromadb

from app.config import settings

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="documents"
)

def store_chunks(
    chunks,
    embeddings,
    document_id,
    filename
):

    ids = [
        f"{document_id}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
      {
         "document_id": document_id,
         "filename": filename,
         "chunk_index": i
      }
      for i in range(len(chunks))
    ]

    collection.add(
      ids=ids,
      documents=chunks,
      embeddings=embeddings.tolist(),
      metadatas=metadatas
    )