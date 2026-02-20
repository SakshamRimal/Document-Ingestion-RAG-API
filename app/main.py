"""Main FastAPI application"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import chat, booking, document
from app.core.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PalmMind Document Ingestion & RAG API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(document.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(booking.router, prefix="/booking", tags=["Booking"])


@app.get("/")
def read_root():
    """Root endpoint - serve UI"""
    from fastapi.responses import FileResponse
    return FileResponse("app/static/index.html")


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
