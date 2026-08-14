from groq import Groq

from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_answer(question: str, context: str):

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information provided
in the document context below.

Important rules:
1. Use the document context as the source of truth.
2. If the answer is explicitly stated or can be directly inferred
   from the context, answer the question.
3. Do not require the question to use the exact wording from the document.
4. Do not use your own outside knowledge.
5. If the context genuinely does not contain enough information,
   respond exactly:
   "I could not find the answer in the uploaded documents."
6. If the question asks for a list, functions, types, steps,
   advantages, disadvantages, or multiple points, include ALL
   relevant points available in the provided context.
Document context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content