"""
Database models for Ngoerah Smart Assistant
Using SQLAlchemy ORM with pgvector support
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base
from pgvector.sqlalchemy import Vector
import uuid

Base = declarative_base()


class Conversation(Base):
    """Tracks chat sessions"""
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    extra_data = Column(JSONB, nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(session_id={self.session_id})>"


class Message(Base):
    """Individual messages in a conversation"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    intent = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, nullable=True)
    extra_data = Column(JSONB, nullable=True)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    feedback = relationship("Feedback", back_populates="message", uselist=False)
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role})>"


class Document(Base):
    """Uploaded documents for RAG"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    document_type = Column(String(50), nullable=True)  # 'pedoman', 'sop', 'pengumuman'
    upload_date = Column(DateTime, default=datetime.utcnow)
    uploaded_by = Column(String(100), nullable=True)
    file_size_kb = Column(Integer, nullable=True)
    page_count = Column(Integer, nullable=True)
    status = Column(String(20), default='processing')  # 'processing', 'ready', 'error'
    extra_data = Column(JSONB, nullable=True)
    
    # Relationships
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename})>"


class DocumentChunk(Base):
    """Document chunks with embeddings for vector search"""
    __tablename__ = "document_chunks"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(384), nullable=True)  # Dimension for all-MiniLM-L6-v2
    page_number = Column(Integer, nullable=True)
    extra_data = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    document = relationship("Document", back_populates="chunks")
    
    def __repr__(self):
        return f"<DocumentChunk(id={self.id}, document_id={self.document_id})>"


class Feedback(Base):
    """User feedback for messages"""
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey("messages.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 = positive, -1 = negative
    comment = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    message = relationship("Message", back_populates="feedback")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, rating={self.rating})>"


class AnalyticsDaily(Base):
    """Daily aggregated analytics"""
    __tablename__ = "analytics_daily"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False, unique=True)
    total_queries = Column(Integer, default=0)
    avg_response_time_ms = Column(Integer, nullable=True)
    positive_feedback = Column(Integer, default=0)
    negative_feedback = Column(Integer, default=0)
    unique_users = Column(Integer, default=0)
    top_intents = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<AnalyticsDaily(date={self.date})>"
