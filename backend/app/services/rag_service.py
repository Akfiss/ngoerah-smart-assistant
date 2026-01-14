"""
RAG Service - Retrieval-Augmented Generation Pipeline
Orchestrates the complete RAG flow: intent → retrieval → generation
"""

import logging
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

from sqlalchemy.orm import Session

from app.config import settings
from app.services.llm_service import LLMService, get_llm_service
from app.services.embedding_service import EmbeddingService, get_embedding_service
from app.services.vector_search import VectorSearchService, get_vector_search_service, SearchResult
from app.services.intent_service import IntentClassifier, get_intent_classifier, IntentResult

logger = logging.getLogger(__name__)


@dataclass
class RAGResponse:
    """Response from RAG pipeline"""
    response: str
    intent: str
    confidence: float
    sources: List[Dict[str, Any]]
    registration_link: Optional[str] = None
    poli: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


class RAGService:
    """Main RAG service orchestrating the complete pipeline"""
    
    SYSTEM_PROMPT = """Kamu adalah asisten virtual RSUP Prof. dr. I.G.N.G. Ngoerah Sanglah, rumah sakit pendidikan terbesar di Bali, Indonesia.

Karakteristik:
- Ramah, sopan, dan profesional
- Menjawab dalam Bahasa Indonesia yang mudah dipahami
- Fokus pada keakuratan informasi berdasarkan dokumen yang diberikan
- Jika tidak yakin, akui keterbatasan dan sarankan menghubungi call center

Batasan:
- Tidak memberikan diagnosis medis
- Tidak menggantikan konsultasi dokter
- Hanya memberikan informasi umum berdasarkan dokumen resmi RS"""

    def __init__(
        self,
        llm_service: Optional[LLMService] = None,
        embedding_service: Optional[EmbeddingService] = None,
        vector_search: Optional[VectorSearchService] = None,
        intent_classifier: Optional[IntentClassifier] = None
    ):
        self.llm = llm_service or get_llm_service()
        self.embedding = embedding_service or get_embedding_service()
        self.vector_search = vector_search or get_vector_search_service()
        self.intent_classifier = intent_classifier or get_intent_classifier()
        logger.info("RAG Service initialized")
    
    def process_query(
        self, 
        db: Session,
        user_message: str, 
        session_id: Optional[str] = None,
        conversation_history: Optional[List[Dict]] = None
    ) -> RAGResponse:
        """
        Process a user query through the RAG pipeline.
        
        Args:
            db: Database session
            user_message: The user's message
            session_id: Optional session ID for context
            conversation_history: Optional previous messages for context
            
        Returns:
            RAGResponse with generated answer and metadata
        """
        logger.info(f"Processing query: {user_message[:50]}...")
        
        # Step 1: Classify intent
        intent_result = self.intent_classifier.classify(user_message)
        logger.info(f"Intent: {intent_result.intent} (confidence: {intent_result.confidence})")
        
        # Step 2: Route based on intent
        if intent_result.intent == 'REGISTRATION':
            return self._handle_registration(user_message, intent_result)
        
        elif intent_result.intent == 'EMERGENCY':
            return self._handle_emergency(user_message, intent_result)
        
        elif intent_result.intent == 'COMPLAINT':
            return self._handle_complaint(user_message, intent_result)
        
        elif intent_result.intent == 'CHITCHAT':
            return self._handle_chitchat(user_message, intent_result)
        
        else:  # FAQ_QUERY
            return self._handle_faq(db, user_message, intent_result, conversation_history)
    
    def _handle_faq(
        self, 
        db: Session,
        query: str, 
        intent_result: IntentResult,
        conversation_history: Optional[List[Dict]] = None
    ) -> RAGResponse:
        """Handle FAQ queries with RAG"""
        
        # Step 1: Get query embedding
        query_embedding = self.embedding.embed_text(query)
        
        # Step 2: Search for relevant chunks
        search_results = self.vector_search.search_similar(
            db=db,
            query_embedding=query_embedding,
            top_k=settings.TOP_K_RESULTS,
            threshold=0.5  # Lower threshold to get some results
        )
        
        # Step 3: Generate response
        if not search_results:
            return RAGResponse(
                response="Maaf, saya tidak menemukan informasi yang relevan tentang pertanyaan Anda. "
                        "Silakan hubungi call center kami di (0361) 227911 atau kunjungi website resmi RS untuk informasi lebih lanjut.",
                intent=intent_result.intent,
                confidence=intent_result.confidence,
                sources=[]
            )
        
        # Build context from search results
        context = self._build_context(search_results)
        
        # Generate answer
        answer = self._generate_answer(query, context, conversation_history)
        
        # Format sources
        sources = [
            {
                "document": r.filename,
                "title": r.title,
                "page": r.page_number,
                "similarity": round(r.similarity, 3)
            }
            for r in search_results
        ]
        
        return RAGResponse(
            response=answer,
            intent=intent_result.intent,
            confidence=search_results[0].similarity if search_results else 0,
            sources=sources
        )
    
    def _build_context(self, search_results: List[SearchResult]) -> str:
        """Build context string from search results"""
        context_parts = []
        for r in search_results:
            source_info = f"[Sumber: {r.title or r.filename}"
            if r.page_number:
                source_info += f", Halaman {r.page_number}"
            source_info += "]"
            
            context_parts.append(f"{source_info}\n{r.content}")
        
        return "\n\n---\n\n".join(context_parts)
    
    def _generate_answer(
        self, 
        query: str, 
        context: str,
        conversation_history: Optional[List[Dict]] = None
    ) -> str:
        """Generate answer using LLM with context"""
        
        prompt = f"""Berdasarkan informasi dari dokumen resmi RSUP Sanglah berikut, jawab pertanyaan pasien.

KONTEKS DARI DOKUMEN:
{context}

PERTANYAAN PASIEN:
{query}

INSTRUKSI:
1. Jawab menggunakan HANYA informasi dari konteks di atas
2. Gunakan bahasa Indonesia yang ramah dan mudah dipahami
3. Jika informasi tidak tersedia di konteks, katakan dengan jelas
4. Jangan mengarang informasi
5. Jawab dengan singkat dan jelas (maksimal 3-4 kalimat)
6. Sertakan informasi penting seperti jam, lokasi, atau nomor kontak jika relevan

JAWABAN:"""

        try:
            answer = self.llm.generate(
                prompt, 
                max_tokens=400, 
                temperature=0.3,
                system_prompt=self.SYSTEM_PROMPT
            )
            return answer.strip()
        except Exception as e:
            logger.error(f"LLM generation error: {str(e)}")
            return "Maaf, terjadi kesalahan saat memproses pertanyaan Anda. Silakan coba lagi atau hubungi call center di (0361) 227911."
    
    def _handle_registration(self, query: str, intent_result: IntentResult) -> RAGResponse:
        """Handle registration intent"""
        query_lower = query.lower()
        
        # Detect specialty
        poli_map = {
            'anak': ('Anak', 'poli=anak'),
            'pediatri': ('Anak', 'poli=anak'),
            'bayi': ('Anak', 'poli=anak'),
            'gigi': ('Gigi & Mulut', 'poli=gigi'),
            'dental': ('Gigi & Mulut', 'poli=gigi'),
            'mata': ('Mata', 'poli=mata'),
            'jantung': ('Jantung', 'poli=jantung'),
            'kardio': ('Jantung', 'poli=jantung'),
            'kulit': ('Kulit & Kelamin', 'poli=kulit'),
            'derma': ('Kulit & Kelamin', 'poli=kulit'),
            'saraf': ('Saraf', 'poli=saraf'),
            'neuro': ('Saraf', 'poli=saraf'),
            'dalam': ('Penyakit Dalam', 'poli=dalam'),
            'internist': ('Penyakit Dalam', 'poli=dalam'),
            'bedah': ('Bedah', 'poli=bedah'),
            'ortho': ('Bedah Ortopedi', 'poli=ortopedi'),
            'tulang': ('Bedah Ortopedi', 'poli=ortopedi'),
            'obgyn': ('Obstetri & Ginekologi', 'poli=obgyn'),
            'kandungan': ('Obstetri & Ginekologi', 'poli=obgyn'),
            'hamil': ('Obstetri & Ginekologi', 'poli=obgyn'),
            'tht': ('THT-KL', 'poli=tht'),
            'telinga': ('THT-KL', 'poli=tht'),
            'paru': ('Paru', 'poli=paru'),
            'psikiatri': ('Psikiatri', 'poli=psikiatri'),
            'jiwa': ('Psikiatri', 'poli=psikiatri'),
        }
        
        poli = "Umum"
        poli_param = ""
        
        for keyword, (name, param) in poli_map.items():
            if keyword in query_lower:
                poli = name
                poli_param = param
                break
        
        base_url = "https://simrs.sanglah.go.id/daftar"
        link = f"{base_url}?{poli_param}" if poli_param else base_url
        
        response = f"""🏥 **Pendaftaran Poliklinik {poli}**

Untuk mendaftar, silakan:

1️⃣ **Online:** Klik link berikut
   🔗 {link}

2️⃣ **Call Center:** (0361) 227911
   ⏰ Senin-Jumat: 07.00-14.00 WITA

📋 **Dokumen yang perlu disiapkan:**
• KTP/Identitas
• Kartu BPJS (jika menggunakan BPJS)
• Surat Rujukan (jika ada)
• Rekam medis sebelumnya (jika ada)

💡 Disarankan datang 30 menit sebelum jadwal untuk registrasi administrasi."""

        return RAGResponse(
            response=response,
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            sources=[],
            registration_link=link,
            poli=poli
        )
    
    def _handle_emergency(self, query: str, intent_result: IntentResult) -> RAGResponse:
        """Handle emergency situations"""
        response = """🚨 **SITUASI DARURAT**

Jika ini adalah keadaan darurat medis:

📞 **Hubungi IGD RSUP Sanglah:**
• Telepon: **(0361) 227911 ext. 111**
• WhatsApp Darurat: **-**

🏥 **Lokasi IGD:**
Gedung A Lantai 1, RSUP Prof. dr. I.G.N.G. Ngoerah
Jl. Diponegoro, Denpasar, Bali

🚑 **IGD RSUP Sanglah beroperasi 24 JAM**

⚠️ Jika kondisi sangat gawat, segera panggil ambulans atau bawa pasien langsung ke IGD terdekat!

Saya adalah asisten virtual dan tidak dapat memberikan pertolongan medis. Segera hubungi tenaga medis profesional."""

        return RAGResponse(
            response=response,
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            sources=[]
        )
    
    def _handle_complaint(self, query: str, intent_result: IntentResult) -> RAGResponse:
        """Handle complaints"""
        response = """📝 **Terima kasih atas masukan Anda**

Kami sangat menghargai feedback Anda untuk meningkatkan layanan kami.

Untuk menyampaikan keluhan atau saran, silakan hubungi:

📞 **Humas & Customer Service:**
• Telepon: (0361) 227911 ext. 120
• Email: humas@sanglah.go.id

📱 **Media Sosial Resmi:**
• Instagram: @rsup_sanglah
• Website: www.sanglah.go.id

🏢 **Unit Pengaduan:**
Gedung Administrasi Lantai 1
Senin-Jumat: 08.00-15.00 WITA

Keluhan Anda akan ditindaklanjuti dalam waktu 1x24 jam kerja."""

        return RAGResponse(
            response=response,
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            sources=[]
        )
    
    def _handle_chitchat(self, query: str, intent_result: IntentResult) -> RAGResponse:
        """Handle casual conversation"""
        query_lower = query.lower()
        
        if any(g in query_lower for g in ['pagi', 'siang', 'sore', 'malam']):
            greeting = "Selamat " + next(g for g in ['pagi', 'siang', 'sore', 'malam'] if g in query_lower)
        else:
            greeting = "Halo"
        
        response = f"""{greeting}! 👋

Saya adalah **Ngoerah Smart Assistant**, asisten virtual RSUP Prof. dr. I.G.N.G. Ngoerah Sanglah.

Saya dapat membantu Anda dengan informasi tentang:
• 📅 Jadwal dokter & poliklinik
• 🏥 Jam besuk & peraturan RS
• 📝 Prosedur pendaftaran
• 💳 Persyaratan BPJS
• 📍 Lokasi fasilitas RS

Silakan tanyakan apa saja! 😊"""

        return RAGResponse(
            response=response,
            intent=intent_result.intent,
            confidence=intent_result.confidence,
            sources=[]
        )


# Singleton instance
_rag_service: Optional[RAGService] = None


def get_rag_service() -> RAGService:
    """Get or create RAG service singleton"""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service
