# Backend API

A FastAPI-based backend for document ingestion and conversational RAG with Gemini Flash 2.5.

## Features

- **Document Ingestion**: Upload PDF/TXT files, extract text, chunk with two strategies
- **Conversational RAG**: Multi-turn chat using Redis memory and Gemini Flash 2.5
- **Interview Booking**: LLM-powered booking detection and scheduling
- **Vector Storage**: Pinecone for document embeddings
- **Chat Memory**: Redis for conversation history

## Project Structure

```
app/
├── main.py              # FastAPI entry point
├── embeddings.py        # HuggingFace embeddings
├── ingestion.py        # Document processing
├── llm_service.py      # Gemini LLM integration
├── memory.py           # Redis chat memory
├── pinecone_db.py      # Vector storage
├── api/
│   ├── document.py     # /documents/ingest
│   ├── chat.py        # /chat (RAG + booking)
│   └── booking.py     # /booking
├── core/
│   ├── config.py      # API keys
│   └── database.py    # SQLAlchemy + Redis
└── db/
    ├── models.py      # SQL tables
    ├── schemas.py     # Pydantic models
    └── crud.py        # Database operations
```

## Installation

```bash
# Clone and enter directory
git clone <repository-url>
cd PalmMind

# Create virtual environment
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ragdb

# Redis
REDIS_URL=redis://localhost:6379/0

# Pinecone
PINECONE_API_KEY=your-pinecone-key
PINECONE_ENV=your-region

# Gemini (for LLM features)
GEMINI_API_KEY=your-gemini-api-key
```

Get Gemini API key: https://aistudio.google.com/app/apikey

## Run Server

```bash
uvicorn app.main:app --reload
```

API docs: http://localhost:8000/docs
