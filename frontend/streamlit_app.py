"""
Ngoerah Smart Assistant - Streamlit Frontend
Chat interface for internal testing and demo
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
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown("""
<style>
/* Main container */
.main {
    background-color: #f5f7fa;
}

/* Chat message containers */
.user-message {
    background-color: #007bff;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0;
    max-width: 80%;
    float: right;
    clear: both;
}

.assistant-message {
    background-color: white;
    color: #333;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 0;
    max-width: 80%;
    float: left;
    clear: both;
    border: 1px solid #e0e0e0;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

/* Header styling */
.header-container {
    display: flex;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 2px solid #007bff;
    margin-bottom: 1rem;
}

/* Quick action buttons */
.stButton > button {
    border-radius: 20px;
    border: 1px solid #007bff;
    color: #007bff;
    background-color: white;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background-color: #007bff;
    color: white;
}

/* Response time badge */
.response-time {
    font-size: 0.75rem;
    color: #888;
    text-align: right;
}
</style>
""", unsafe_allow_html=True)


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
            timeout=30
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
    st.image("https://via.placeholder.com/150x50?text=RSUP+Sanglah", width=150)
    st.title("🏥 Ngoerah Assistant")
    st.caption("Asisten Virtual RSUP Sanglah")
    
    st.divider()
    
    # API Status
    api_healthy = check_api_health()
    if api_healthy:
        st.success("✅ API Connected")
    else:
        st.error("❌ API Offline")
        st.info(f"Pastikan backend berjalan di:\n`{API_BASE_URL}`")
    
    st.divider()
    
    # Quick Actions
    st.subheader("⚡ Pertanyaan Cepat")
    
    quick_questions = [
        "Jam besuk ICU kapan?",
        "Jadwal dokter anak hari ini?",
        "Bagaimana cara daftar online?",
        "Lokasi poli gigi dimana?",
        "Persyaratan BPJS apa saja?"
    ]
    
    for q in quick_questions:
        if st.button(q, key=f"quick_{q[:20]}", use_container_width=True):
            st.session_state.pending_question = q
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Hapus Riwayat Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()
    
    st.divider()
    
    # Session info
    with st.expander("ℹ️ Info Sesi"):
        st.code(f"Session ID:\n{st.session_state.session_id[:8]}...")
        st.write(f"Total pesan: {len(st.session_state.messages)}")


# =============================================================================
# MAIN CONTENT
# =============================================================================

# Header
st.markdown("""
<div class="header-container">
    <h1>🏥 Ngoerah Smart Assistant</h1>
</div>
""", unsafe_allow_html=True)

st.caption("Asisten Virtual RSUP Prof. dr. I.G.N.G. Ngoerah - Tanya apa saja tentang layanan RS!")


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
            "timestamp": datetime.now()
        })
    st.rerun()


# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        
        # Show sources for assistant messages
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("📚 Sumber Referensi"):
                for src in msg["sources"]:
                    st.write(f"• {src.get('document', 'N/A')} (Hal. {src.get('page', 'N/A')})")


# Chat input
if prompt := st.chat_input("Tanya sesuatu tentang RSUP Sanglah..."):
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now()
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from API
    with st.chat_message("assistant"):
        with st.spinner("🤔 Sedang berpikir..."):
            response = send_message_to_api(prompt)
            
        st.markdown(response.get("response", "Maaf, terjadi kesalahan."))
        
        # Store assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response.get("response", "Maaf, terjadi kesalahan."),
            "sources": response.get("sources", []),
            "intent": response.get("intent", "unknown"),
            "timestamp": datetime.now()
        })
        
        # Show sources if available
        if response.get("sources"):
            with st.expander("📚 Sumber Referensi"):
                for src in response["sources"]:
                    st.write(f"• {src.get('document', 'N/A')} (Hal. {src.get('page', 'N/A')})")
        
        # Show response time
        if response.get("response_time_ms"):
            st.caption(f"⚡ Response time: {response['response_time_ms']}ms")


# Empty state
if not st.session_state.messages:
    st.info("""
    👋 **Selamat datang di Ngoerah Smart Assistant!**
    
    Saya dapat membantu Anda dengan informasi tentang:
    - 📅 Jadwal dokter dan poliklinik
    - 🏥 Jam besuk dan peraturan RS
    - 📝 Prosedur pendaftaran
    - 💳 Persyaratan BPJS
    - 📍 Lokasi fasilitas RS
    
    Silakan ketik pertanyaan Anda di bawah atau gunakan **Pertanyaan Cepat** di sidebar.
    """)
