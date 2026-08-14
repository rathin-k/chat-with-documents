import chromadb

from app.config import settings

client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = client.get_or_create_collection(
    name="documents",
    metadata={
        "hnsw:space": "cosine"
    }
)

def search_chunks(
    query_embedding,
    user_id,
    n_results=5,
    similarity_threshold=0.30
):
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        where={
            "user_id": user_id
        },
        include=["documents", "metadatas", "distances"]
    )

    filtered_documents = []
    filtered_metadatas = []
    filtered_distances = []

    for i, distance in enumerate(results["distances"][0]):

        similarity = 1 - distance

        print(
           f"Result {i}: "
           f"chunk_index={results['metadatas'][0][i].get('chunk_index')} "
           f"distance={distance:.4f}, "
           f"similarity={similarity:.4f}"
        )

        if similarity >= similarity_threshold:
            filtered_documents.append(
                results["documents"][0][i]
            )

            filtered_metadatas.append(
                results["metadatas"][0][i]
            )

            filtered_distances.append(
                similarity
            )

    return {
        "documents": [filtered_documents],
        "metadatas": [filtered_metadatas],
        "distances": [filtered_distances]
    }

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