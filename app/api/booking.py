"""Booking API"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db, schemas, crud

router = APIRouter(tags=["Booking"])


@router.post("/", response_model=schemas.BookingResponse)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking"""
    return crud.create_booking(db, booking)
