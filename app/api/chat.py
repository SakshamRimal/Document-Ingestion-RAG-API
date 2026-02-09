"""Chat API for conversational RAG"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db import get_db
from app.db.schemas import ChatRequest, ChatResponse
from app.memory import add_to_memory, get_memory
from app.pinecone_db import get_vectorstore
from app.embeddings import get_embeddings
from app.llm_service import generate_rag_response, detect_booking_intent, generate_booking_confirmation
from app.db.crud import create_booking
from app.db.schemas import BookingCreate

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("/history/{session_id}")
def get_chat_history(session_id: str):
    """Get chat history for a session"""
    history = get_memory(session_id)
    return {"session_id": session_id, "history": history}


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """Handle chat with RAG and booking support"""
 
    booking_info = detect_booking_intent(request.query)
    
    if booking_info.is_booking_request:
    
        if not booking_info.name or not booking_info.date or not booking_info.time:
            return ChatResponse(
                response="I'd be happy to help you book an interview! Please provide your name, preferred date, and time.",
                history=get_memory(request.session_id)
            )
        
        # Create booking
        booking = BookingCreate(
            name=booking_info.name,
            email=booking_info.email or "pending@example.com",
            date=booking_info.date,
            time=booking_info.time
        )
        create_booking(db, booking)
        
        # Generate confirmation
        bot_response = generate_booking_confirmation(
            name=booking_info.name,
            date=booking_info.date,
            time=booking_info.time
        )
        
        add_to_memory(request.session_id, request.query, bot_response)
        return ChatResponse(response=bot_response, history=get_memory(request.session_id))
    
    # Regular RAG chat
    history = get_memory(request.session_id)
    
    # Get embeddings and search vectorstore
    embedding = get_embeddings()
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(request.query, k=3)
    context = " ".join([doc.page_content for doc in docs])
    
    # Generate response using LLM
    bot_response = generate_rag_response(request.query, context, history)
    
    add_to_memory(request.session_id, request.query, bot_response)
    
    return ChatResponse(response=bot_response, history=get_memory(request.session_id))
