"""
Vector Search Service - Similarity search using cosine similarity
Searches document chunks by embedding similarity
Works without pgvector extension using Python-based similarity calculation
"""

import logging
import numpy as np
from typing import List, Optional
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.config import settings
from app.models.database import DocumentChunk, Document

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
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if vec1 is None or vec2 is None:
            return 0.0
        
        a = np.array(vec1)
        b = np.array(vec2)
        
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return float(dot_product / (norm_a * norm_b))
    
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
            # Get all chunks with embeddings from ready documents
            chunks = db.query(DocumentChunk, Document).join(
                Document, DocumentChunk.document_id == Document.id
            ).filter(
                Document.status == 'ready',
                DocumentChunk.embedding.isnot(None)
            ).all()
            
            if not chunks:
                logger.info("No chunks with embeddings found")
                return []
            
            # Calculate similarity for each chunk
            results_with_similarity = []
            for chunk, doc in chunks:
                similarity = self._cosine_similarity(query_embedding, chunk.embedding)
                if similarity >= threshold:
                    results_with_similarity.append({
                        'chunk': chunk,
                        'doc': doc,
                        'similarity': similarity
                    })
            
            # Sort by similarity (descending) and take top_k
            results_with_similarity.sort(key=lambda x: x['similarity'], reverse=True)
            top_results = results_with_similarity[:top_k]
            
            # Convert to SearchResult objects
            search_results = []
            for item in top_results:
                chunk = item['chunk']
                doc = item['doc']
                search_results.append(SearchResult(
                    content=chunk.content,
                    page_number=chunk.page_number,
                    title=doc.title,
                    filename=doc.filename,
                    similarity=item['similarity'],
                    document_id=doc.id,
                    chunk_id=chunk.id
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
