"""LLM service using Google Gemini Flash 2.5"""
import os
from typing import Optional, List
import google.generativeai as genai
from pydantic import BaseModel

# Load API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Configure Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class BookingInfo(BaseModel):
    """Booking information extracted from user message"""
    name: Optional[str] = None
    email: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    is_booking_request: bool = False


def get_llm():
    """Get LLM instance (Google Gemini Flash 2.5)"""
    if not GEMINI_API_KEY:
        return None
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_rag_response(query: str, context: str, chat_history: List[dict]) -> str:
    """Generate RAG response using LLM"""
    llm = get_llm()
    if not llm:
        # Fallback to simple response if no API key
        return f"Based on the documents: {context[:300]}..."
    
    # Build history context
    history_text = ""
    if chat_history:
        history_text = "\nPrevious conversation:\n"
        for msg in chat_history[-3:]:  # Last 3 exchanges
            history_text += f"User: {msg.get('user', '')}\nAssistant: {msg.get('bot', '')}\n"
    
    system_prompt = """You are a helpful assistant. Answer the user's question based on the provided context. 
    If the context doesn't contain the answer, say so clearly. Keep answers concise and helpful."""
    
    human_prompt = f"""Context:
{context}

{history_text}
User's question: {query}"""
    
    response = llm.generate_content(f"{system_prompt}\n\n{human_prompt}")
    return response.text


def detect_booking_intent(user_message: str) -> BookingInfo:
    """Detect if user wants to book an interview and extract info"""
    llm = get_llm()
    if not llm:
        # More strict keyword-based detection
        booking_keywords = ["i want to book", "book an interview", "schedule an interview", "book a meeting"]
        user_lower = user_message.lower().strip()
        
        # Check for explicit booking phrases
        if any(phrase in user_lower for phrase in booking_keywords):
            return BookingInfo(is_booking_request=True)
        
        # Check if message asks about booking/availability
        question_words = ["?", "when is", "available", "slots"]
        has_booking_word = any(kw in user_lower for kw in ["book", "schedule", "appointment"])
        has_question = any(q in user_lower for q in question_words[:2])
        
        if has_booking_word and has_question:
            return BookingInfo(is_booking_request=True)
        
        return BookingInfo()
    
    # Use LLM to detect booking intent
    prompt = """Analyze if the user wants to book an interview or meeting.

Look for explicit booking requests like:
- "I want to book an interview"
- "Schedule a meeting"
- "Book an appointment"
- "I need to set up a call"

Do NOT detect as booking if the user is just asking general questions about interviews, meetings, or scheduling in documents.

Respond with just "YES" if they want to book, or "NO" if they are asking a general question."""
    
    response = llm.generate_content(f"{prompt}\n\nUser message: {user_message}")
    result = response.text.strip().upper()
    
    if result == "YES":
        return BookingInfo(is_booking_request=True)
    
    return BookingInfo()


def generate_booking_confirmation(name: str, date: str, time: str) -> str:
    """Generate booking confirmation message"""
    return f"Great! I've scheduled your interview:\n\nName: {name}\nDate: {date}\nTime: {time}\n\nWe'll send a confirmation to your email."
