# PalmMind Backend API

This project is a backend system built with FastAPI that provides:

1. **Document Ingestion API**
   - Upload `.pdf` or `.txt` files.
   - Extract text from documents.
   - Chunk documents with selectable strategies.
   - Generate embeddings and store them in vector databases (Pinecone, Qdrant, Weaviate, or Milvus).
   - Store document metadata in SQL/NoSQL database.

2. **Conversational RAG API**
   - Multi-turn chatbot using Redis for memory.
   - Handles custom queries and responses.
   - Supports **interview booking** with fields: name, email, date, and time.
   - Stores booking information in the database.

## Features

- Modular and clean code structure.
- Uses SQLAlchemy for database management.
- Pydantic schemas for request and response validation.
- Redis integration for chat memory.

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd PalmMind


Create and activate virtual environment:

python -m venv myenv
source myenv/bin/activate  # Linux/Mac
myenv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Run the server:

uvicorn main:app --reload

Usage

Access the API at http://127.0.0.1:8000/

Document ingestion: POST /documents/upload

Chat endpoint: POST /chat/

Booking endpoint: POST /chat/booking

License

This project is open-source and free to use.
```
