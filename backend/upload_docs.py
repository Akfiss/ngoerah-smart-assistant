"""
Bulk Upload Documents Script
Upload multiple documents from a folder to the RAG database
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.database import Document, DocumentChunk
from app.services.embedding_service import get_embedding_service
from app.services.document_service import get_document_processor


def process_markdown_file(file_path: Path) -> dict:
    """Process a markdown file and return content with chunks"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple chunking for markdown - split by sections or paragraphs
    processor = get_document_processor()
    
    # Clean the content
    clean_content = processor.clean_text(content)
    
    # Create chunks (smaller for markdown)
    chunks = []
    paragraphs = content.split('\n\n')
    
    current_chunk = ""
    chunk_index = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if len(current_chunk) + len(para) < 800:  # ~200 words
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            if current_chunk:
                chunks.append({
                    'chunk_index': chunk_index,
                    'content': processor.clean_text(current_chunk),
                    'page_number': None
                })
                chunk_index += 1
            current_chunk = para
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append({
            'chunk_index': chunk_index,
            'content': processor.clean_text(current_chunk),
            'page_number': None
        })
    
    return {
        'content': clean_content,
        'chunks': chunks
    }


def upload_documents_from_folder(folder_path: str):
    """Upload all documents from a folder to the RAG database"""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Get all markdown and text files
    files = list(folder.glob("*.md")) + list(folder.glob("*.txt"))
    
    if not files:
        print(f"❌ No .md or .txt files found in {folder_path}")
        return
    
    print("=" * 60)
    print("Bulk Document Upload for Ngoerah Smart Assistant")
    print("=" * 60)
    print(f"\n📁 Source folder: {folder_path}")
    print(f"📄 Files found: {len(files)}")
    
    # Initialize services
    print("\n⏳ Loading embedding model...")
    embedding_service = get_embedding_service()
    print(f"✅ Embedding model loaded (dimension: {embedding_service.dimension})")
    
    # Process each file
    db = SessionLocal()
    total_chunks = 0
    
    try:
        for i, file_path in enumerate(files, 1):
            filename = file_path.name
            title = file_path.stem.replace('-', ' ').replace('_', ' ')
            
            print(f"\n[{i}/{len(files)}] Processing: {filename}")
            
            # Check if already exists
            existing = db.query(Document).filter(Document.filename == filename).first()
            if existing:
                print(f"   ⚠️ Already exists, skipping...")
                continue
            
            # Process the file
            result = process_markdown_file(file_path)
            
            # Create document record
            doc = Document(
                filename=filename,
                title=title,
                content=result['content'],
                document_type='panduan',
                file_size_kb=file_path.stat().st_size // 1024,
                status='processing'
            )
            db.add(doc)
            db.flush()
            
            # Create chunks with embeddings
            for chunk_data in result['chunks']:
                # Generate embedding
                embedding = embedding_service.embed_text(chunk_data['content'])
                
                chunk = DocumentChunk(
                    document_id=doc.id,
                    chunk_index=chunk_data['chunk_index'],
                    content=chunk_data['content'],
                    embedding=embedding,
                    page_number=chunk_data.get('page_number')
                )
                db.add(chunk)
                total_chunks += 1
            
            doc.status = 'ready'
            db.commit()
            
            print(f"   ✅ Created {len(result['chunks'])} chunks")
        
        print("\n" + "=" * 60)
        print(f"✅ Upload complete!")
        print(f"   Documents processed: {len(files)}")
        print(f"   Total chunks created: {total_chunks}")
        print("=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Error: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Default folder path
    default_folder = r"D:\Magang Kemanker\chatbot-ngoerah\panduan-simetriss"
    
    folder = sys.argv[1] if len(sys.argv) > 1 else default_folder
    upload_documents_from_folder(folder)
