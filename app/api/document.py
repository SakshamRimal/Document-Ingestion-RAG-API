"""Document Ingestion API"""
from fastapi import APIRouter, UploadFile, Depends, HTTPException
import shutil
import os
from sqlalchemy.orm import Session
from app.ingestion import ingest_document
from app.core.database import get_db
from app.db.schemas import DocumentUploadResponse
from app.db.crud import get_all_chunks

router = APIRouter(tags=["Documents"])

ALLOWED_EXTENSIONS = {".pdf", ".txt"}


def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS


@router.post("/ingest", response_model=DocumentUploadResponse)
def ingest_document_endpoint(
    file: UploadFile,
    chunk_strategy: str = "recursive",
    db: Session = Depends(get_db)
):
    """Upload and ingest a document (PDF or TXT)"""
    # Check file extension
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Only .pdf and .txt files are allowed"
        )
    
    file_path = f"data/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        ingest_document(file_path, chunk_strategy, db)
        return DocumentUploadResponse(
            status="Document ingested successfully",
            filename=file.filename
        )
    except Exception as e:
        # Clean up file on error
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list")
def list_documents(db: Session = Depends(get_db)):
    """List all ingested documents"""
    chunks = get_all_chunks(db)
    documents = {}
    for chunk in chunks:
        doc_name = chunk.document_name
        if doc_name not in documents:
            documents[doc_name] = {
                "name": doc_name,
                "chunks": 0,
                "vector_ids": []
            }
        documents[doc_name]["chunks"] += 1
        documents[doc_name]["vector_ids"].append(chunk.vector_id)
    return {"documents": list(documents.values())}


@router.get("/count")
def get_document_count(db: Session = Depends(get_db)):
    """Get total document count"""
    chunks = get_all_chunks(db)
    return {
        "total_chunks": len(chunks),
        "unique_documents": len(set(c.document_name for c in chunks))
    }
