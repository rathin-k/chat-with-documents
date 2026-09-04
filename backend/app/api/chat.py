from fastapi import APIRouter, Depends
from uuid import uuid4
from datetime import datetime, timezone

from app.models.chat import ChatRequest
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import search_chunks
from app.api.auth import get_current_user
from app.services.llm_service import (
    generate_answer,
    rewrite_query
)

from app.database.mongodb import (
    conversations_collection,
    messages_collection
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/")
def chat(
    request: ChatRequest,
    current_user=Depends(get_current_user)
):

    user_id = current_user["sub"]

    # --------------------------------------------------
    # 1. Create or use conversation
    # --------------------------------------------------

    conversation_id = request.conversation_id

    if not conversation_id:

        conversation_id = str(uuid4())

        conversations_collection.insert_one({
            "conversation_id": conversation_id,
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc)
        })

    else:

        # Make sure conversation belongs to current user
        conversation = conversations_collection.find_one({
            "conversation_id": conversation_id,
            "user_id": user_id
        })

        if not conversation:
            return {
                "error": "Invalid conversation_id"
            }

    # --------------------------------------------------
    # 2. Get recent conversation history
    # --------------------------------------------------

    history_cursor = messages_collection.find(
        {
            "conversation_id": conversation_id,
            "user_id": user_id
        },
        {
            "_id": 0,
            "role": 1,
            "content": 1
        }
    ).sort("created_at", -1).limit(6)

    history = list(history_cursor)

    # Reverse so oldest message comes first
    history.reverse()

    # --------------------------------------------------
    # 3. Generate query embedding
    # --------------------------------------------------

    search_query = rewrite_query(
      request.question,
      history
    )

    print("Original question:", request.question)
    print("Search query:", search_query)
    
    query_embedding = generate_embeddings(
      [search_query]
    )[0]
    # --------------------------------------------------
    # 4. Search document chunks
    # --------------------------------------------------

    results = search_chunks(
        query_embedding,
        user_id,
        n_results=10,
        similarity_threshold=0.20
    )

    # --------------------------------------------------
    # 5. No relevant document found
    # --------------------------------------------------

    if not results["documents"][0]:

        answer = (
            "I could not find the answer in the uploaded documents."
        )

        # Save user message
        messages_collection.insert_one({
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": "user",
            "content": request.question,
            "created_at": datetime.now(timezone.utc)
        })

        # Save assistant message
        messages_collection.insert_one({
            "conversation_id": conversation_id,
            "user_id": user_id,
            "role": "assistant",
            "content": answer,
            "created_at": datetime.now(timezone.utc)
        })

        return {
            "question": request.question,
            "answer": answer,
            "sources": [],
            "conversation_id": conversation_id
        }

    # --------------------------------------------------
    # 6. Prepare sources
    # --------------------------------------------------

    sources = []

    for i, document in enumerate(results["documents"][0]):

        sources.append({
            "text": document,
            "metadata": results["metadatas"][0][i]
        })

    # --------------------------------------------------
    # 7. Prepare document context
    # --------------------------------------------------

    context = "\n\n".join(
        source["text"]
        for source in sources
    )

    # --------------------------------------------------
    # 8. Generate answer using document + history
    # --------------------------------------------------

    answer = generate_answer(
        request.question,
        context,
        history
    )

    # --------------------------------------------------
    # 9. Save user message
    # --------------------------------------------------

    messages_collection.insert_one({
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": "user",
        "content": request.question,
        "created_at": datetime.now(timezone.utc)
    })

    # --------------------------------------------------
    # 10. Save assistant message
    # --------------------------------------------------

    messages_collection.insert_one({
        "conversation_id": conversation_id,
        "user_id": user_id,
        "role": "assistant",
        "content": answer,
        "created_at": datetime.now(timezone.utc)
    })

    # --------------------------------------------------
    # 11. Return response
    # --------------------------------------------------

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources,
        "conversation_id": conversation_id
    }