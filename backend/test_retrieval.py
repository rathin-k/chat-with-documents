from app.services.embedding_service import generate_embeddings
from app.services.vector_service import collection


query = "How do I find an element in a rotated sorted array?"

query_embedding = generate_embeddings([query])[0]


results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)


print("Retrieved chunks:")

for i, document in enumerate(results["documents"][0]):
    print("\n--------------------")
    print(f"Result {i + 1}")
    print("--------------------")
    print(document)

    print("\nMetadata:")
    print(results["metadatas"][0][i])