"""Pydantic schemas for API requests/responses"""
from pydantic import BaseModel, EmailStr
from typing import List, Dict
from datetime import date, time


class BookingCreate(BaseModel):
    """Schema for creating a booking"""
    name: str
    email: EmailStr
    date: date 
    time: time  


class BookingResponse(BaseModel):
    """Schema for booking response"""
    id: int
    name: str
    email: str
    date: date
    time: time


class ChatRequest(BaseModel):
    """Schema for chat request"""
    session_id: str
    query: str


class ChatResponse(BaseModel):
    """Schema for chat response"""
    response: str
    history: List[Dict[str, str]] = []


class DocumentUploadResponse(BaseModel):
    """Schema for document upload response"""
    status: str
    filename: str
