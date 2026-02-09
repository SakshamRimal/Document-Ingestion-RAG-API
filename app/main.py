"""Main FastAPI application"""
from fastapi import FastAPI
from app.api import chat, booking, document
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PalmMind Document Ingestion & RAG API")

# Include routers
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])


@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "PalmMind API is running!"}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
