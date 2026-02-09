"""Document Ingestion API"""
from fastapi import APIRouter, UploadFile, Depends, HTTPException
import shutil
import os
from sqlalchemy.orm import Session
from app.ingestion import ingest_document
from app.core.database import get_db
from app.db.schemas import DocumentUploadResponse

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
