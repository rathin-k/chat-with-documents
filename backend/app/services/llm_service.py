from groq import Groq

from app.config import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def generate_answer(
    question: str,
    context: str,
    history: list
):

    history_text = ""

    if history:

        for message in history:

            role = message["role"]
            content = message["content"]

            history_text += (
                f"{role}: {content}\n"
            )

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question using ONLY the information
provided in the document context below.

Important rules:

1. Use the document context as the source of truth.
2. If the answer is explicitly stated or can be directly
   inferred from the document context, answer the question.
3. Previous conversation is provided only to understand
   references such as "it", "its", "they", etc.
4. Do not use previous conversation as a source of factual
   information if that information is not present in the
   current document context.
5. Do not use your own outside knowledge.
6. Do not require the question to use the exact wording
   from the document.
7. If the context genuinely does not contain enough
   information, respond exactly:
   "I could not find the answer in the uploaded documents."

Formatting rules:
- Use Markdown for formatting.
- Use **bold** for important terms when useful.
- Use Markdown headings when appropriate.
- Use Markdown bullet points or numbered lists when appropriate.
- Use Markdown tables when a comparison is clearer as a table.
- Do NOT use HTML tags such as <br>, <p>, <div>, <strong>, etc.
- Do not include raw HTML in your answer.
- Keep the answer clear and easy to read.

Previous conversation:
{history_text}

Document context:
{context}

Question:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def rewrite_query(question: str, history: list):
    
    history_text = ""

    for message in history:
        history_text += (
            f"{message['role']}: {message['content']}\n"
        )

    prompt = f"""
You are a query rewriting assistant for a document question-answering system.

Your task is to rewrite the user's current question into a
standalone, natural-language search query for semantic document retrieval.

Use the previous conversation ONLY to resolve references such as:
- it
- its
- they
- this
- that
- first
- second
- third
- first one
- second one
- previous function
- next point

Important rules:

1. Do NOT answer the question.
2. Return ONLY the rewritten standalone search query.
3. Preserve the user's original intent.
4. Preserve important concepts and terminology from the user's question.
5. Prefer a complete natural-language question instead of a short keyword phrase.
6. Do not unnecessarily shorten the question.
7. Resolve pronouns and references using the conversation history.
8. If the question is already clear and standalone, return it with minimal changes.
9. Do not introduce information that is not supported by the conversation.

Examples:

Conversation:
user: What is a process?
assistant: A process is a program under execution.

Current question:
What are its states?

Good rewritten query:
What are the states of a process?

---

Conversation:
user: What is a semaphore?
assistant: A semaphore is a synchronization method.

Current question:
What are its types?

Good rewritten query:
What are the types of a semaphore?

---

Conversation:
user: What are the disadvantages of Mutex/Locks?
assistant: 1. Contention
2. Deadlocks
3. Debugging
4. Starvation of high priority threads.

Current question:
Explain the second one.

Good rewritten query:
Explain the second disadvantage of Mutex/Locks, Deadlocks.

---

Previous conversation:
{history_text}

Current question:
{question}

Return ONLY the rewritten standalone search query.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()