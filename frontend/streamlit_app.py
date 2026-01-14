"""
Ngoerah Smart Assistant - Streamlit Frontend
Chat interface for internal testing and demo
Uses native Streamlit components only
"""

import streamlit as st
import requests
from datetime import datetime
import uuid

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Ngoerah Smart Assistant",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CONFIGURATION
# =============================================================================

API_BASE_URL = "http://localhost:8000"

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def send_message_to_api(message: str) -> dict:
    """Send message to backend API and get response"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/chat",
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "response": f"Error: {response.status_code} - {response.text}",
                "intent": "error",
                "confidence": 0,
                "sources": []
            }
    except requests.exceptions.ConnectionError:
        return {
            "response": "❌ Tidak dapat terhubung ke server. Pastikan backend API berjalan di " + API_BASE_URL,
            "intent": "error",
            "confidence": 0,
            "sources": []
        }
    except requests.exceptions.Timeout:
        return {
            "response": "⏱️ Request timeout. Server mungkin sedang sibuk, coba lagi.",
            "intent": "error",
            "confidence": 0,
            "sources": []
        }
    except Exception as e:
        return {
            "response": f"❌ Error: {str(e)}",
            "intent": "error",
            "confidence": 0,
            "sources": []
        }


def check_api_health() -> bool:
    """Check if backend API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.title("🏥 Ngoerah Assistant")
    st.caption("Asisten Virtual RSUP Sanglah")
    
    st.divider()
    
    # API Status
    api_healthy = check_api_health()
    if api_healthy:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Offline")
        st.info(f"Pastikan backend berjalan di: {API_BASE_URL}")
    
    st.divider()
    
    # Quick Actions
    st.subheader("⚡ Pertanyaan Cepat")
    
    quick_questions = [
        "Bagaimana cara login SIMETRISS?",
        "Cara registrasi pasien rawat jalan?",
        "Bagaimana mengatur jadwal dokter?",
        "Cara mengubah poliklinik?",
        "Apa itu passphrase?"
    ]
    
    for q in quick_questions:
        if st.button(q, key=f"quick_{q[:15]}", use_container_width=True):
            st.session_state.pending_question = q
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
    
    st.divider()
    
    # Session info
    with st.expander("ℹ️ Info Sesi"):
        st.text(f"Session ID: {st.session_state.session_id[:8]}...")
        st.text(f"Total pesan: {len(st.session_state.messages)}")


# =============================================================================
# MAIN CONTENT
# =============================================================================

# Header
st.title("🏥 Ngoerah Smart Assistant")
st.caption("Asisten Virtual RSUP Prof. dr. I.G.N.G. Ngoerah Sanglah")
st.divider()

# Check for pending question from quick action
if 'pending_question' in st.session_state:
    pending_q = st.session_state.pending_question
    del st.session_state.pending_question
    
    # Add to messages and get response
    st.session_state.messages.append({
        "role": "user",
        "content": pending_q,
        "timestamp": datetime.now()
    })
    
    with st.spinner("🤔 Sedang berpikir..."):
        response = send_message_to_api(pending_q)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.get("response", "Maaf, terjadi kesalahan."),
            "sources": response.get("sources", []),
            "intent": response.get("intent", "unknown"),
            "response_time_ms": response.get("response_time_ms", 0),
            "timestamp": datetime.now()
        })
    st.rerun()


# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        # Show metadata for assistant messages
        if msg["role"] == "assistant":
            col1, col2 = st.columns([3, 1])
            
            # Show sources if available
            if msg.get("sources") and len(msg["sources"]) > 0:
                with col1:
                    with st.expander("📚 Sumber Referensi"):
                        for src in msg["sources"]:
                            doc_name = src.get('document', 'N/A')
                            page = src.get('page')
                            similarity = src.get('similarity', 0)
                            if page:
                                st.write(f"• {doc_name} (Hal. {page}) - {similarity:.0%}")
                            else:
                                st.write(f"• {doc_name} - {similarity:.0%}")
            
            # Show response time
            with col2:
                if msg.get("response_time_ms"):
                    st.caption(f"⚡ {msg['response_time_ms']}ms")


# Chat input
if prompt := st.chat_input("Tanya sesuatu tentang RSUP Sanglah..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now()
    })
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("🤔 Sedang berpikir..."):
            response = send_message_to_api(prompt)
        
        answer = response.get("response", "Maaf, terjadi kesalahan.")
        st.write(answer)
        
        # Store assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": response.get("sources", []),
            "intent": response.get("intent", "unknown"),
            "response_time_ms": response.get("response_time_ms", 0),
            "timestamp": datetime.now()
        })
        
        col1, col2 = st.columns([3, 1])
        
        # Show sources if available
        if response.get("sources") and len(response["sources"]) > 0:
            with col1:
                with st.expander("📚 Sumber Referensi"):
                    for src in response["sources"]:
                        doc_name = src.get('document', 'N/A')
                        page = src.get('page')
                        similarity = src.get('similarity', 0)
                        if page:
                            st.write(f"• {doc_name} (Hal. {page}) - {similarity:.0%}")
                        else:
                            st.write(f"• {doc_name} - {similarity:.0%}")
        
        # Show response time
        with col2:
            if response.get("response_time_ms"):
                st.caption(f"⚡ {response['response_time_ms']}ms")


# Empty state - Welcome message
if not st.session_state.messages:
    st.info("""
    👋 **Selamat datang di Ngoerah Smart Assistant!**
    
    Saya dapat membantu Anda dengan informasi tentang:
    - 📅 Panduan SIMETRISS
    - 🏥 Registrasi pasien
    - 📝 Prosedur pendaftaran
    - 👨‍⚕️ Jadwal dokter
    - 📍 Informasi layanan RS
    
    Silakan ketik pertanyaan Anda di bawah atau gunakan **Pertanyaan Cepat** di sidebar.
    """)
    
    # Quick start suggestions
    st.write("**💡 Coba tanyakan:**")
    suggestions = [
        "Bagaimana cara login ke SIMETRISS?",
        "Cara registrasi pasien rawat jalan?",
        "Bagaimana cara mengatur jadwal dokter?"
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"suggest_{i}", use_container_width=True):
                st.session_state.pending_question = suggestion
                st.rerun()
