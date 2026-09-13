# Chat with Documents

A full-stack RAG (Retrieval-Augmented Generation) application that allows users to upload PDF documents and interact with them using natural-language questions.

The application retrieves relevant information from uploaded documents and uses an LLM to generate answers based on the retrieved context.

## Features

- User registration and login
- JWT-based authentication
- Secure user-specific document access
- PDF document upload
- PDF text extraction
- Text chunking
- Semantic search using embeddings
- Vector storage using ChromaDB
- Retrieval-Augmented Generation (RAG)
- Conversational chat with follow-up questions
- Conversation history
- Create new conversations
- Load previous conversations
- Conversation titles generated from the first question
- Document deletion
- Source documents displayed with answers
- Markdown-formatted AI responses
- User-scoped document retrieval

## Tech Stack

### Frontend

- React
- React Router
- Axios
- Tailwind CSS
- React Markdown

### Backend

- Python
- FastAPI
- PyMongo
- PyMuPDF
- Sentence Transformers
- ChromaDB
- Groq API
- JWT Authentication
- Pydantic

### Database

- MongoDB - users, documents, conversations and messages
- ChromaDB - document embeddings and semantic search

## System Architecture

```text
                    ┌──────────────────┐
                    │     React UI     │
                    │   Tailwind CSS   │
                    └────────┬─────────┘
                             │
                         HTTP / Axios
                             │
                             ▼
                    ┌──────────────────┐
                    │     FastAPI      │
                    │     Backend      │
                    └────────┬─────────┘
                             │
             ┌───────────────┼────────────────┐
             │               │                │
             ▼               ▼                ▼
        ┌─────────┐    ┌───────────┐    ┌──────────┐
        │ MongoDB │    │ ChromaDB  │    │  Groq    │
        │         │    │           │    │   LLM    │
        └─────────┘    └───────────┘    └──────────┘

RAG Pipeline

When a user uploads a PDF:

PDF Upload
    ↓
Save PDF
    ↓
Extract Text
    ↓
Split Text into Chunks
    ↓
Generate Embeddings
    ↓
Store Embeddings in ChromaDB

When a user asks a question:

User Question
    ↓
Conversation History
    ↓
Query Rewriting
    ↓
Generate Query Embedding
    ↓
Semantic Search in ChromaDB
    ↓
Retrieve Relevant Chunks
    ↓
Build Document Context
    ↓
Send Context + Question + History to LLM
    ↓
Generate Answer
    ↓
Return Answer + Sources
Authentication Flow

The application uses JWT-based authentication.

User
 ↓
Signup
 ↓
Password Hashing
 ↓
MongoDB

For login:

User Login
 ↓
Verify Credentials
 ↓
Generate JWT
 ↓
Frontend Stores Token
 ↓
Token Sent with API Requests
 ↓
FastAPI Validates Token

Protected resources such as documents and conversations are associated with the authenticated user's ID.

Conversation Management

Each chat session has a unique conversation ID.

The application supports:

Creating a new conversation
Continuing an existing conversation
Loading previous conversations
Loading messages from a conversation
Using previous messages for contextual follow-up questions

Example:

User: What is multiprogramming?

AI: Multiprogramming keeps multiple jobs in memory...

User: What are its benefits?

AI: The system understands "its" refers to multiprogramming.
Document Sources

For each generated answer, the application can display the documents from which the relevant information was retrieved.

This provides transparency about the source of the generated answer.

Project Structure

chat-with-documents/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── database.py
│   │   │   ├── documents.py
│   │   │   └── upload.py
│   │   │
│   │   ├── database/
│   │   │   └── mongodb.py
│   │   │
│   │   ├── models/
│   │   │   ├── chat.py
│   │   │   ├── document.py
│   │   │   └── user.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── chunking_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── pdf_service.py
│   │   │   ├── upload_service.py
│   │   │   └── vector_service.py
│   │   │
│   │   ├── utils/
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   │
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js
│   │   ├── assets/
│   │   │   ├── hero.png
│   │   │   ├── react.svg
│   │   │   └── vite.svg
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx
│   │   │   ├── ProtectedRoute.jsx
│   │   │   └── Sidebar.jsx
│   │   ├── pages/
│   │   │   ├── Chat.jsx
│   │   │   ├── Login.jsx
│   │   │   └── Signup.jsx
│   │   ├── App.css
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── .gitignore
│   ├── eslint.config.js
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── README.md
└── .gitignore

Running the Project Locally

1. Clone the repository
git clone <your-repository-url>
cd chat-with-documents

2. Backend Setup

Navigate to the backend:

cd backend

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

MONGODB_URL=your_mongodb_connection_string
GROQ_API_KEY=your_groq_api_key
JWT_SECRET_KEY=your_secret_key

Start the FastAPI server:

uvicorn app.main:app --reload

The backend will run on:

http://127.0.0.1:8000

FastAPI Swagger documentation:

http://127.0.0.1:8000/docs

3. Frontend Setup

Open another terminal:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will run on:

http://localhost:5173

Environment Variables

Do not commit API keys, passwords, or database credentials to GitHub.

Example:

MONGODB_URL=
GROQ_API_KEY=
JWT_SECRET_KEY=

The actual .env file should remain in .gitignore.

Future Improvements

Possible future improvements include:

Streaming LLM responses
Better document previews
Page-level source citations
Improved error handling
File size and upload validation
Rate limiting
Production deployment
More advanced retrieval strategies
Reranking retrieved chunks
Support for additional document formats
Automated tests
Production logging and monitoring
Learning Goals

This project was built to understand and implement:

REST APIs
FastAPI
JWT authentication
MongoDB
Vector databases
Embeddings
Semantic search
RAG architecture
LLM integration
Query rewriting
Conversational memory
React frontend-backend integration
Tailwind CSS