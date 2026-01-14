"""
Chat Router - Main chat API endpoint
Handles user chat messages and RAG responses
"""

import logging
import time
import uuid
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.rag_service import get_rag_service, RAGService
from app.models.database import Conversation, Message, Feedback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["Chat"])


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=500, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Jam besuk ICU jam berapa?",
                "session_id": None
            }
        }


class SourceInfo(BaseModel):
    """Source reference information"""
    document: str
    title: Optional[str] = None
    page: Optional[int] = None
    similarity: float


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str
    intent: str
    confidence: float = 0.0
    sources: List[SourceInfo] = []
    session_id: str
    message_id: Optional[int] = None
    response_time_ms: int
    registration_link: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Jam besuk ICU adalah pukul 11.00-12.00 dan 17.00-18.00 setiap hari.",
                "intent": "FAQ_QUERY",
                "confidence": 0.92,
                "sources": [],
                "session_id": "abc123",
                "message_id": 1,
                "response_time_ms": 1500
            }
        }


class FeedbackRequest(BaseModel):
    """Request model for feedback endpoint"""
    message_id: int = Field(..., description="ID of the message to provide feedback for")
    rating: int = Field(..., ge=-1, le=1, description="Rating: 1=positive, -1=negative")
    comment: Optional[str] = Field(None, max_length=500, description="Optional feedback comment")


class FeedbackResponse(BaseModel):
    """Response model for feedback endpoint"""
    status: str
    message: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint for user queries.
    
    Processes user message through RAG pipeline and returns AI-generated response.
    """
    start_time = time.time()
    
    try:
        # Validate message
        if len(request.message.strip()) < 2:
            raise HTTPException(
                status_code=400, 
                detail="Pesan terlalu pendek. Mohon berikan pertanyaan yang lebih jelas."
            )
        
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get or create conversation
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            conversation = Conversation(
                session_id=session_id,
                user_id=request.user_id
            )
            db.add(conversation)
            db.flush()
        else:
            conversation.last_activity = datetime.utcnow()
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.flush()
        
        # Process through RAG
        rag_service = get_rag_service()
        result = rag_service.process_query(
            db=db,
            user_message=request.message,
            session_id=session_id
        )
        
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # Save assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=result.response,
            intent=result.intent,
            confidence=result.confidence,
            response_time_ms=response_time_ms,
            extra_data={"sources": result.sources}
        )
        db.add(assistant_message)
        db.commit()
        
        # Format sources for response
        sources = [
            SourceInfo(
                document=s.get("document", "Unknown"),
                title=s.get("title"),
                page=s.get("page"),
                similarity=s.get("similarity", 0.0)
            )
            for s in result.sources
        ]
        
        logger.info(f"Chat response generated in {response_time_ms}ms (intent: {result.intent})")
        
        return ChatResponse(
            response=result.response,
            intent=result.intent,
            confidence=result.confidence,
            sources=sources,
            session_id=session_id,
            message_id=assistant_message.id,
            response_time_ms=response_time_ms,
            registration_link=result.registration_link
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat error: {str(e)}", exc_info=True)
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Silakan coba lagi."
        )


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    request: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for a chat response.
    
    Allows users to rate responses as positive (1) or negative (-1).
    """
    try:
        # Verify message exists
        message = db.query(Message).filter(Message.id == request.message_id).first()
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        # Check if feedback already exists
        existing = db.query(Feedback).filter(
            Feedback.message_id == request.message_id
        ).first()
        
        if existing:
            # Update existing feedback
            existing.rating = request.rating
            existing.comment = request.comment
            existing.submitted_at = datetime.utcnow()
        else:
            # Create new feedback
            feedback = Feedback(
                message_id=request.message_id,
                rating=request.rating,
                comment=request.comment
            )
            db.add(feedback)
        
        db.commit()
        
        rating_text = "positif" if request.rating > 0 else "negatif"
        logger.info(f"Feedback received for message {request.message_id}: {rating_text}")
        
        return FeedbackResponse(
            status="success",
            message=f"Terima kasih atas feedback {rating_text} Anda!"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Gagal menyimpan feedback")


@router.get("/conversation/{session_id}")
async def get_conversation_history(
    session_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get conversation history for a session.
    """
    conversation = db.query(Conversation).filter(
        Conversation.session_id == session_id
    ).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Session not found")
    
    messages = db.query(Message).filter(
        Message.conversation_id == conversation.id
    ).order_by(Message.timestamp.desc()).limit(limit).all()
    
    return {
        "session_id": session_id,
        "message_count": len(messages),
        "messages": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "intent": m.intent,
                "timestamp": m.timestamp.isoformat()
            }
            for m in reversed(messages)
        ]
    }
