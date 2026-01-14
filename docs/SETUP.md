# Ngoerah Smart Assistant - Setup Guide

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Redis
- Ollama with Llama 3.1:8b model

### Installation

1. **Clone repository**

   ```bash
   git clone https://github.com/your-repo/chatbot-ngoerah.git
   cd chatbot-ngoerah
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Setup environment**

   ```bash
   cp backend/.env.example backend/.env
   # Edit .env with your configuration
   ```

5. **Start services**

   ```bash
   # Terminal 1: Start Redis
   redis-server

   # Terminal 2: Start Ollama
   ollama serve

   # Terminal 3: Start Backend
   cd backend
   uvicorn app.main:app --reload

   # Terminal 4: Start Frontend
   streamlit run frontend/streamlit_app.py
   ```

6. **Access application**
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Frontend: http://localhost:8501

## Project Structure

```
chatbot-ngoerah/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routers/         # API endpoints
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helper functions
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   └── streamlit_app.py
├── data/
│   ├── documents/           # PDF storage
│   └── sample_data/
└── docs/
```
