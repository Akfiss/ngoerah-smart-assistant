"""
Documents Router - Document management API endpoints  
Handles document upload, processing, and listing
"""

import logging
import os
from typing import Optional, List
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.document_service import get_document_processor, DocumentProcessor
from app.services.embedding_service import get_embedding_service, EmbeddingService
from app.models.database import Document, DocumentChunk

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/documents", tags=["Documents"])


# =============================================================================
# RESPONSE MODELS
# =============================================================================

class DocumentInfo(BaseModel):
    """Document information model"""
    id: int
    filename: str
    title: Optional[str]
    document_type: Optional[str]
    status: str
    page_count: Optional[int]
    chunk_count: int
    upload_date: datetime

    class Config:
        from_attributes = True


class UploadResponse(BaseModel):
    """Response for document upload"""
    status: str
    document_id: int
    filename: str
    message: str
    chunks_created: int


class ProcessingStatus(BaseModel):
    """Document processing status"""
    document_id: int
    filename: str
    status: str
    chunks_processed: int
    total_chunks: Optional[int]


# =============================================================================
# BACKGROUND TASKS
# =============================================================================

def process_document_background(
    document_id: int,
    file_path: str,
    db_url: str
):
    """Background task to process uploaded document"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(db_url)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        # Get document
        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            logger.error(f"Document {document_id} not found for processing")
            return
        
        logger.info(f"Processing document {document_id}: {document.filename}")
        
        # Process document
        doc_processor = get_document_processor()
        result = doc_processor.process_document(file_path, document.title)
        
        # Update document
        document.content = result['content']
        document.page_count = result['page_count']
        
        # Create embeddings and chunks
        embedding_service = get_embedding_service()
        
        for chunk_data in result['chunks']:
            # Generate embedding
            embedding = embedding_service.embed_text(chunk_data['content'])
            
            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=chunk_data['chunk_index'],
                content=chunk_data['content'],
                embedding=embedding,
                page_number=chunk_data.get('page_number'),
                metadata={'word_count': chunk_data.get('word_count')}
            )
            db.add(chunk)
        
        document.status = 'ready'
        db.commit()
        
        logger.info(f"Document {document_id} processed: {len(result['chunks'])} chunks created")
        
    except Exception as e:
        logger.error(f"Error processing document {document_id}: {str(e)}")
        document = db.query(Document).filter(Document.id == document_id).first()
        if document:
            document.status = 'error'
            document.metadata = {'error': str(e)}
            db.commit()
    finally:
        db.close()


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    document_type: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF document for RAG processing.
    
    The document will be processed in the background:
    1. Text extraction from PDF
    2. Text cleaning and chunking
    3. Embedding generation for each chunk
    """
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    try:
        # Read file content
        content = await file.read()
        file_size_kb = len(content) // 1024
        
        # Save file
        doc_processor = get_document_processor()
        file_path = doc_processor.save_uploaded_file(content, file.filename)
        
        # Create document record
        document = Document(
            filename=file.filename,
            title=title or file.filename.replace('.pdf', ''),
            document_type=document_type,
            file_size_kb=file_size_kb,
            status='processing'
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        
        # Get database URL for background task
        from app.config import settings
        
        # Schedule background processing
        background_tasks.add_task(
            process_document_background,
            document.id,
            file_path,
            settings.DATABASE_URL
        )
        
        logger.info(f"Document uploaded: {file.filename} (ID: {document.id})")
        
        return UploadResponse(
            status="processing",
            document_id=document.id,
            filename=file.filename,
            message="Document uploaded and queued for processing",
            chunks_created=0
        )
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/", response_model=List[DocumentInfo])
async def list_documents(
    status: Optional[str] = None,
    document_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    List all uploaded documents.
    """
    query = db.query(Document)
    
    if status:
        query = query.filter(Document.status == status)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    
    documents = query.order_by(Document.upload_date.desc()).offset(skip).limit(limit).all()
    
    result = []
    for doc in documents:
        chunk_count = db.query(DocumentChunk).filter(
            DocumentChunk.document_id == doc.id
        ).count()
        
        result.append(DocumentInfo(
            id=doc.id,
            filename=doc.filename,
            title=doc.title,
            document_type=doc.document_type,
            status=doc.status,
            page_count=doc.page_count,
            chunk_count=chunk_count,
            upload_date=doc.upload_date
        ))
    
    return result


@router.get("/{document_id}", response_model=DocumentInfo)
async def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get document details by ID.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    chunk_count = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).count()
    
    return DocumentInfo(
        id=document.id,
        filename=document.filename,
        title=document.title,
        document_type=document.document_type,
        status=document.status,
        page_count=document.page_count,
        chunk_count=chunk_count,
        upload_date=document.upload_date
    )


@router.get("/{document_id}/status", response_model=ProcessingStatus)
async def get_processing_status(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Get document processing status.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    chunks_processed = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id,
        DocumentChunk.embedding.isnot(None)
    ).count()
    
    total_chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).count()
    
    return ProcessingStatus(
        document_id=document_id,
        filename=document.filename,
        status=document.status,
        chunks_processed=chunks_processed,
        total_chunks=total_chunks if total_chunks > 0 else None
    )


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a document and all its chunks.
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Delete chunks first
    db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).delete()
    
    # Delete document
    db.delete(document)
    db.commit()
    
    logger.info(f"Document deleted: {document.filename} (ID: {document_id})")
    
    return {"status": "success", "message": f"Document {document.filename} deleted"}
