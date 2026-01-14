# 🏥 Ngoerah Smart Assistant

AI-Powered Virtual Assistant untuk RSUP Prof. dr. I.G.N.G. Ngoerah Sanglah, Bali.

## Overview

Ngoerah Smart Assistant adalah asisten virtual bertenaga Generative AI yang menggunakan teknologi **Llama 3** dengan metode **RAG (Retrieval-Augmented Generation)** untuk memberikan jawaban akurat dan kontekstual berdasarkan basis pengetahuan internal rumah sakit.

## Features

- 🤖 **Smart FAQ** - Jawab pertanyaan umum tentang RS menggunakan RAG
- 📝 **Smart Navigation** - Arahkan pengguna ke halaman pendaftaran yang tepat
- 💬 **Conversation History** - Ingat konteks percakapan
- 👍 **Feedback Mechanism** - Kumpulkan feedback untuk improvement

## Tech Stack

| Component | Technology                             |
| --------- | -------------------------------------- |
| LLM       | Llama 3.1 (8B) via Ollama              |
| Backend   | FastAPI                                |
| Frontend  | Streamlit (MVP)                        |
| Database  | PostgreSQL + pgvector                  |
| Embedding | sentence-transformers/all-MiniLM-L6-v2 |
| Cache     | Redis                                  |

## Project Structure

```
ngoerah-smart-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # Database connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routers/             # API endpoints
│   │   └── services/            # Business logic (RAG, LLM, etc.)
│   ├── tests/
│   ├── requirements.txt
│   └── alembic/                 # Database migrations
├── frontend/
│   └── streamlit_app.py         # Streamlit chat interface
├── data/
│   └── documents/               # PDF storage for RAG
├── docs/
│   ├── API.md
│   └── SETUP.md
└── PRD.md                       # Product Requirements Document
```

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Ollama with llama3.1:8b model
- Redis (optional, for caching)

### Installation

1. **Clone repository**

   ```bash
   git clone https://github.com/Akfiss/ngoerah-smart-assistant.git
   cd ngoerah-smart-assistant
   ```

2. **Setup virtual environment**

   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Setup database**

   ```sql
   CREATE DATABASE ngoerah_assistant;
   \c ngoerah_assistant
   CREATE EXTENSION vector;
   ```

5. **Create tables**

   ```bash
   python -c "from app.database import create_tables; create_tables()"
   ```

6. **Configure environment**

   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

7. **Pull Ollama model**
   ```bash
   ollama pull llama3.1:8b
   ```

### Running the Application

**Backend API:**

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Frontend (Streamlit):**

```bash
cd frontend
streamlit run streamlit_app.py
```

**Access:**

- API Docs: http://localhost:8000/docs
- Chat UI: http://localhost:8501

## API Endpoints

| Endpoint                   | Method | Description         |
| -------------------------- | ------ | ------------------- |
| `/health`                  | GET    | Health check        |
| `/api/v1/chat`             | POST   | Send chat message   |
| `/api/v1/feedback`         | POST   | Submit feedback     |
| `/api/v1/documents/upload` | POST   | Upload PDF document |
| `/api/v1/documents`        | GET    | List documents      |

## Development Status

- [x] Phase 0: Project Setup
- [x] Phase 1: Backend Development
- [ ] Phase 2: Frontend Enhancement
- [ ] Phase 3: Testing & Optimization
- [ ] Phase 4: Internal Deployment
- [ ] Phase 5: Mobile App

## License

Internal use only - RSUP Prof. dr. I.G.N.G. Ngoerah

## Contributors

- Tim IT RSUP Sanglah
