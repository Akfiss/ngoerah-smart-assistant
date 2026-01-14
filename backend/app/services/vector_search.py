"""
Vector Search Service - Similarity search using pgvector
Searches document chunks by embedding similarity
"""

import logging
from typing import List, Optional
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    """Result from vector similarity search"""
    content: str
    page_number: Optional[int]
    title: Optional[str]
    filename: str
    similarity: float
    document_id: int
    chunk_id: int


class VectorSearchService:
    """Service for vector similarity search in document chunks"""
    
    def __init__(
        self, 
        top_k: Optional[int] = None,
        threshold: Optional[float] = None
    ):
        self.default_top_k = top_k or settings.TOP_K_RESULTS
        self.default_threshold = threshold or settings.SIMILARITY_THRESHOLD
        logger.info(f"Vector Search initialized (top_k={self.default_top_k}, threshold={self.default_threshold})")
    
    def search_similar(
        self, 
        db: Session,
        query_embedding: List[float],
        top_k: Optional[int] = None,
        threshold: Optional[float] = None
    ) -> List[SearchResult]:
        """
        Find similar document chunks using cosine similarity.
        
        Args:
            db: Database session
            query_embedding: Query vector
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of SearchResult objects
        """
        top_k = top_k or self.default_top_k
        threshold = threshold or self.default_threshold
        
        try:
            # Convert embedding to string format for pgvector
            embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'
            
            query = text("""
                SELECT 
                    dc.id as chunk_id,
                    dc.content,
                    dc.page_number,
                    d.id as document_id,
                    d.title,
                    d.filename,
                    1 - (dc.embedding <=> :query_vector::vector) AS similarity
                FROM document_chunks dc
                JOIN documents d ON dc.document_id = d.id
                WHERE d.status = 'ready'
                  AND dc.embedding IS NOT NULL
                  AND 1 - (dc.embedding <=> :query_vector::vector) > :threshold
                ORDER BY dc.embedding <=> :query_vector::vector
                LIMIT :top_k
            """)
            
            result = db.execute(query, {
                "query_vector": embedding_str,
                "threshold": threshold,
                "top_k": top_k
            })
            
            search_results = []
            for row in result.fetchall():
                search_results.append(SearchResult(
                    content=row.content,
                    page_number=row.page_number,
                    title=row.title,
                    filename=row.filename,
                    similarity=float(row.similarity),
                    document_id=row.document_id,
                    chunk_id=row.chunk_id
                ))
            
            logger.info(f"Found {len(search_results)} similar chunks (threshold={threshold})")
            return search_results
            
        except Exception as e:
            logger.error(f"Vector search error: {str(e)}")
            raise
    
    def search_by_text(
        self, 
        db: Session,
        query_text: str,
        embedding_service,
        top_k: Optional[int] = None,
        threshold: Optional[float] = None
    ) -> List[SearchResult]:
        """
        Search for similar chunks given a text query.
        
        Args:
            db: Database session
            query_text: Text query
            embedding_service: EmbeddingService instance for encoding
            top_k: Number of results
            threshold: Minimum similarity
            
        Returns:
            List of SearchResult objects
        """
        # Convert query to embedding
        query_embedding = embedding_service.embed_text(query_text)
        
        # Perform vector search
        return self.search_similar(db, query_embedding, top_k, threshold)


# Singleton instance
_vector_search_service: Optional[VectorSearchService] = None


def get_vector_search_service() -> VectorSearchService:
    """Get or create vector search service singleton"""
    global _vector_search_service
    if _vector_search_service is None:
        _vector_search_service = VectorSearchService()
    return _vector_search_service
