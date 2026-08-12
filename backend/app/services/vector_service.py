import chromadb

from app.config import settings

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="documents"
)

def search_chunks(
    query_embedding,
    user_id,
    n_results=3
):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        where={
            "user_id": user_id
        }
    )

    return results

def store_chunks(
    chunks,
    embeddings,
    document_id,
    filename,
    user_id
):

    ids = [
        f"{document_id}_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
       {
         "user_id": user_id,
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