"""
Ngoerah Smart Assistant - FastAPI Backend
Main application entry point with RAG-powered chat
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from datetime import datetime

from app.config import settings
from app.routers import chat_router, documents_router

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    logger.info("🚀 Starting Ngoerah Smart Assistant API...")
    logger.info(f"📍 Running on {settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"🤖 LLM Model: {settings.LLM_MODEL}")
    logger.info(f"🔢 Embedding Model: {settings.EMBEDDING_MODEL}")
    logger.info(f"🔗 Database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else 'configured'}")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down Ngoerah Smart Assistant API...")


# Create FastAPI application
app = FastAPI(
    title="Ngoerah Smart Assistant API",
    description="""
## AI-Powered Virtual Assistant untuk RSUP Prof. dr. I.G.N.G. Ngoerah

Asisten virtual berbasis RAG (Retrieval-Augmented Generation) untuk menjawab pertanyaan seputar:
- 📅 Jadwal dokter dan poliklinik
- 🏥 Jam besuk dan peraturan RS
- 📝 Prosedur pendaftaran
- 💳 Persyaratan BPJS
- 📍 Lokasi fasilitas RS

### Authentication
API ini saat ini public untuk development. Authentication akan ditambahkan di production.

### Rate Limiting
- 10 requests per minute per IP (chat endpoint)
    """,
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)


# =============================================================================
# MIDDLEWARE
# =============================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration_ms = int((time.time() - start_time) * 1000)
    
    # Log request (skip health checks for less noise)
    if not request.url.path.startswith("/health"):
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Duration: {duration_ms}ms"
        )
    
    # Add custom headers
    response.headers["X-Response-Time"] = f"{duration_ms}ms"
    
    return response


# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "message": "Internal server error" if not settings.DEBUG else str(exc),
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# =============================================================================
# INCLUDE ROUTERS
# =============================================================================

app.include_router(chat_router)
app.include_router(documents_router)


# =============================================================================
# ROOT & HEALTH ENDPOINTS
# =============================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "🏥 Selamat datang di Ngoerah Smart Assistant API!",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
        "endpoints": {
            "chat": "/api/v1/chat",
            "documents": "/api/v1/documents",
            "health": "/health"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "ngoerah-smart-assistant",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health/detailed", tags=["Health"])
async def detailed_health_check():
    """Detailed health check with component status"""
    from app.database import SessionLocal
    
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "components": {
            "api": {"status": "up"},
            "database": {"status": "unknown"},
            "llm": {"status": "unknown"},
            "embedding": {"status": "unknown"}
        }
    }
    
    # Check database
    try:
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        health_status["components"]["database"] = {"status": "up"}
    except Exception as e:
        health_status["components"]["database"] = {
            "status": "down",
            "error": str(e) if settings.DEBUG else "Connection failed"
        }
        health_status["status"] = "degraded"
    
    # Check LLM (optional, could be slow)
    try:
        from app.services.llm_service import get_llm_service
        llm = get_llm_service()
        if llm.test_connection():
            health_status["components"]["llm"] = {
                "status": "up",
                "model": settings.LLM_MODEL
            }
        else:
            health_status["components"]["llm"] = {"status": "down"}
            health_status["status"] = "degraded"
    except Exception as e:
        health_status["components"]["llm"] = {
            "status": "error",
            "error": str(e) if settings.DEBUG else "Check failed"
        }
    
    # Check embedding service
    try:
        from app.services.embedding_service import get_embedding_service
        emb = get_embedding_service()
        if emb.test_connection():
            health_status["components"]["embedding"] = {
                "status": "up",
                "model": settings.EMBEDDING_MODEL,
                "dimension": emb.dimension
            }
        else:
            health_status["components"]["embedding"] = {"status": "down"}
    except Exception as e:
        health_status["components"]["embedding"] = {
            "status": "error",
            "error": str(e) if settings.DEBUG else "Check failed"
        }
    
    return health_status


@app.get("/api/v1/stats", tags=["Analytics"])
async def get_basic_stats():
    """Get basic usage statistics"""
    from app.database import SessionLocal
    from app.models.database import Message, Conversation, Document, Feedback
    from sqlalchemy import func
    
    db = SessionLocal()
    try:
        total_conversations = db.query(Conversation).count()
        total_messages = db.query(Message).filter(Message.role == "user").count()
        total_documents = db.query(Document).filter(Document.status == "ready").count()
        
        # Feedback stats
        positive = db.query(Feedback).filter(Feedback.rating > 0).count()
        negative = db.query(Feedback).filter(Feedback.rating < 0).count()
        
        # Average response time
        avg_response = db.query(func.avg(Message.response_time_ms)).filter(
            Message.role == "assistant",
            Message.response_time_ms.isnot(None)
        ).scalar() or 0
        
        return {
            "total_conversations": total_conversations,
            "total_queries": total_messages,
            "total_documents": total_documents,
            "feedback": {
                "positive": positive,
                "negative": negative,
                "satisfaction_rate": round(positive / (positive + negative) * 100, 1) if (positive + negative) > 0 else 0
            },
            "average_response_time_ms": round(avg_response, 0),
            "timestamp": datetime.utcnow().isoformat()
        }
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
