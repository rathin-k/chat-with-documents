from groq import Groq

from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_answer(question: str, context: str):

    prompt = f"""
You are a helpful assistant that answers questions based only on
the provided document context.

If the answer cannot be found in the context, say:
"I could not find the answer in the uploaded documents."

Do not make up information.

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