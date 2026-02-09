from sqlalchemy import Column, Integer, String, Text, Date, Time
from app.core.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_name = Column(String)
    source = Column(String)
    chunk_text = Column(Text)
    chunk_index = Column(Integer)
    vector_id = Column(String)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    date = Column(Date, nullable=False)  # <- use Date type
    time = Column(Time, nullable=False)  # <- use Time type
