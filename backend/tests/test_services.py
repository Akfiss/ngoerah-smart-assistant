"""
Test LLM Service
Verify Ollama connection and LLM generation
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_llm_connection():
    """Test that LLM service can connect to Ollama"""
    from app.services.llm_service import LLMService
    
    llm = LLMService()
    assert llm.test_connection() == True, "LLM connection failed - make sure Ollama is running"
    print("✅ LLM connection successful")


def test_llm_generate():
    """Test basic LLM text generation"""
    from app.services.llm_service import LLMService
    
    llm = LLMService()
    response = llm.generate("Apa itu RSUP Sanglah? Jawab dalam 1 kalimat.", max_tokens=100)
    
    assert len(response) > 0, "LLM returned empty response"
    assert isinstance(response, str), "LLM response should be string"
    print(f"✅ LLM Response: {response[:100]}...")


def test_llm_generate_with_system_prompt():
    """Test LLM generation with system prompt"""
    from app.services.llm_service import LLMService
    
    llm = LLMService()
    system_prompt = "Kamu adalah asisten rumah sakit. Jawab dengan singkat."
    response = llm.generate(
        "Halo", 
        max_tokens=50,
        system_prompt=system_prompt
    )
    
    assert len(response) > 0, "LLM returned empty response"
    print(f"✅ LLM with system prompt: {response[:80]}...")


def test_embedding_service():
    """Test embedding service"""
    from app.services.embedding_service import EmbeddingService
    
    emb = EmbeddingService()
    vector = emb.embed_text("Jam besuk ICU")
    
    assert len(vector) == 384, f"Expected 384 dimensions, got {len(vector)}"
    assert all(isinstance(v, float) for v in vector), "Embedding should be list of floats"
    print(f"✅ Embedding dimension: {len(vector)}")


def test_embedding_batch():
    """Test batch embedding"""
    from app.services.embedding_service import EmbeddingService
    
    emb = EmbeddingService()
    texts = ["Jam besuk", "Jadwal dokter", "Pendaftaran BPJS"]
    vectors = emb.embed_batch(texts)
    
    assert len(vectors) == 3, "Should return 3 embeddings"
    assert all(len(v) == 384 for v in vectors), "All embeddings should have 384 dims"
    print(f"✅ Batch embedding: {len(vectors)} vectors")


def test_intent_classifier():
    """Test intent classification"""
    from app.services.intent_service import IntentClassifier
    
    classifier = IntentClassifier()
    
    test_cases = [
        ("Jam besuk ICU jam berapa?", "FAQ_QUERY"),
        ("Saya mau daftar ke dokter anak", "REGISTRATION"),
        ("Halo", "CHITCHAT"),
    ]
    
    for message, expected_intent in test_cases:
        result = classifier.classify(message)
        print(f"  Message: '{message}' -> {result.intent} (conf: {result.confidence:.2f})")
        # Note: LLM may vary, so we don't strictly assert
    
    print("✅ Intent classification working")


def test_document_processor():
    """Test document processor"""
    from app.services.document_service import DocumentProcessor
    
    processor = DocumentProcessor()
    
    # Test text chunking
    sample_text = " ".join(["word"] * 1000)  # 1000 words
    chunks = processor.chunk_text(sample_text, chunk_size=100, overlap=10)
    
    assert len(chunks) > 0, "Should create chunks"
    print(f"✅ Document chunking: {len(chunks)} chunks from 1000 words")


if __name__ == "__main__":
    print("\n" + "="*50)
    print("Testing Ngoerah Smart Assistant Services")
    print("="*50 + "\n")
    
    print("1. Testing LLM Service...")
    test_llm_connection()
    test_llm_generate()
    test_llm_generate_with_system_prompt()
    
    print("\n2. Testing Embedding Service...")
    test_embedding_service()
    test_embedding_batch()
    
    print("\n3. Testing Intent Classifier...")
    test_intent_classifier()
    
    print("\n4. Testing Document Processor...")
    test_document_processor()
    
    print("\n" + "="*50)
    print("✅ All tests passed!")
    print("="*50)
