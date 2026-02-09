"""API routers"""
from app.api.document import router as document_router
from app.api.chat import router as chat_router
from app.api.booking import router as booking_router

__all__ = ["document_router", "chat_router", "booking_router"]
