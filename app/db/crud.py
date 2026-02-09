"""Database CRUD operations"""
from sqlalchemy.orm import Session
from app.db import models, schemas


def save_chunk(
    db: Session,
    document_name: str,
    source: str,
    chunk_text: str,
    chunk_index: int,
    vector_id: str
) -> None:
    """Save a document chunk to the database"""
    chunk = models.DocumentChunk(
        document_name=document_name,
        source=source,
        chunk_text=chunk_text,
        chunk_index=chunk_index,
        vector_id=vector_id
    )
    db.add(chunk)
    db.commit()


def create_booking(db: Session, booking: schemas.BookingCreate) -> models.Booking:
    """Create a new booking"""
    db_booking = models.Booking(
        name=booking.name,
        email=booking.email,
        date=booking.date,
        time=booking.time
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
