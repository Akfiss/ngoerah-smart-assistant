# 🛠️ Developer Guide - Ngoerah Smart Assistant

Panduan lengkap untuk development dan menjalankan project.

## 📋 Prerequisites

| Software   | Version | Keterangan         |
| ---------- | ------- | ------------------ |
| Python     | 3.11+   | Runtime            |
| PostgreSQL | 15+     | Database           |
| Ollama     | Latest  | LLM Server         |
| Redis      | Latest  | Caching (optional) |
| Git        | Latest  | Version control    |

---

## 🚀 Quick Start

### 1. Clone & Setup Environment

```bash
# Clone repository
git clone https://github.com/Akfiss/ngoerah-smart-assistant.git
cd ngoerah-smart-assistant

# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\venv\Scripts\activate.bat

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt
```

### 2. Setup Database

```sql
-- Login PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE ngoerah_assistant;

-- Connect & enable extensions
\c ngoerah_assistant
-- CREATE EXTENSION vector;  -- Optional if pgvector installed
```

```bash
# Create tables
cd backend
python setup_db.py
```

### 3. Configure Environment

```bash
# Copy example config
cp backend/.env.example backend/.env

# Edit .env dengan credentials yang benar
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ngoerah_assistant
```

### 4. Pull LLM Model

```bash
ollama pull llama3.1:8b
```

---

## 🏃 Running the Application

### Backend (FastAPI)

```bash
cd backend

# Activate virtual environment
..\venv\Scripts\Activate.ps1    # Windows PowerShell
# atau
source ../venv/bin/activate      # Linux/Mac

# Run development server
uvicorn app.main:app --reload --port 8000

# Run with custom host (accessible from network)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Access:**

- API Root: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

### Frontend (Streamlit)

```bash
cd frontend

# Activate virtual environment (if not already)
..\venv\Scripts\Activate.ps1

# Run Streamlit
streamlit run streamlit_app.py

# Run with custom port
streamlit run streamlit_app.py --server.port 8502
```

**Access:** http://localhost:8501

---

## 📄 Document Management

### Upload Documents for RAG

**Via Script (Bulk Upload):**

```bash
cd backend

# Upload semua file dari folder
python upload_docs.py "D:\path\to\documents"

# Default: upload dari panduan-simetriss
python upload_docs.py
```

**Via API:**

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@document.pdf" \
  -F "title=Panduan Jam Besuk" \
  -F "document_type=panduan"
```

**Via Swagger UI:**

1. Buka http://localhost:8000/docs
2. Cari endpoint `/api/v1/documents/upload`
3. Click "Try it out"
4. Upload file PDF

### List Documents

```bash
curl http://localhost:8000/api/v1/documents
```

---

## 🧪 Testing

### Test Services

```bash
cd backend
python tests/test_services.py
```

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Chat endpoint
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Halo"}'

# PowerShell version
$body = @{message="Halo"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method Post -Body $body -ContentType "application/json"
```

---

## 📁 Project Structure

```
ngoerah-smart-assistant/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # DB connection
│   │   ├── models/              # SQLAlchemy models
│   │   ├── routers/             # API endpoints
│   │   │   ├── chat.py          # /api/v1/chat
│   │   │   └── documents.py     # /api/v1/documents
│   │   └── services/            # Business logic
│   │       ├── llm_service.py   # Ollama wrapper
│   │       ├── embedding_service.py
│   │       ├── document_service.py
│   │       ├── vector_search.py
│   │       ├── intent_service.py
│   │       └── rag_service.py   # Main RAG pipeline
│   ├── tests/
│   ├── .env                     # Environment config
│   ├── requirements.txt
│   ├── setup_db.py              # Database setup
│   └── upload_docs.py           # Bulk document upload
├── frontend/
│   └── streamlit_app.py         # Chat UI
├── data/
│   └── documents/               # Uploaded PDFs
├── panduan-simetriss/           # Sample documents
├── PRD.md                       # Product Requirements
├── README.md
└── dev-guide.md                 # This file
```

---

## 🔧 Configuration

### Environment Variables (.env)

| Variable          | Default                                | Description           |
| ----------------- | -------------------------------------- | --------------------- |
| `DATABASE_URL`    | postgresql://...                       | PostgreSQL connection |
| `REDIS_URL`       | redis://localhost:6379/0               | Redis connection      |
| `OLLAMA_URL`      | http://localhost:11434                 | Ollama server         |
| `LLM_MODEL`       | llama3.1:8b                            | LLM model name        |
| `EMBEDDING_MODEL` | sentence-transformers/all-MiniLM-L6-v2 | Embedding model       |
| `DEBUG`           | True                                   | Enable debug mode     |
| `API_PORT`        | 8000                                   | API server port       |

---

## 🐛 Troubleshooting

### Ollama Not Running

```bash
# Start Ollama service
ollama serve

# Check model
ollama list
ollama pull llama3.1:8b
```

### Database Connection Failed

```bash
# Check PostgreSQL running
pg_isready

# Test connection
psql -U postgres -d ngoerah_assistant -c "SELECT 1;"
```

### Port Already in Use

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (Windows)
taskkill /PID <PID> /F
```

### Embedding Model Download Slow

First run akan download model (~90MB). Tunggu sampai selesai.

---

## 📝 Git Workflow

```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "feat: add new feature"

# Push
git push origin main
```

---

## 📚 API Reference

See full API documentation at:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Main Endpoints

| Method | Endpoint                   | Description       |
| ------ | -------------------------- | ----------------- |
| GET    | `/health`                  | Health check      |
| GET    | `/health/detailed`         | Detailed health   |
| POST   | `/api/v1/chat`             | Send chat message |
| POST   | `/api/v1/feedback`         | Submit feedback   |
| POST   | `/api/v1/documents/upload` | Upload document   |
| GET    | `/api/v1/documents`        | List documents    |
| GET    | `/api/v1/stats`            | Usage statistics  |

---

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test locally
4. Commit with descriptive message
5. Push and create PR

---

_Last updated: January 2026_
