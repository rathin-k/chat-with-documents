from fastapi import APIRouter, Depends

from app.models.chat import ChatRequest
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import search_chunks
from app.api.auth import get_current_user
from app.services.llm_service import generate_answer

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user)
):

    query_embedding = generate_embeddings(
        [request.question]
    )[0]

    results = search_chunks(
      query_embedding,
      current_user["sub"],
      n_results=10,
      similarity_threshold=0.30
    )

    if not results["documents"][0]:
      return {
          "question": request.question,
          "answer": "I could not find the answer in the uploaded documents.",
          "sources": []
       }
    
    sources = []

    for i, document in enumerate(results["documents"][0]):

        sources.append({
            "text": document,
            "metadata": results["metadatas"][0][i]
        })

    context = "\n\n".join(
        source["text"]
        for source in sources
    )

    answer = generate_answer(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }