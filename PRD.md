# 🏥 Ngoerah Smart Assistant - Complete PRD & Development Guide

> **Product Requirements Document & Project Todolist**
>
> **Status:** Prototype / Minimum Viable Product (MVP)  
> **Version:** 2.0.0 (AI-Native Architecture)  
> **Division:** IT Department - RSUP Prof. dr. I.G.N.G. Ngoerah  
> **Prepared By:** Tim IT RSUP Sanglah  
> **Last Updated:** January 13, 2026

---

## 📋 Table of Contents

### Part A: Product Requirements Document

1. [Executive Summary](#1-executive-summary)
2. [Background & Problem Analysis](#2-background--problem-analysis)
3. [Project Objectives & Goals](#3-project-objectives--goals)
4. [Architecture Concept](#4-architecture-concept-the-brain--the-mouth)
5. [Technical Specifications](#5-technical-specifications)
6. [Functional Features](#6-functional-features-mvp-scope)
7. [User Stories & Use Cases](#7-user-stories--use-cases)
8. [System Workflow](#8-system-workflow)
9. [Database Design](#9-database-design)
10. [API Documentation](#10-api-documentation)
11. [Security & Privacy](#11-security--privacy)
12. [Performance & Scalability](#12-performance--scalability)
13. [Testing Strategy](#13-testing-strategy)
14. [Success Metrics & KPIs](#14-success-metrics--kpis)
15. [Risk Assessment](#15-risk-assessment--mitigation)

### Part B: Project Development Todolist

16. [Phase 0: Project Setup & Preparation](#phase-0-project-setup--preparation)
17. [Phase 1: Backend Development (The Brain)](#phase-1-backend-development-the-brain)
18. [Phase 2: Frontend Development - Streamlit (The Mouth v1)](#phase-2-frontend-development---streamlit)
19. [Phase 3: Testing & Optimization](#phase-3-testing--optimization)
20. [Phase 4: Internal Deployment & UAT](#phase-4-internal-deployment--uat)
21. [Phase 5: Mobile App Development - Flutter (The Mouth v2)](#phase-5-mobile-app-development---flutter)
22. [Phase 6: Production Deployment](#phase-6-production-deployment)

---

# Part A: Product Requirements Document

## 1. Executive Summary

### 1.1. Project Overview

**Ngoerah Smart Assistant** adalah asisten virtual bertenaga Generative AI yang dirancang untuk meningkatkan efisiensi layanan informasi di RSUP Prof. dr. I.G.N.G. Ngoerah. Sistem ini menggunakan teknologi **Llama 3** dengan metode **RAG (Retrieval-Augmented Generation)** untuk memberikan jawaban akurat dan kontekstual berdasarkan basis pengetahuan internal rumah sakit.

### 1.2. Key Differentiators

| Aspek                | Chatbot Konvensional           | Ngoerah Smart Assistant                    |
| -------------------- | ------------------------------ | ------------------------------------------ |
| **Pemahaman Bahasa** | Keyword-based (kaku)           | Natural Language Understanding (fleksibel) |
| **Akurasi Jawaban**  | Template statis                | Dynamic, context-aware (RAG)               |
| **Pembaruan Konten** | Manual edit script             | Upload PDF/dokumen baru                    |
| **Data Privacy**     | Cloud-based (risiko kebocoran) | On-Premise (aman, data tidak keluar RS)    |
| **Biaya Lisensi**    | Mahal (subscription)           | Rp 0,- (Open Source)                       |
| **Maintenance**      | Vendor dependent               | In-house control                           |
| **Skalabilitas**     | Terbatas                       | Mudah dikembangkan (modular)               |
| **Halusinasi AI**    | N/A                            | Diminimalisir dengan RAG                   |

### 1.3. Target Users

1. **Primary Users:**

   - Pasien & Keluarga Pasien
   - Calon Pasien (prospective patients)

2. **Secondary Users:**

   - Staf Non-Medis (front desk, customer service)
   - Staf Medis (untuk info cepat prosedur internal)

3. **Tertiary Users:**
   - Management (untuk monitoring & analytics)

### 1.4. Business Value

- **Cost Reduction:** Mengurangi beban kerja call center hingga 60-70%
- **24/7 Availability:** Layanan informasi tanpa batas waktu
- **Improved Patient Experience:** Response time < 5 detik
- **Scalability:** Dapat melayani unlimited concurrent users
- **Data-Driven Insights:** Analytics untuk improvement berkelanjutan

---

## 2. Background & Problem Analysis

### 2.1. Current State Analysis

#### 2.1.1. Pain Points Identified

**A. Operational Challenges:**

1. **Overload Pertanyaan Repetitif (80% dari total inquiries)**

   - Jadwal praktek dokter
   - Jam besuk
   - Persyaratan BPJS
   - Lokasi ruang/poli
   - Biaya layanan

2. **Keterbatasan SDM:**

   - Call center beroperasi 08:00-16:00 (8 jam/hari)
   - Kebutuhan informasi pasien: 24/7
   - Ratio staff:pasien tidak ideal (1:200+)

3. **Kesulitan Navigasi Digital:**
   - Website RS overloaded dengan informasi
   - Menu pendaftaran online "terkubur" dalam hierarki kompleks
   - Bounce rate tinggi pada halaman registrasi (>40%)

**B. Patient Impact:**

- Waktu tunggu call center rata-rata: 5-10 menit
- Tingkat kepuasan layanan informasi: 6.5/10
- Komplain terkait sulit akses informasi: 30+ per bulan

**C. Staff Impact:**

- Burnout rate tinggi pada staff front desk
- 70% waktu kerja habis untuk pertanyaan repetitif
- Terhambatnya pekerjaan administratif kompleks

### 2.2. Solution Approach

#### 2.2.1. Proposed Solution

Mengembangkan **AI-Powered Virtual Assistant** dengan karakteristik:

1. **Intelligent & Contextual:**

   - Memahami bahasa natural (tidak harus keyword persis)
   - Dapat menangani variasi pertanyaan
   - Memberikan jawaban kontekstual

2. **Accurate & Trustworthy:**

   - Menggunakan RAG untuk grounding jawaban pada dokumen resmi
   - Menghindari "hallucination" (jawaban mengada-ada)
   - Cite sources untuk transparansi

3. **Secure & Compliant:**

   - On-premise deployment (data tidak keluar RS)
   - Compliant dengan regulasi privasi data kesehatan
   - Audit trail untuk accountability

4. **Cost-Effective:**
   - Open-source stack (zero licensing fee)
   - Leverage existing server infrastructure
   - Minimal training cost untuk maintenance

#### 2.2.2. Why AI/RAG Instead of Rule-Based?

| Skenario                                             | Rule-Based Chatbot               | RAG-Based AI                         |
| ---------------------------------------------------- | -------------------------------- | ------------------------------------ |
| "Jam besuk kapan?"                                   | ✅ Bisa jawab                    | ✅ Bisa jawab                        |
| "Kalau saya mau jenguk kakak saya jam berapa boleh?" | ❌ Bingung (pattern tidak match) | ✅ Bisa jawab (paham konteks)        |
| "Dokter anak praktek hari apa?"                      | ✅ Bisa jawab                    | ✅ Bisa jawab                        |
| "Anak saya batuk mau periksa ke dokter siapa ya?"    | ❌ Tidak bisa                    | ✅ Bisa (rekomendasikan dokter anak) |
| **Update Info (misal: jadwal berubah)**              | Manual edit 50+ rules            | Upload dokumen baru (auto re-index)  |

---

## 3. Project Objectives & Goals

### 3.1. Primary Objectives

1. **Efficiency Goal:**

   - Mengurangi beban call center hingga 60% untuk pertanyaan repetitif
   - Response time < 5 detik untuk 90% queries

2. **Availability Goal:**

   - Menyediakan layanan informasi 24/7/365
   - Uptime target: 99.5%

3. **User Satisfaction Goal:**

   - Meningkatkan skor kepuasan layanan informasi dari 6.5 → 8.5/10
   - Resolution rate (first contact): > 80%

4. **Cost Efficiency:**
   - MVP development dengan budget Rp 0,- (open source)
   - Proof of concept dalam 3 bulan

### 3.2. Success Criteria (MVP)

| Metric                | Target         | Measurement Method               |
| --------------------- | -------------- | -------------------------------- |
| **Accuracy Rate**     | > 85%          | Manual evaluation 100 sample Q&A |
| **Response Time**     | < 5 detik      | Average API latency              |
| **User Satisfaction** | > 7.5/10       | Post-chat survey                 |
| **Query Resolution**  | > 75%          | Follow-up needed rate            |
| **System Uptime**     | > 99%          | Monitoring logs (1 month)        |
| **Adoption Rate**     | > 50 users/day | Usage analytics (internal phase) |

### 3.3. Out of Scope (MVP)

❌ **Not Included in MVP:**

- Transactional features (pendaftaran langsung via chat)
- Integration dengan SIMRS untuk data real-time
- Multi-language support (hanya Bahasa Indonesia)
- Voice interface
- WhatsApp integration (ditargetkan Phase 2)
- Pembayaran online
- Video call dengan dokter

---

## 4. Architecture Concept: "The Brain & The Mouth"

### 4.1. Design Philosophy

Sistem dirancang dengan prinsip **Separation of Concerns** untuk menjamin:

- **Flexibility:** Mudah ganti interface tanpa mengubah core logic
- **Maintainability:** Backend & frontend dapat dikembangkan paralel
- **Scalability:** Tiap layer dapat di-scale independen

```
┌─────────────────────────────────────────────────────────┐
│                    THE SYSTEM                           │
│                                                         │
│  ┌─────────────────────┐      ┌──────────────────────┐ │
│  │   THE MOUTH         │      │     THE BRAIN        │ │
│  │  (Interface Layer)  │◄────►│   (Core Logic)       │ │
│  │                     │      │                      │ │
│  │  • Streamlit (MVP)  │      │  • FastAPI           │ │
│  │  • Flutter (Phase2) │      │  • RAG Engine        │ │
│  │  • WhatsApp (Future)│      │  • LLM (Llama 3)     │ │
│  └─────────────────────┘      │  • Vector DB         │ │
│                               └──────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 4.2. The Brain (Backend Core)

**Responsibilities:**

- Natural Language Understanding (NLU)
- Intent classification
- Retrieval-Augmented Generation (RAG)
- Response generation
- Session management
- Analytics & logging

**Key Characteristics:**

- **Platform Agnostic:** Tidak peduli interface yang digunakan
- **RESTful API:** Communicate via standard HTTP/JSON
- **Stateless:** Setiap request independen (untuk scalability)
- **Modular:** Tiap komponen (intent detection, RAG, LLM) terpisah

### 4.3. The Mouth (Interface Layer)

**Phase 1 (MVP): Streamlit Web App**

- **Purpose:** Internal demo & testing
- **Users:** Staff RS, management (closed beta)
- **Pros:** Rapid development (2-3 hari), zero cost, Python native
- **Cons:** Tidak cocok untuk public-facing, limited customization

**Phase 2: Flutter Mobile App**

- **Purpose:** External user (pasien & keluarga)
- **Platform:** Android & iOS
- **Pros:** Native performance, better UX, offline capability
- **Cons:** Development time lebih lama (4-6 minggu)

**Phase 3 (Future): WhatsApp Business API**

- **Purpose:** Reach broader audience
- **Platform:** WhatsApp
- **Pros:** High adoption rate (90%+ pasien punya WA)
- **Cons:** Ada biaya lisensi (~Rp 5-10 juta/bulan)

### 4.4. Data Flow Architecture

```mermaid
graph LR
    A[User Input] --> B{Interface Layer}
    B -->|HTTP POST| C[FastAPI Gateway]
    C --> D[Intent Classifier]
    D -->|FAQ Query| E[RAG Pipeline]
    D -->|Registration Intent| F[Navigation Handler]
    E --> G[Vector DB Search]
    G --> H[Context Retrieval]
    H --> I[LLM Generation]
    I --> J[Response Formatter]
    F --> J
    J --> C
    C -->|HTTP Response| B
    B --> K[User Output]

    style E fill:#e1f5ff
    style I fill:#fff3e1
    style G fill:#f0f0f0
```

---

## 5. Technical Specifications

### 5.1. Complete Tech Stack

| Layer                  | Component        | Technology            | Version          | Rationale                                        |
| ---------------------- | ---------------- | --------------------- | ---------------- | ------------------------------------------------ |
| **AI Model**           | LLM              | Llama 3 (via Ollama)  | 3.1 (8B)         | Open-source, on-premise, good Indonesian support |
|                        | Embedding Model  | sentence-transformers | all-MiniLM-L6-v2 | Fast, lightweight, multilingual                  |
|                        | RAG Framework    | LangChain             | 0.1.x            | Production-ready, extensive tooling              |
| **Backend**            | API Framework    | FastAPI               | 0.109.x          | Async, fast, auto-documentation                  |
|                        | Task Queue       | Celery + Redis        | Latest           | Handle async tasks (document processing)         |
|                        | Caching          | Redis                 | 7.x              | Session cache, rate limiting                     |
| **Database**           | Primary DB       | PostgreSQL            | 15.x             | Transactional data, analytics                    |
|                        | Vector Extension | pgvector              | 0.5.x            | Native vector similarity search                  |
| **Frontend (Phase 1)** | Web UI           | Streamlit             | 1.30.x           | Rapid prototyping                                |
| **Frontend (Phase 2)** | Mobile App       | Flutter               | 3.16.x           | Cross-platform (Android/iOS)                     |
|                        | State Management | Riverpod              | 2.4.x            | Reactive, scalable                               |
|                        | HTTP Client      | Dio                   | 5.4.x            | REST API communication                           |
| **DevOps**             | Containerization | Docker                | 24.x             | Consistent environments                          |
|                        | Orchestration    | Docker Compose        | 2.x              | Multi-container management                       |
|                        | Monitoring       | Prometheus + Grafana  | Latest           | Performance metrics                              |
|                        | Logging          | ELK Stack             | 8.x              | Centralized logging                              |
| **Infrastructure**     | Server OS        | Ubuntu Server         | 22.04 LTS        | Stable, long-term support                        |
|                        | Web Server       | Nginx                 | Latest           | Reverse proxy, load balancing                    |
|                        | Process Manager  | Supervisor            | Latest           | Keep services running                            |

### 5.2. System Requirements

#### 5.2.1. Server Requirements (Minimum)

**Backend Server:**

- **CPU:** 8 cores (Intel Xeon or AMD EPYC recommended)
- **RAM:** 32 GB (16 GB for LLM, 8 GB for DB, 8 GB for OS/cache)
- **Storage:** 500 GB SSD (100 GB for models, 200 GB for DB, 200 GB for logs/backup)
- **GPU:** Optional (NVIDIA with CUDA for faster inference)
- **Network:** 1 Gbps (internal network)

**Database Server:**

- **CPU:** 4 cores
- **RAM:** 16 GB
- **Storage:** 1 TB SSD (scalable)

**Note:** Untuk MVP, bisa menggunakan 1 server untuk semua komponen (monolithic), tapi untuk production sebaiknya dipisah.

#### 5.2.2. Client Requirements

**Streamlit Web App:**

- Browser modern (Chrome 90+, Firefox 88+, Safari 14+)
- Internet connection: > 1 Mbps
- Screen resolution: > 1280x720

**Flutter Mobile App:**

- **Android:** Version 8.0+ (API Level 26+)
- **iOS:** Version 12.0+
- RAM: > 2 GB
- Storage: 50 MB (app size)

### 5.3. Development Environment

```yaml
# Recommended Development Setup

IDE:
  - Backend: VS Code / PyCharm
  - Frontend (Flutter): Android Studio / VS Code with Flutter extension

Version Control:
  - Git (with GitHub/GitLab)

Python Environment:
  - Python 3.11+
  - Virtual Environment (venv or conda)

Flutter Setup:
  - Flutter SDK 3.16+
  - Android SDK
  - Xcode (for iOS development)

Docker:
  - Docker Desktop (for local testing)
```

---

## 6. Functional Features (MVP Scope)

### 6.1. Core Features

#### F-01: Smart FAQ (RAG-Based)

**Description:**  
Menjawab pertanyaan umum tentang rumah sakit menggunakan RAG untuk memastikan akurasi dan grounding pada dokumen resmi.

**User Flow:**

```
User: "Jam besuk ICU jam berapa?"
↓
System:
1. Detect intent: INFO_QUERY
2. Convert query to embedding
3. Search vector DB untuk dokumen relevan
4. Retrieve top 3 chunks (similarity > 0.7)
5. Send to LLM with prompt: "Answer based on these documents..."
↓
Response: "Jam besuk ICU di RSUP Sanglah adalah pukul 11.00-12.00
dan 17.00-18.00 setiap hari. Maksimal 2 pengunjung per pasien."
```

**Supported Query Types:**

- Jadwal praktek dokter
- Jadwal poliklinik
- Jam besuk (reguler, ICU, NICU)
- Persyaratan administrasi (BPJS, Umum)
- Fasilitas RS (parkir, kantin, ATM, musholla)
- Biaya layanan (range estimasi)
- Lokasi ruangan/poli
- Prosedur medis umum

**Technical Specifications:**

- **Input:** Text (max 500 characters)
- **Output:** Text response + source references
- **Max Response Time:** 5 seconds
- **Confidence Threshold:** 0.7 (if below, return "Maaf, saya kurang yakin...")

**Error Handling:**
| Error Case | System Behavior |
|------------|-----------------|
| Query terlalu pendek (<5 chars) | "Mohon berikan pertanyaan yang lebih jelas" |
| No relevant documents found | "Maaf, saya tidak menemukan informasi tentang itu. Silakan hubungi [contact info]" |
| Ambiguous query | "Apakah yang Anda maksud: [option 1] atau [option 2]?" |
| Offensive language detected | "Mohon gunakan bahasa yang sopan" |

#### F-02: Smart Navigation (Registration)

**Description:**  
Mendeteksi niat user untuk mendaftar/booking dan mengarahkan ke halaman yang tepat tanpa memproses data sensitif di chat.

**User Flow:**

```
User: "Saya mau daftar periksa ke dokter anak"
↓
System:
1. Detect intent: REGISTRATION
2. Classify sub-intent: POLIKLINIK (anak)
3. Generate deeplink: https://simrs.sanglah.go.id/daftar?poli=anak
↓
Response: "Baik, untuk pendaftaran ke Poliklinik Anak, silakan
klik link berikut: [Button: Daftar Sekarang]

Atau scan QR code ini: [QR Code]

Jam layanan pendaftaran: 07.00 - 14.00"
```

**Supported Navigation Targets:**

- Pendaftaran poliklinik (by specialty)
- Pendaftaran IGD
- Cek nomor antrean
- Riwayat kunjungan
- Hasil lab online
- Pembayaran online

**Technical Specifications:**

- **Input:** Natural language intent
- **Output:** Deeplink + QR code + instructions
- **Security:** No PII (Personal Identifiable Information) handled in chat

#### F-03: Conversation History (Session Management)

**Description:**  
Menyimpan konteks percakapan untuk pengalaman yang lebih natural.

**Features:**

- Remember previous questions (last 5 messages)
- Context-aware follow-up questions
- Session timeout: 30 minutes inactive

**Example:**

```
User: "Jam besuk ICU kapan?"
Bot: "Jam besuk ICU adalah 11.00-12.00 dan 17.00-18.00"

User: "Boleh bawa anak kecil?"
Bot: "Untuk ICU, pengunjung anak di bawah 12 tahun tidak diperbolehkan
masuk demi keamanan pasien dan anak itu sendiri."
```

#### F-04: Feedback Mechanism

**Description:**  
User dapat memberikan feedback untuk continuous improvement.

**Features:**

- 👍 👎 buttons setelah setiap response
- Optional text feedback: "What could be better?"
- Data stored untuk retraining

### 6.2. Admin Features

#### A-01: Document Management

**Features:**

- Upload PDF dokumen (pedoman, SOP, pengumuman)
- Auto-processing: Extract text → Chunk → Embed → Store
- Version control (track changes)
- Bulk upload

**UI Components:**

- File uploader
- Processing status indicator
- Document library (list dengan search)
- Preview dokumen

#### A-02: Analytics Dashboard

**Metrics:**

- Total queries (daily, weekly, monthly)
- Top 10 pertanyaan
- Unresolved queries (confidence < threshold)
- Response time average
- User satisfaction score
- Peak hours

**Visualizations:**

- Line chart: Query volume over time
- Bar chart: Query categories
- Heatmap: Activity by hour/day
- Word cloud: Common keywords

#### A-03: System Monitoring

**Metrics:**

- API latency
- LLM inference time
- Database query time
- Error rate
- Server resources (CPU, RAM, disk)

---

## 7. User Stories & Use Cases

### 7.1. Patient Personas

#### Persona 1: Ibu Dewi (35 tahun)

- **Background:** Ibu rumah tangga, anak sakit, perlu info cepat
- **Tech Savviness:** Medium
- **Goals:** Cari dokter anak yang praktek hari ini, jadwal, cara daftar
- **Pain Points:** Website RS terlalu kompleks, call center sering sibuk

**User Stories:**

```
AS a mother with a sick child
I WANT to quickly find which pediatrician is available today
SO THAT I can register without wasting time on hold
```

#### Persona 2: Pak Wayan (50 tahun)

- **Background:** Pegawai swasta, ayah dirawat di ICU
- **Tech Savviness:** Low-Medium
- **Goals:** Tahu jam besuk, apa yang boleh dibawa, prosedur visit
- **Pain Points:** Tidak punya waktu datang ke RS hanya untuk tanya info

**User Stories:**

```
AS a family member of ICU patient
I WANT to know visiting hours and rules without calling
SO THAT I can plan my visit efficiently
```

#### Persona 3: Made (28 tahun)

- **Background:** Mahasiswa, first-time patient
- **Tech Savviness:** High
- **Goals:** Daftar online, cek biaya, lokasi poli
- **Pain Points:** Bingung navigasi sistem registrasi online

**User Stories:**

```
AS a first-time patient
I WANT a simple way to register online
SO THAT I don't have to come early just to queue
```

### 7.2. Use Case Scenarios

#### Use Case 1: Info Jadwal Dokter

```
Title: Check Doctor's Schedule
Actor: Patient (Ibu Dewi)
Precondition: User has access to chatbot
Main Flow:
  1. User opens chatbot
  2. User types: "Dokter anak siapa yang praktek besok?"
  3. System detects intent: INFO_QUERY (doctor schedule)
  4. System searches knowledge base for pediatrician schedule
  5. System returns: "Besok (Selasa) dokter anak yang praktek:
     - dr. Ketut Suarta, Sp.A (08.00-12.00)
     - dr. Made Kardana, Sp.A (14.00-16.00)"
  6. User satisfied, closes chat
Postcondition: User has the information needed
Alternative Flow:
  - If no doctor available: System suggests alternative dates
  - If user wants to register: System provides deeplink
```

#### Use Case 2: Registration Navigation

```
Title: Navigate to Registration
Actor: Patient (Made)
Precondition: User wants to register
Main Flow:
  1. User types: "Saya mau daftar"
  2. System detects intent: REGISTRATION
  3. System asks: "Mau daftar untuk layanan apa? Poliklinik atau IGD?"
  4. User selects: "Poliklinik"
  5. System asks: "Poliklinik apa? (Umum/Gigi/Mata/dll)"
  6. User selects: "Umum"
  7. System provides:
     - Deeplink button
     - QR code
     - Text instructions
  8. User clicks button → redirected to registration form
Postcondition: User reaches registration page
```

#### Use Case 3: Multi-turn Conversation

```
Title: Context-Aware Follow-up
Actor: Patient (Pak Wayan)
Precondition: Active conversation session
Main Flow:
  1. User: "Jam besuk ICU jam berapa?"
  2. Bot: "Jam besuk ICU 11.00-12.00 dan 17.00-18.00"
  3. User: "Boleh bawa makanan?"
  4. Bot (understands context = ICU): "Untuk ICU, makanan dari
     luar tidak diperbolehkan. Nutrisi pasien diatur tim medis."
  5. User: "Parkir dimana?"
  6. Bot: "Parkir pengunjung tersedia di basement gedung utama..."
Postcondition: User gets comprehensive info in natural conversation
```

---

## 8. System Workflow

### 8.1. High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        A1[Streamlit Web App]
        A2[Flutter Mobile App]
        A3[Future: WhatsApp]
    end

    subgraph "API Gateway Layer"
        B[Nginx Reverse Proxy]
        C[FastAPI Backend]
    end

    subgraph "Application Layer"
        D[Intent Classifier]
        E[RAG Engine]
        F[Session Manager]
        G[Navigation Handler]
    end

    subgraph "AI Layer"
        H[Llama 3 LLM via Ollama]
        I[Embedding Model]
    end

    subgraph "Data Layer"
        J[(PostgreSQL + pgvector)]
        K[(Redis Cache)]
        L[Document Storage]
    end

    subgraph "Admin Layer"
        M[Admin Dashboard]
        N[Analytics Engine]
    end

    A1 & A2 & A3 --> B
    B --> C
    C --> D & F
    D --> E
    D --> G
    E --> I
    E --> J
    E --> H
    F --> K
    G --> J
    L --> E
    M --> C
    N --> J

    style E fill:#e1f5ff
    style H fill:#fff3e1
    style J fill:#f0f0f0
```

### 8.2. Detailed RAG Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as Frontend
    participant API as FastAPI
    participant Intent as Intent Classifier
    participant Cache as Redis
    participant Embed as Embedding Model
    participant VDB as Vector DB
    participant LLM as Llama 3
    participant Log as Analytics DB

    User->>UI: Enter question
    UI->>API: POST /api/v1/chat

    rect rgb(240, 248, 255)
        Note over API,Intent: Step 1: Intent Detection
        API->>Intent: Classify intent
        Intent->>LLM: Quick classification prompt
        LLM-->>Intent: Intent type + confidence
        Intent-->>API: Result: FAQ_QUERY (0.95)
    end

    alt Intent = REGISTRATION
        API->>API: Generate deeplink
        API-->>UI: Return navigation response
        UI-->>User: Show link/QR code
    else Intent = FAQ_QUERY
        rect rgb(255, 250, 240)
            Note over API,VDB: Step 2: Check Cache
            API->>Cache: Check if query cached
            alt Cache Hit
                Cache-->>API: Return cached response
            else Cache Miss
                Note over Embed,VDB: Step 3: Retrieval
                API->>Embed: Convert query to vector
                Embed-->>API: Embedding [768 dims]
                API->>VDB: Similarity search (top_k=5)
                VDB-->>API: Relevant chunks + metadata

                Note over API,LLM: Step 4: Generation
                API->>API: Build prompt with context
                API->>LLM: Generate response
                LLM-->>API: Natural language answer

                API->>Cache: Cache response (TTL 1hr)
            end
        end

        API->>Log: Log query + response + metadata
        API-->>UI: JSON response + sources
        UI-->>User: Display formatted answer
    end

    User->>UI: Rate response (👍/👎)
    UI->>API: POST /api/v1/feedback
    API->>Log: Store feedback
```

### 8.3. Document Processing Pipeline

```mermaid
flowchart TD
    A[Admin Upload PDF] --> B{Validate File}
    B -->|Invalid| C[Return Error]
    B -->|Valid| D[Extract Text<br/>PyPDF2/pdfplumber]
    D --> E[Clean & Preprocess<br/>Remove headers/footers]
    E --> F[Text Chunking<br/>Semantic splitting]
    F --> G[Generate Metadata<br/>Title, page, date]
    G --> H[Create Embeddings<br/>sentence-transformers]
    H --> I[Store in Vector DB<br/>PostgreSQL pgvector]
    I --> J[Update Search Index]
    J --> K[Notify Admin:<br/>✅ Processing Complete]

    style D fill:#e1f5ff
    style H fill:#fff3e1
    style I fill:#f0f0f0
```

---

## 9. Database Design

### 9.1. Database Schema

#### 9.1.1. Core Tables

**Table: `conversations`**

```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    last_activity TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB
);
```

**Table: `messages`**

```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    intent VARCHAR(50),
    confidence FLOAT,
    timestamp TIMESTAMP DEFAULT NOW(),
    response_time_ms INTEGER,
    metadata JSONB
);
```

**Table: `documents`**

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    content TEXT,
    document_type VARCHAR(50), -- 'pedoman', 'sop', 'pengumuman'
    upload_date TIMESTAMP DEFAULT NOW(),
    uploaded_by VARCHAR(100),
    file_size_kb INTEGER,
    page_count INTEGER,
    status VARCHAR(20) DEFAULT 'processing', -- 'processing', 'ready', 'error'
    metadata JSONB
);
```

**Table: `document_chunks`**

```sql
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(384), -- Dimension depends on model
    page_number INTEGER,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create vector similarity search index
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops);
```

**Table: `feedback`**

```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    message_id INTEGER REFERENCES messages(id),
    rating INTEGER CHECK (rating IN (-1, 1)), -- thumbs down or up
    comment TEXT,
    submitted_at TIMESTAMP DEFAULT NOW()
);
```

**Table: `analytics_daily`**

```sql
CREATE TABLE analytics_daily (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    total_queries INTEGER DEFAULT 0,
    avg_response_time_ms INTEGER,
    positive_feedback INTEGER DEFAULT 0,
    negative_feedback INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    top_intents JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 9.2. Sample Queries

```sql
-- Get conversation history
SELECT role, content, timestamp
FROM messages
WHERE conversation_id = 'xxx'
ORDER BY timestamp DESC
LIMIT 10;

-- Vector similarity search
SELECT
    dc.content,
    d.title,
    d.filename,
    1 - (dc.embedding <=> '[query_embedding]'::vector) AS similarity
FROM document_chunks dc
JOIN documents d ON dc.document_id = d.id
WHERE d.status = 'ready'
ORDER BY dc.embedding <=> '[query_embedding]'::vector
LIMIT 5;

-- Daily statistics
SELECT
    date,
    total_queries,
    avg_response_time_ms,
    ROUND(positive_feedback::NUMERIC / NULLIF(positive_feedback + negative_feedback, 0) * 100, 2) as satisfaction_rate
FROM analytics_daily
WHERE date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY date DESC;
```

---

## 10. API Documentation

### 10.1. API Endpoints

**Base URL:** `http://localhost:8000/api/v1`

#### Endpoint: Chat

```http
POST /chat
Content-Type: application/json

Request Body:
{
    "message": "Jam besuk ICU jam berapa?",
    "session_id": "optional-session-id",
    "user_id": "optional-user-id"
}

Response (200 OK):
{
    "response": "Jam besuk ICU adalah pukul 11.00-12.00 dan 17.00-18.00...",
    "intent": "faq_query",
    "confidence": 0.95,
    "sources": [
        {
            "document": "Pedoman_Pasien_2024.pdf",
            "page": 15,
            "relevance": 0.89
        }
    ],
    "session_id": "abc-123-def",
    "response_time_ms": 2341
}

Error Response (400 Bad Request):
{
    "error": "Message too short",
    "message": "Please provide a question with at least 5 characters"
}
```

#### Endpoint: Feedback

```http
POST /feedback
Content-Type: application/json

Request Body:
{
    "message_id": 12345,
    "rating": 1,  // 1 for thumbs up, -1 for thumbs down
    "comment": "Very helpful!"  // optional
}

Response (200 OK):
{
    "status": "success",
    "message": "Thank you for your feedback"
}
```

#### Endpoint: Upload Document (Admin)

```http
POST /admin/documents
Content-Type: multipart/form-data

Request Body:
- file: [PDF file]
- title: "Pedoman Pasien 2024"
- document_type: "pedoman"

Response (200 OK):
{
    "status": "processing",
    "document_id": 42,
    "message": "Document uploaded and processing started"
}
```

#### Endpoint: Get Analytics

```http
GET /admin/analytics?days=30

Response (200 OK):
{
    "total_queries": 1523,
    "avg_response_time": 2845,
    "satisfaction_rate": 87.3,
    "top_queries": [
        {"query": "jam besuk", "count": 234},
        {"query": "jadwal dokter", "count": 198}
    ],
    "daily_stats": [...]
}
```

---

## 11. Security & Privacy

### 11.1. Data Privacy Measures

**Personal Data Handling:**

- ❌ **NO collection** of: Nama, NIK, No. Rekam Medis, Alamat, No. Telp
- ✅ **Anonymous tracking** only: session_id (random UUID)
- ✅ **Optional** user_id untuk registered users (future)
- ✅ Chat history **not** linked to identifiable person

**Data Retention:**

```
- Active conversations: 30 days
- Archived conversations: 90 days (for analytics)
- Feedback data: 1 year
- Analytics aggregates: Permanent (anonymized)
```

### 11.2. Security Implementations

**1. Input Validation:**

```python
# Anti-injection
- Max message length: 500 characters
- Sanitize special characters
- Block SQL injection patterns
- Rate limiting: 10 requests/minute per session
```

**2. Authentication (Admin Panel):**

```python
# Simple JWT-based auth for MVP
- Admin login with username/password
- JWT token expires in 8 hours
- Password hashed with bcrypt
```

**3. Network Security:**

```nginx
# Nginx configuration
- HTTPS only (TLS 1.3)
- CORS policy (whitelist internal domain)
- Hide server version headers
- DDoS protection (rate limiting)
```

**4. On-Premise Deployment:**

- All data stays within hospital network
- No external API calls (OpenAI, Google, etc.)
- Local LLM inference only

---

## 12. Performance & Scalability

### 12.1. Performance Targets

| Metric                | Target     | Measurement        |
| --------------------- | ---------- | ------------------ |
| **API Response Time** | < 3s (p95) | Prometheus metrics |
| **LLM Inference**     | < 2s       | Direct measurement |
| **Vector Search**     | < 500ms    | PostgreSQL logs    |
| **Concurrent Users**  | 50 users   | Load testing       |
| **Throughput**        | 20 req/sec | Locust testing     |

### 12.2. Optimization Strategies

**1. Caching Strategy:**

```python
# Redis cache for common queries
Cache Key: hash(query_normalized)
TTL: 1 hour for FAQ, 5 minutes for dynamic data
Hit Rate Target: > 40%
```

**2. Database Optimization:**

```sql
-- Indexes
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp);
CREATE INDEX idx_documents_status ON documents(status);

-- Connection pooling
Min connections: 5
Max connections: 20
```

**3. LLM Optimization:**

```python
# For personal/small-scale project
- Use quantized model (8-bit) to reduce memory
- Max tokens: 512 (good enough for most answers)
- Temperature: 0.3 (more deterministic, faster)
- Batch size: 1 (one at a time is fine for MVP)
```

### 12.3. Scalability Plan

**Phase 1 (MVP): Single Server**

```
Capacity: ~50 concurrent users
Cost: Rp 0 (use existing server/laptop)
```

**Phase 2 (If Successful): Vertical Scaling**

```
Upgrade RAM: 32GB → 64GB
Add GPU: RTX 4060 (optional, ~Rp 6 juta)
Capacity: ~200 concurrent users
```

**Phase 3 (Production): Horizontal Scaling**

```
Load Balancer + 2 Backend Servers
Separate DB server
Redis cluster
Capacity: 1000+ concurrent users
```

---

## 13. Testing Strategy

### 13.1. Testing Levels

#### Unit Testing

```python
# Test coverage target: > 70%
# Tools: pytest, pytest-cov

Test cases:
- Intent classification accuracy
- Embedding generation
- Vector similarity search
- Response formatting
- Error handling
```

#### Integration Testing

```python
# Test API endpoints end-to-end
# Tools: pytest + httpx

Test cases:
- POST /chat → returns valid response
- Invalid input → returns proper error
- Session management → maintains context
- Database transactions → ACID compliance
```

#### System Testing

```python
# Test complete workflows
# Tools: Selenium (for Streamlit), pytest

Test cases:
- User asks question → gets answer → rates → stored
- Admin uploads PDF → processed → searchable
- Analytics dashboard → displays correct data
```

#### Performance Testing

```python
# Load testing
# Tools: Locust, Apache JMeter

Test scenarios:
- 10 concurrent users (normal load)
- 50 concurrent users (peak load)
- 100 concurrent users (stress test)
```

### 13.2. Test Dataset

**Prepare 100 test questions:**

```
Category breakdown:
- Jadwal/Jam (30 questions)
- Lokasi/Fasilitas (25 questions)
- Prosedur/Syarat (25 questions)
- Biaya (10 questions)
- Emergency/Urgent (10 questions)
```

**Ground truth answers:**

- Manually created reference answers
- Used for accuracy evaluation
- Updated when documents change

---

## 14. Success Metrics & KPIs

### 14.1. Quantitative Metrics

| Metric                | Target (3 months) | Measurement Method                    |
| --------------------- | ----------------- | ------------------------------------- |
| **Accuracy**          | > 85%             | Manual evaluation (100 samples/month) |
| **Response Time**     | < 5 seconds       | Average API latency                   |
| **User Satisfaction** | > 7.5/10          | Post-chat survey                      |
| **Query Resolution**  | > 75%             | % of queries not needing follow-up    |
| **Adoption Rate**     | > 30 users/day    | Unique sessions (internal testing)    |
| **System Uptime**     | > 99%             | Monitoring logs                       |

### 14.2. Qualitative Metrics

**User Feedback:**

- Apakah jawaban mudah dipahami?
- Apakah jawaban sesuai dengan pertanyaan?
- Apakah lebih mudah daripada cara lama (call/visit)?

**Staff Feedback:**

- Apakah workload berkurang?
- Apakah ada pertanyaan yang sering tidak terjawab bot?
- Apa saran improvement?

### 14.3. Success Criteria for Each Phase

**MVP Success (Month 3):**

- ✅ Sistem berjalan stabil 24/7
- ✅ Accuracy > 80%
- ✅ Positive feedback dari 20+ internal testers
- ✅ Management approval untuk lanjut ke mobile app

**Production Success (Month 6):**

- ✅ 100+ users/day menggunakan mobile app
- ✅ 50% reduction in repetitive calls to call center
- ✅ ROI positive (time saved > development time)

---

## 15. Risk Assessment & Mitigation

### 15.1. Technical Risks

| Risk                    | Probability | Impact | Mitigation                                         |
| ----------------------- | ----------- | ------ | -------------------------------------------------- |
| **LLM hallucination**   | Medium      | High   | Use RAG, set confidence threshold, cite sources    |
| **Slow inference time** | Medium      | Medium | Use quantized model, optimize prompts, add caching |
| **Server crashes**      | Low         | High   | Auto-restart with Supervisor, monitoring alerts    |
| **Database corruption** | Low         | High   | Daily backups, transaction logs                    |
| **Out of memory**       | Medium      | Medium | Memory limits, graceful degradation                |

### 15.2. Business Risks

| Risk                                | Probability | Impact   | Mitigation                                         |
| ----------------------------------- | ----------- | -------- | -------------------------------------------------- |
| **Low adoption rate**               | Medium      | Medium   | Internal training, clear communication of benefits |
| **Incorrect information**           | Low         | Critical | Manual review of documents, version control        |
| **Privacy concerns**                | Low         | High     | Clear privacy policy, anonymous tracking only      |
| **Competition from existing tools** | Low         | Low      | Highlight unique value (RAG, on-premise, free)     |

### 15.3. Personal Project Risks

| Risk                               | Probability | Impact | Mitigation                                               |
| ---------------------------------- | ----------- | ------ | -------------------------------------------------------- |
| **Time constraint** (side project) | High        | Medium | Focus on MVP only, skip nice-to-have features            |
| **Limited resources** (1 person)   | High        | Medium | Use pre-built tools (LangChain), avoid reinventing wheel |
| **Knowledge gaps** (new tech)      | Medium      | Low    | Allocate learning time, use ChatGPT/docs extensively     |
| **Burnout**                        | Medium      | High   | Set realistic timeline, work in sprints, take breaks     |
| **Hardware limitations**           | Medium      | Medium | Use smaller model (3B/8B), optimize for local machine    |

---

# Part B: Project Development Todolist

## 16. Phase 0: Project Setup & Preparation

**Duration:** 3-5 days  
**Goal:** Setup development environment dan project structure

### 📋 Checklist

#### Day 1: Environment Setup

- [x] **Install Python 3.11+**

  ```bash
  # Verify installation
  python --version
  ```

- [x] **Install Ollama & Download Llama 3**

  ```bash
  # Download from ollama.ai
  curl https://ollama.ai/install.sh | sh

  # Pull Llama 3 model (8B recommended for personal laptop)
  ollama pull llama3.1:8b

  # Test
  ollama run llama3.1:8b "Hello, world!"
  ```

- [x] **Install PostgreSQL**

  ```bash
  # Ubuntu/Debian
  sudo apt install postgresql postgresql-contrib

  # Start service
  sudo systemctl start postgresql

  # Create database
  sudo -u postgres createdb ngoerah_assistant
  ```

- [x] **Install pgvector extension**

  ```bash
  sudo apt install postgresql-15-pgvector

  # Enable in database
  psql -U postgres -d ngoerah_assistant
  CREATE EXTENSION vector;
  ```

- [x] **Install Redis**

  ```bash
  sudo apt install redis-server
  sudo systemctl start redis

  # Test
  redis-cli ping  # Should return "PONG"
  ```

- [x] **Setup Git repository**

  ```bash
  mkdir ngoerah-smart-assistant
  cd ngoerah-smart-assistant
  git init

  # Create .gitignore
  echo "venv/
  __pycache__/
  .env
  *.pyc
  .DS_Store
  uploads/
  *.db" > .gitignore
  ```

#### Day 2: Project Structure

- [x] **Create project directory structure**

  ```bash
  ngoerah-smart-assistant/
  ├── backend/
  │   ├── app/
  │   │   ├── __init__.py
  │   │   ├── main.py              # FastAPI app
  │   │   ├── config.py            # Configuration
  │   │   ├── models/              # Database models
  │   │   ├── routers/             # API endpoints
  │   │   ├── services/            # Business logic
  │   │   │   ├── llm_service.py   # LLM interaction
  │   │   │   ├── rag_service.py   # RAG pipeline
  │   │   │   ├── intent_service.py
  │   │   │   └── document_service.py
  │   │   └── utils/               # Helper functions
  │   ├── tests/
  │   ├── requirements.txt
  │   └── .env.example
  ├── frontend/
  │   └── streamlit_app.py
  ├── data/
  │   ├── documents/               # PDF storage
  │   └── sample_data/
  ├── docs/
  │   ├── API.md
  │   └── SETUP.md
  └── docker-compose.yml           # For later
  ```

- [x] **Create Python virtual environment**

  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

- [x] **Create requirements.txt**

  ```txt
  # Core
  fastapi==0.109.0
  uvicorn[standard]==0.27.0
  pydantic==2.5.0
  python-dotenv==1.0.0

  # Database
  sqlalchemy==2.0.25
  psycopg2-binary==2.9.9
  pgvector==0.2.4
  alembic==1.13.1

  # AI/ML
  langchain==0.1.0
  langchain-community==0.0.10
  sentence-transformers==2.3.1
  pypdf==4.0.1

  # LLM
  ollama==0.1.6

  # Caching
  redis==5.0.1

  # Frontend
  streamlit==1.30.0

  # Utils
  python-multipart==0.0.6
  aiofiles==23.2.1

  # Testing
  pytest==7.4.4
  pytest-asyncio==0.23.3
  httpx==0.26.0
  ```

- [x] **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

#### Day 3: Configuration

- [x] **Create .env file**

  ```bash
  # Database
  DATABASE_URL=postgresql://postgres:password@localhost/ngoerah_assistant

  # Redis
  REDIS_URL=redis://localhost:6379/0

  # Ollama
  OLLAMA_URL=http://localhost:11434
  LLM_MODEL=llama3.1:8b

  # Embedding
  EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

  # App
  DEBUG=True
  API_HOST=0.0.0.0
  API_PORT=8000

  # Security (generate with: openssl rand -hex 32)
  SECRET_KEY=your-secret-key-here
  ```

- [x] **Create config.py**

  ```python
  from pydantic_settings import BaseSettings

  class Settings(BaseSettings):
      DATABASE_URL: str
      REDIS_URL: str
      OLLAMA_URL: str
      LLM_MODEL: str = "llama3.1:8b"
      EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
      DEBUG: bool = True
      SECRET_KEY: str

      class Config:
          env_file = ".env"

  settings = Settings()
  ```

#### Day 4: Database Schema

- [x] **Create Alembic migration**

  ```bash
  alembic init alembic
  ```

- [x] **Create initial migration (create_tables.py)**

  ```python
  # Copy schema from Section 9.1 above
  # Run migration
  alembic revision -m "create initial tables"
  alembic upgrade head
  ```

- [x] **Verify tables created**
  ```bash
  psql -U postgres -d ngoerah_assistant -c "\dt"
  ```

#### Day 5: Hello World Test

- [x] **Create minimal FastAPI app**

  ```python
  # backend/app/main.py
  from fastapi import FastAPI

  app = FastAPI(title="Ngoerah Smart Assistant API")

  @app.get("/")
  def read_root():
      return {"message": "Hello from Ngoerah Assistant!"}

  @app.get("/health")
  def health_check():
      return {"status": "healthy"}
  ```

- [x] **Run FastAPI**

  ```bash
  cd backend
  uvicorn app.main:app --reload

  # Test: http://localhost:8000/docs
  ```

- [x] **Create minimal Streamlit app**

  ```python
  # frontend/streamlit_app.py
  import streamlit as st

  st.title("🏥 Ngoerah Smart Assistant")
  st.write("Asisten Virtual RSUP Sanglah")

  user_input = st.text_input("Tanya apa saja:")
  if st.button("Kirim"):
      st.write(f"Echo: {user_input}")
  ```

- [x] **Run Streamlit**

  ```bash
  streamlit run frontend/streamlit_app.py

  # Opens browser automatically
  ```

- [x] **✅ Checkpoint:** Both apps running successfully

---

## 17. Phase 1: Backend Development (The Brain)

**Duration:** 14-21 days  
**Goal:** Build core RAG engine and API endpoints

### Week 1: LLM & RAG Foundation

#### Day 1-2: LLM Service

- [x] **Create LLM service wrapper**

  ```python
  # backend/app/services/llm_service.py
  import ollama
  from app.config import settings

  class LLMService:
      def __init__(self):
          self.model = settings.LLM_MODEL
          self.client = ollama.Client(host=settings.OLLAMA_URL)

      def generate(self, prompt: str, max_tokens: int = 512) -> str:
          response = self.client.generate(
              model=self.model,
              prompt=prompt,
              options={
                  "temperature": 0.3,
                  "num_predict": max_tokens
              }
          )
          return response['response']

      def test_connection(self) -> bool:
          try:
              self.generate("Hello")
              return True
          except:
              return False
  ```

- [x] **Test LLM service**

  ```python
  # tests/test_llm.py
  from app.services.llm_service import LLMService

  def test_llm_basic():
      llm = LLMService()
      response = llm.generate("What is 2+2?")
      assert len(response) > 0
      print(f"✅ LLM Response: {response}")
  ```

- [x] **Run test:** `pytest tests/test_llm.py -v`

#### Day 3-4: Embedding Service

- [x] **Create embedding service**

  ```python
  # backend/app/services/embedding_service.py
  from sentence_transformers import SentenceTransformer
  import numpy as np

  class EmbeddingService:
      def __init__(self, model_name: str):
          self.model = SentenceTransformer(model_name)
          self.dimension = self.model.get_sentence_embedding_dimension()

      def embed_text(self, text: str) -> list[float]:
          embedding = self.model.encode(text)
          return embedding.tolist()

      def embed_batch(self, texts: list[str]) -> list[list[float]]:
          embeddings = self.model.encode(texts)
          return embeddings.tolist()
  ```

- [x] **Test embedding**
  ```python
  def test_embedding():
      emb = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")
      vector = emb.embed_text("Hello world")
      assert len(vector) == 384  # Model dimension
      print(f"✅ Embedding dimension: {len(vector)}")
  ```

#### Day 5-7: Document Processing

- [x] **Create document processor**

  ```python
  # backend/app/services/document_service.py
  from pypdf import PdfReader
  import re

  class DocumentProcessor:
      def extract_text_from_pdf(self, file_path: str) -> str:
          reader = PdfReader(file_path)
          text = ""
          for page in reader.pages:
              text += page.extract_text()
          return text

      def clean_text(self, text: str) -> str:
          # Remove extra whitespace
          text = re.sub(r'\s+', ' ', text)
          # Remove special characters
          text = re.sub(r'[^\w\s.,!?-]', '', text)
          return text.strip()

      def chunk_text(self, text: str, chunk_size: int = 500,
                     overlap: int = 50) -> list[str]:
          """Split text into overlapping chunks"""
          words = text.split()
          chunks = []

          for i in range(0, len(words), chunk_size - overlap):
              chunk = ' '.join(words[i:i + chunk_size])
              if len(chunk) > 100:  # Minimum chunk size
                  chunks.append(chunk)

          return chunks
  ```

- [x] **Create document upload endpoint**

  ```python
  # backend/app/routers/documents.py
  from fastapi import APIRouter, UploadFile, File
  from app.services.document_service import DocumentProcessor
  from app.services.embedding_service import EmbeddingService
  from app.models import Document, DocumentChunk
  import uuid

  router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
  doc_processor = DocumentProcessor()
  embedding_service = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")

  @router.post("/upload")
  async def upload_document(file: UploadFile = File(...)):
      # Save file
      file_path = f"data/documents/{uuid.uuid4()}_{file.filename}"
      with open(file_path, "wb") as f:
          f.write(await file.read())

      # Process
      text = doc_processor.extract_text_from_pdf(file_path)
      clean_text = doc_processor.clean_text(text)
      chunks = doc_processor.chunk_text(clean_text)

      # Save to database
      doc = Document(filename=file.filename, content=clean_text)
      # db.add(doc) ...

      # Create embeddings
      for idx, chunk in enumerate(chunks):
          embedding = embedding_service.embed_text(chunk)
          chunk_obj = DocumentChunk(
              document_id=doc.id,
              chunk_index=idx,
              content=chunk,
              embedding=embedding
          )
          # db.add(chunk_obj) ...

      return {"status": "success", "chunks": len(chunks)}
  ```

- [x] **Test document upload** with sample PDF

### Week 2: RAG Pipeline

#### Day 8-10: Vector Search

- [x] **Create vector search service**

  ```python
  # backend/app/services/vector_search.py
  from sqlalchemy import text
  from app.database import get_db

  class VectorSearchService:
      def search_similar(self, query_embedding: list[float],
                        top_k: int = 5, threshold: float = 0.7):
          """Find similar document chunks using cosine similarity"""

          query = text("""
              SELECT
                  dc.content,
                  dc.page_number,
                  d.title,
                  d.filename,
                  1 - (dc.embedding <=> :query_vector::vector) AS similarity
              FROM document_chunks dc
              JOIN documents d ON dc.document_id = d.id
              WHERE d.status = 'ready'
                AND 1 - (dc.embedding <=> :query_vector::vector) > :threshold
              ORDER BY dc.embedding <=> :query_vector::vector
              LIMIT :top_k
          """)

          results = db.execute(query, {
              "query_vector": query_embedding,
              "threshold": threshold,
              "top_k": top_k
          })

          return results.fetchall()
  ```

- [x] **Test vector search**

  ```python
  def test_vector_search():
      # Assuming some documents are already indexed
      emb_service = EmbeddingService("...")
      search_service = VectorSearchService()

      query = "Jam besuk ICU"
      query_vec = emb_service.embed_text(query)
      results = search_service.search_similar(query_vec)

      assert len(results) > 0
      print(f"✅ Found {len(results)} relevant chunks")
  ```

#### Day 11-12: Intent Classification

- [x] **Create intent classifier**

  ```python
  # backend/app/services/intent_service.py
  from app.services.llm_service import LLMService

  class IntentClassifier:
      def __init__(self):
          self.llm = LLMService()

      def classify(self, user_message: str) -> dict:
          prompt = f"""Analyze this user message and classify the intent.

  User Message: "{user_message}"

  Possible Intents:
  1. FAQ_QUERY - User asking for information
  2. REGISTRATION - User wants to register/book appointment
  3. EMERGENCY - Urgent medical situation
  4. COMPLAINT - User has a complaint
  5. CHITCHAT - Casual conversation

  Respond ONLY with JSON:
  {{"intent": "FAQ_QUERY", "confidence": 0.95, "reasoning": "brief explanation"}}
  """

          response = self.llm.generate(prompt, max_tokens=100)
          # Parse JSON from response
          import json
          try:
              result = json.loads(response)
              return result
          except:
              return {"intent": "FAQ_QUERY", "confidence": 0.5}
  ```

- [x] **Test intent classification**

  ```python
  def test_intent():
      classifier = IntentClassifier()

      # Test cases
      test_cases = [
          ("Jam besuk ICU jam berapa?", "FAQ_QUERY"),
          ("Saya mau daftar ke dokter anak", "REGISTRATION"),
          ("Halo", "CHITCHAT")
      ]

      for message, expected in test_cases:
          result = classifier.classify(message)
          print(f"Message: {message}")
          print(f"Intent: {result['intent']} (confidence: {result['confidence']})")
          assert result['intent'] == expected
  ```

#### Day 13-14: Complete RAG Pipeline

- [x] **Create RAG service (putting it all together)**

  ```python
  # backend/app/services/rag_service.py
  from app.services.llm_service import LLMService
  from app.services.embedding_service import EmbeddingService
  from app.services.vector_search import VectorSearchService
  from app.services.intent_service import IntentClassifier

  class RAGService:
      def __init__(self):
          self.llm = LLMService()
          self.embedding = EmbeddingService("sentence-transformers/all-MiniLM-L6-v2")
          self.vector_search = VectorSearchService()
          self.intent_classifier = IntentClassifier()

      def process_query(self, user_message: str, session_id: str = None) -> dict:
          # Step 1: Classify intent
          intent_result = self.intent_classifier.classify(user_message)

          if intent_result['intent'] == 'REGISTRATION':
              return self._handle_registration(user_message)

          elif intent_result['intent'] == 'FAQ_QUERY':
              return self._handle_faq(user_message)

          else:
              return {
                  "response": "Maaf, saya belum bisa membantu dengan itu. Coba tanyakan tentang jadwal, fasilitas, atau prosedur RS.",
                  "intent": intent_result['intent']
              }

      def _handle_faq(self, query: str) -> dict:
          # Step 2: Convert query to embedding
          query_embedding = self.embedding.embed_text(query)

          # Step 3: Search similar documents
          search_results = self.vector_search.search_similar(
              query_embedding,
              top_k=3,
              threshold=0.65
          )

          if not search_results:
              return {
                  "response": "Maaf, saya tidak menemukan informasi tentang itu. Silakan hubungi call center di (0361) 227911.",
                  "intent": "FAQ_QUERY",
                  "sources": []
              }

          # Step 4: Build context from retrieved chunks
          context = "\n\n".join([
              f"[Dokumen: {r.filename}, Hal: {r.page_number}]\n{r.content}"
              for r in search_results
          ])

          # Step 5: Generate answer with LLM
          prompt = f"""Kamu adalah asisten virtual RSUP Sanglah. Jawab pertanyaan pasien berdasarkan informasi berikut.
  ```

KONTEKS DARI DOKUMEN RESMI:
{context}

PERTANYAAN PASIEN:
{query}

INSTRUKSI:

- Jawab dalam bahasa Indonesia yang ramah dan mudah dipahami
- Gunakan HANYA informasi dari konteks di atas
- Jika informasi tidak ada, katakan dengan jelas
- Jangan mengarang informasi
- Jawab maksimal 3-4 kalimat

JAWABAN:"""

          answer = self.llm.generate(prompt, max_tokens=300)

          # Step 6: Format sources
          sources = [
              {
                  "document": r.filename,
                  "page": r.page_number,
                  "similarity": round(r.similarity, 2)
              }
              for r in search_results
          ]

          return {
              "response": answer.strip(),
              "intent": "FAQ_QUERY",
              "confidence": search_results[0].similarity if search_results else 0,
              "sources": sources
          }

      def _handle_registration(self, query: str) -> dict:
          # Simple keyword detection for sub-intent
          query_lower = query.lower()

          if any(word in query_lower for word in ['anak', 'pediatri', 'bayi']):
              link = "https://simrs.sanglah.go.id/daftar?poli=anak"
              poli = "Anak"
          elif any(word in query_lower for word in ['gigi', 'dental']):
              link = "https://simrs.sanglah.go.id/daftar?poli=gigi"
              poli = "Gigi"
          elif any(word in query_lower for word in ['mata', 'opthal']):
              link = "https://simrs.sanglah.go.id/daftar?poli=mata"
              poli = "Mata"
          else:
              link = "https://simrs.sanglah.go.id/daftar"
              poli = "Umum"

          response = f"""Baik, untuk pendaftaran ke Poliklinik {poli}, silakan klik link berikut:

🔗 {link}

Atau hubungi:
📞 Call Center: (0361) 227911
⏰ Jam Pendaftaran: 07.00 - 14.00

Dokumen yang perlu disiapkan:

- KTP/Identitas
- Kartu BPJS (jika pakai BPJS)
- Rujukan (jika ada)"""

          return {
              "response": response,
              "intent": "REGISTRATION",
              "registration_link": link,
              "poli": poli
          }

  ```

  ```

- [x] **Test complete RAG pipeline**

  ```python
  def test_rag_pipeline():
      rag = RAGService()

      # Test FAQ
      result = rag.process_query("Jam besuk ICU kapan?")
      print("FAQ Test:")
      print(f"Response: {result['response']}")
      print(f"Sources: {result['sources']}")

      # Test Registration
      result = rag.process_query("Saya mau daftar ke dokter gigi")
      print("\nRegistration Test:")
      print(f"Response: {result['response']}")
      print(f"Link: {result.get('registration_link')}")
  ```

- [x] **✅ Checkpoint:** RAG pipeline working end-to-end

### Week 3: API Endpoints

#### Day 15-17: Main Chat API

- [x] **Create chat endpoint**

  ```python
  # backend/app/routers/chat.py
  from fastapi import APIRouter, HTTPException
  from pydantic import BaseModel
  from app.services.rag_service import RAGService
  from app.models import Message, Conversation
  import time
  import uuid

  router = APIRouter(prefix="/api/v1", tags=["chat"])
  rag_service = RAGService()

  class ChatRequest(BaseModel):
      message: str
      session_id: str = None
      user_id: str = None

  class ChatResponse(BaseModel):
      response: str
      intent: str
      confidence: float = 0.0
      sources: list = []
      session_id: str
      response_time_ms: int

  @router.post("/chat", response_model=ChatResponse)
  async def chat(request: ChatRequest):
      # Validation
      if len(request.message) < 3:
          raise HTTPException(400, "Message too short")

      if len(request.message) > 500:
          raise HTTPException(400, "Message too long (max 500 chars)")

      # Generate session_id if not provided
      session_id = request.session_id or str(uuid.uuid4())

      # Process query
      start_time = time.time()
      result = rag_service.process_query(request.message, session_id)
      response_time_ms = int((time.time() - start_time) * 1000)

      # Save to database (conversation + message)
      # ... database operations ...

      return ChatResponse(
          response=result['response'],
          intent=result['intent'],
          confidence=result.get('confidence', 0),
          sources=result.get('sources', []),
          session_id=session_id,
          response_time_ms=response_time_ms
      )
  ```

- [x] **Add rate limiting**

  ```python
  from fastapi import Request
  from slowapi import Limiter
  from slowapi.util import get_remote_address

  limiter = Limiter(key_func=get_remote_address)

  @router.post("/chat")
  @limiter.limit("10/minute")  # Max 10 requests per minute
  async def chat(request: Request, chat_request: ChatRequest):
      # ... existing code ...
  ```

- [x] **Test chat endpoint**
  ```bash
  curl -X POST http://localhost:8000/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Jam besuk ICU jam berapa?"}'
  ```

#### Day 18: Feedback & Analytics Endpoints

- [x] **Create feedback endpoint**

  ```python
  @router.post("/feedback")
  async def submit_feedback(
      message_id: int,
      rating: int,  # 1 or -1
      comment: str = None
  ):
      # Save to database
      feedback = Feedback(
          message_id=message_id,
          rating=rating,
          comment=comment
      )
      # db.add(feedback) ...

      return {"status": "success", "message": "Thank you for feedback"}
  ```

- [x] **Create analytics endpoint**

  ```python
  @router.get("/admin/analytics")
  async def get_analytics(days: int = 30):
      # Query database for statistics
      stats = {
          "total_queries": 0,  # SELECT COUNT(*) FROM messages ...
          "avg_response_time": 0,
          "satisfaction_rate": 0,
          "top_intents": [],
          "daily_stats": []
      }

      return stats
  ```

#### Day 19-21: Polish & Error Handling

- [x] **Add comprehensive error handling**

  ```python
  from fastapi import HTTPException
  from fastapi.responses import JSONResponse

  @app.exception_handler(Exception)
  async def global_exception_handler(request, exc):
      return JSONResponse(
          status_code=500,
          content={
              "error": "Internal server error",
              "message": str(exc) if app.debug else "Something went wrong"
          }
      )
  ```

- [x] **Add request logging**

  ```python
  import logging

  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[
          logging.FileHandler('logs/app.log'),
          logging.StreamHandler()
      ]
  )
  ```

- [x] **Add health check endpoints**

  ```python
  @router.get("/health")
  def health_check():
      return {
          "status": "healthy",
          "timestamp": datetime.now().isoformat()
      }

  @router.get("/health/detailed")
  def detailed_health():
      return {
          "database": check_database_connection(),
          "redis": check_redis_connection(),
          "llm": check_llm_connection(),
          "disk_space": get_disk_space()
      }
  ```

- [x] **✅ Checkpoint:** Backend API complete and tested

---

## 18. Phase 2: Frontend Development - Streamlit

**Duration:** 5-7 days  
**Goal:** Create user-friendly chat interface

### Day 22-23: Basic Chat Interface

- [ ] **Create Streamlit layout**

  ```python
  # frontend/streamlit_app.py
  import streamlit as st
  import requests
  from datetime import datetime

  # Page config
  st.set_page_config(
      page_title="Ngoerah Smart Assistant",
      page_icon="🏥",
      layout="wide"
  )

  # Custom CSS
  st.markdown("""
  <style>
  .main {
      background-color: #f0f2f6;
  }
  .stTextInput > div > div > input {
      border-radius: 20px;
  }
  .chat-message {
      padding: 1rem;
      border-radius: 10px;
      margin-bottom: 1rem;
  }
  .user-message {
      background-color: #007bff;
      color: white;
      text-align: right;
  }
  .bot-message {
      background-color: white;
      border: 1px solid #ddd;
  }
  </style>
  """, unsafe_allow_html=True)

  # Header
  st.title("🏥 Ngoerah Smart Assistant")
  st.caption("Asisten Virtual RSUP Prof. dr. I.G.N.G. Ngoerah Sanglah")

  # Initialize session state
  if 'messages' not in st.session_state:
      st.session_state.messages = []
      st.session_state.session_id = None

  # Display chat history
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])
          if message["role"] == "assistant" and "sources" in message:
              with st.expander("📚 Sumber Referensi"):
                  for source in message["sources"]:
                      st.write(f"- {source['document']} (hal. {source['page']})")

  # Chat input
  if prompt := st.chat_input("Tanya sesuatu tentang RSUP Sanglah..."):
      # Display user message
      st.session_state.messages.append({"role": "user", "content": prompt})
      with st.chat_message("user"):
          st.markdown(prompt)

      # Call backend API
      with st.chat_message("assistant"):
          with st.spinner("Sedang berpikir..."):
              try:
                  response = requests.post(
                      "http://localhost:8000/api/v1/chat",
                      json={
                          "message": prompt,
                          "session_id": st.session_state.session_id
                      },
                      timeout=30
                  )

                  if response.status_code == 200:
                      data = response.json()
                      st.session_state.session_id = data['session_id']

                      # Display response
                      st.markdown(data['response'])

                      # Display sources
                      if data.get('sources'):
                          with st.expander("📚 Sumber Referensi"):
                              for source in data['sources']:
                                  st.write(f"- {source['document']} (hal. {source['page']}) - Relevansi: {source['similarity']}")

                      # Store in history
                      st.session_state.messages.append({
                          "role": "assistant",
                          "content": data['response'],
                          "sources": data.get('sources', [])
                      })

                      # Show response time
                      st.caption(f"⚡ Response time: {data['response_time_ms']}ms")

                  else:
                      st.error(f"Error: {response.status_code}")

              except Exception as e:
                  st.error(f"Gagal menghubungi server: {str(e)}")
  ```

### Day 24: Feedback Mechanism

- [ ] **Add feedback buttons**

  ```python
  # After displaying bot response
  col1, col2, col3 = st.columns([1, 1, 8])

  with col1:
      if st.button("👍", key=f"thumbs_up_{len(st.session_state.messages)}"):
          # Send feedback to backend
          requests.post(
              "http://localhost:8000/api/v1/feedback",
              json={"message_id": last_message_id, "rating": 1}
          )
          st.success("Terima kasih atas feedback Anda!")

  with col2:
      if st.button("👎", key=f"thumbs_down_{len(st.session_state.messages)}"):
          # Show feedback form
          feedback_text = st.text_area("Apa yang bisa diperbaiki?")
          if st.button("Kirim Feedback"):
              requests.post(
                  "http://localhost:8000/api/v1/feedback",
                  json={
                      "message_id": last_message_id,
                      "rating": -1,
                      "comment": feedback_text
                  }
              )
              st.success("Terima kasih atas feedback Anda!")
  ```

### Day 25: Quick Actions & Suggestions

- [ ] **Add quick action buttons**

  ```python
  # Below chat input
  st.write("**Pertanyaan Populer:**")
  col1, col2, col3 = st.columns(3)

  with col1:
      if st.button("📅 Jadwal Dokter"):
          st.session_state.quick_query = "Bagaimana cara lihat jadwal dokter?"

  with col2:
      if st.button("🏥 Jam Besuk"):
          st.session_state.quick_query = "Jam besuk di RS Sanglah jam berapa?"

  with col3:
      if st.button("📝 Cara Daftar"):
          st.session_state.quick_query = "Bagaimana cara daftar online?"

  # Handle quick query
  if 'quick_query' in st.session_state and st.session_state.quick_query:
      # Process like normal chat input
      # ... (reuse chat logic)
      st.session_state.quick_query = None
  ```

### Day 26-27: Admin Panel

- [ ] **Create admin page (separate file)**

  ```python
  # frontend/pages/1_📊_Admin_Dashboard.py
  import streamlit as st
  import requests
  import pandas as pd
  import plotly.express as px

  st.title("📊 Admin Dashboard")

  # Password protection (simple version)
  password = st.text_input("Password:", type="password")
  if password != "admin123":  # Change this!
      st.warning("Enter password to access admin panel")
      st.stop()

  # Fetch analytics
  response = requests.get("http://localhost:8000/api/v1/admin/analytics?days=30")
  if response.status_code == 200:
      data = response.json()

      # Metrics
      col1, col2, col3, col4 = st.columns(4)
      col1.metric("Total Queries", data['total_queries'])
      col2.metric("Avg Response Time", f"{data['avg_response_time']}ms")
      col3.metric("Satisfaction Rate", f"{data['satisfaction_rate']}%")
      col4.metric("Today's Users", data.get('today_users', 0))

      # Charts
      st.subheader("Query Volume (30 days)")
      df = pd.DataFrame(data['daily_stats'])
      fig = px.line(df, x='date', y='total_queries', title='Daily Queries')
      st.plotly_chart(fig)

      # Top queries
      st.subheader("Top 10 Pertanyaan")
      st.table(data['top_queries'])
  ```

- [ ] **Create document upload page**

  ```python
  # frontend/pages/2_📄_Upload_Document.py
  import streamlit as st
  import requests

  st.title("📄 Upload Dokumen")

  uploaded_file = st.file_uploader("Pilih file PDF", type=['pdf'])

  if uploaded_file:
      col1, col2 = st.columns(2)
      title = col1.text_input("Judul Dokumen", uploaded_file.name)
      doc_type = col2.selectbox("Jenis Dokumen",
          ["Pedoman", "SOP", "Pengumuman", "Lainnya"])

      if st.button("Upload & Process"):
          with st.spinner("Uploading dan memproses dokumen..."):
              files = {"file": uploaded_file}
              data = {"title": title, "document_type": doc_type}

              response = requests.post(
                  "http://localhost:8000/api/v1/documents/upload",
                  files=files,
                  data=data
              )

              if response.status_code == 200:
                  result = response.json()
                  st.success(f"✅ Berhasil! {result['chunks']} chunks diproses")
              else:
                  st.error("Gagal upload dokumen")
  ```

- [ ] **✅ Checkpoint:** Streamlit app fully functional

---

## 19. Phase 3: Testing & Optimization

**Duration:** 5-7 days  
**Goal:** Ensure quality and performance

### Day 28-29: Create Test Dataset

- [ ] **Prepare 100 test questions**

  ```python
  # tests/test_data/test_questions.json
  [
      {
          "id": 1,
          "question": "Jam besuk ICU kapan?",
          "expected_intent": "FAQ_QUERY",
          "expected_answer_contains": ["11.00", "17.00", "ICU"]
      },
      {
          "id": 2,
          "question": "Saya mau daftar ke dokter anak",
          "expected_intent": "REGISTRATION",
          "expected_answer_contains": ["link", "daftar"]
      },
      // ... 98 more questions
  ]
  ```

- [ ] **Create manual ground truth answers**
  ```python
  # tests/test_data/ground_truth.json
  [
      {
          "question_id": 1,
          "correct_answer": "Jam besuk ICU di RSUP Sanglah adalah pukul 11.00-12.00 dan 17.00-18.00 setiap hari..."
      },
      // ...
  ]
  ```

### Day 30: Accuracy Testing

- [ ] **Create automated accuracy test**

  ```python
  # tests/test_accuracy.py
  import json
  import requests
  from difflib import SequenceMatcher

  def test_accuracy():
      with open('tests/test_data/test_questions.json') as f:
          test_cases = json.load(f)

      with open('tests/test_data/ground_truth.json') as f:
          ground_truth = {gt['question_id']: gt['correct_answer']
                         for gt in json.load(f)}

      correct = 0
      total = len(test_cases)
      results = []

      for test in test_cases:
          # Call API
          response = requests.post(
              "http://localhost:8000/api/v1/chat",
              json={"message": test['question']}
          )

          data = response.json()

          # Check intent
          intent_correct = data['intent'] == test['expected_intent']

          # Check answer similarity
          similarity = SequenceMatcher(
              None,
              data['response'].lower(),
              ground_truth[test['id']].lower()
          ).ratio()

          is_correct = intent_correct and similarity > 0.7

          if is_correct:
              correct += 1

          results.append({
              "question": test['question'],
              "intent_correct": intent_correct,
              "similarity": similarity,
              "passed": is_correct
          })

      accuracy = (correct / total) * 100
      print(f"\n✅ Accuracy: {accuracy:.2f}% ({correct}/{total})")

      # Save detailed results
      with open('tests/results/accuracy_report.json', 'w') as f:
          json.dump(results, f, indent=2)

      assert accuracy >= 85, f"Accuracy {accuracy}% below target 85%"
  ```

- [ ] **Run accuracy test:** `pytest tests/test_accuracy.py -v`

### Day 31: Performance Testing

- [ ] **Install Locust**

  ```bash
  pip install locust
  ```

- [ ] **Create load test script**

  ```python
  # tests/locustfile.py
  from locust import HttpUser, task, between
  import random

  class ChatUser(HttpUser):
      wait_time = between(1, 3)  # Wait 1-3 seconds between requests

      questions = [
          "Jam besuk ICU jam berapa?",
          "Jadwal dokter anak kapan?",
          "Saya mau daftar periksa",
          "Dimana lokasi poli gigi?",
          "Biaya rawat inap berapa?"
      ]

      @task
      def chat(self):
          self.client.post("/api/v1/chat", json={
              "message": random.choice(self.questions)
          })

      @task(2)  # 2x weight (more frequent)
      def health_check(self):
          self.client.get("/health")
  ```

- [ ] **Run load test**

  ```bash
  locust -f tests/locustfile.py --host=http://localhost:8000

  # Open browser: http://localhost:8089
  # Set: 10 users, spawn rate 1 user/sec
  # Run for 5 minutes
  ```

- [ ] **Analyze results:**
  - Target: < 5s response time for 95% requests
  - Target: < 1% error rate
  - Note bottlenecks (LLM inference, DB query, etc.)

### Day 32-33: Optimization

- [ ] **Add caching for common queries**

  ```python
  # backend/app/services/cache_service.py
  import redis
  import json
  import hashlib

  class CacheService:
      def __init__(self, redis_url: str):
          self.redis = redis.from_url(redis_url)

      def get_cached_response(self, query: str):
          key = self._make_key(query)
          cached = self.redis.get(key)
          if cached:
              return json.loads(cached)
          return None

      def cache_response(self, query: str, response: dict, ttl: int = 3600):
          key = self._make_key(query)
          self.redis.setex(key, ttl, json.dumps(response))

      def _make_key(self, query: str) -> str:
          # Normalize and hash
          normalized = query.lower().strip()
          return f"chat:{hashlib.md5(normalized.encode()).hexdigest()}"
  ```

- [ ] **Integrate caching in RAG service**

  ```python
  # In RAGService.process_query()

  # Check cache first
  cached = cache_service.get_cached_response(user_message)
  if cached:
      return cached

  # If not cached, process normally
  result = self._handle_faq(user_message)

  # Cache the result
  cache_service.cache_response(user_message, result, ttl=3600)

  return result
  ```

- [ ] **Optimize database queries**

  ```sql
  -- Add missing indexes
  CREATE INDEX idx_chunks_document ON document_chunks(document_id);
  CREATE INDEX idx_messages_session ON messages(conversation_id, timestamp);

  -- Analyze query performance
  EXPLAIN ANALYZE SELECT ... ;
  ```

- [ ] **Optimize LLM prompts (reduce tokens)**
  ```python
  # Before: 500 token prompt
  # After: 300 token prompt (remove unnecessary instructions)
  ```

### Day 34: Bug Fixes & Polish

- [ ] **Fix known issues from testing**
- [ ] **Add input validation everywhere**
- [ ] **Improve error messages**
- [ ] **Add loading indicators**
- [ ] **Test edge cases:**

  - Empty messages
  - Very long messages
  - Special characters
  - Rapid consecutive requests
  - Network timeout

- [ ] **✅ Checkpoint:** System tested and optimized

---

## 20. Phase 4: Internal Deployment & UAT

**Duration:** 7-14 days  
**Goal:** Deploy for internal testing and gather feedback

### Day 35-36: Server Deployment

- [ ] **Prepare production server**

  ```bash
  # On server (Ubuntu 22.04)
  sudo apt update
  sudo apt upgrade -y

  # Install dependencies
  sudo apt install python3.11 python3-pip postgresql redis nginx supervisor

  # Install Ollama
  curl https://ollama.ai/install.sh | sh
  ollama pull llama3.1:8b
  ```

- [ ] **Clone repository**

  ```bash
  cd /opt
  git clone https://your-repo/ngoerah-assistant.git
  cd ngoerah-assistant

  # Setup Python environment
  python3 -m venv venv
  source venv/bin/activate
  pip install -r backend/requirements.txt
  ```

- [ ] **Configure environment**

  ```bash
  # Create .env file
  cp .env.example .env
  nano .env  # Edit with production values

  # Create necessary directories
  mkdir -p data/documents logs
  chmod 755 data/documents
  ```

- [ ] **Setup database**

  ```bash
  sudo -u postgres psql
  CREATE DATABASE ngoerah_assistant;
  CREATE USER ngoerah_user WITH PASSWORD 'strong_password_here';
  GRANT ALL PRIVILEGES ON DATABASE ngoerah_assistant TO ngoerah_user;
  \q

  # Run migrations
  cd backend
  alembic upgrade head
  ```

- [ ] **Configure Supervisor (keep services running)**

  ```bash
  # /etc/supervisor/conf.d/ngoerah-backend.conf
  [program:ngoerah-backend]
  directory=/opt/ngoerah-assistant/backend
  command=/opt/ngoerah-assistant/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
  user=www-data
  autostart=true
  autorestart=true
  redirect_stderr=true
  stdout_logfile=/opt/ngoerah-assistant/logs/backend.log

  # /etc/supervisor/conf.d/ngoerah-frontend.conf
  [program:ngoerah-frontend]
  directory=/opt/ngoerah-assistant/frontend
  command=/opt/ngoerah-assistant/venv/bin/streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
  user=www-data
  autostart=true
  autorestart=true
  redirect_stderr=true
  stdout_logfile=/opt/ngoerah-assistant/logs/frontend.log
  ```

- [ ] **Start services**

  ```bash
  sudo supervisorctl reread
  sudo supervisorctl update
  sudo supervisorctl start all

  # Check status
  sudo supervisorctl status
  ```

- [ ] **Configure Nginx (reverse proxy)**

  ```nginx
  # /etc/nginx/sites-available/ngoerah-assistant
  server {
      listen 80;
      server_name assistant.sanglah.internal;  # Internal domain

      # Backend API
      location /api/ {
          proxy_pass http://localhost:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_read_timeout 30s;
      }

      # Frontend
      location / {
          proxy_pass http://localhost:8501;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_set_header Host $host;
          proxy_cache_bypass $http_upgrade;
      }
  }
  ```

- [ ] **Enable site & restart Nginx**

  ```bash
  sudo ln -s /etc/nginx/sites-available/ngoerah-assistant /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl restart nginx
  ```

- [ ] **Verify deployment**

  ```bash
  # Check all services running
  sudo supervisorctl status

  # Test backend
  curl http://localhost:8000/health

  # Test frontend
  curl http://localhost:8501

  # Test through Nginx
  curl http://assistant.sanglah.internal/health
  ```

### Day 37-38: Upload Initial Documents

- [ ] **Gather hospital documents**

  - Pedoman Pasien
  - SOP Pendaftaran
  - Jadwal Dokter
  - Informasi Fasilitas
  - Prosedur BPJS
  - Jam Besuk & Peraturan

- [ ] **Upload via admin panel**

  - Access: http://assistant.sanglah.internal/📄_Upload_Document
  - Upload each PDF
  - Verify processing success
  - Test search for each document

- [ ] **Create backup of processed data**

  ```bash
  # Backup database
  pg_dump ngoerah_assistant > backup_$(date +%Y%m%d).sql

  # Backup document files
  tar -czf documents_backup_$(date +%Y%m%d).tar.gz data/documents/
  ```

### Day 39-42: User Acceptance Testing (UAT)

- [ ] **Recruit internal testers (10-15 people)**

  - 3-5 staff front desk/call center
  - 3-5 staff IT
  - 2-3 management
  - 2-3 staff medis

- [ ] **Create UAT guide document**

  ```markdown
  # UAT Guide - Ngoerah Smart Assistant

  ## Akses

  URL: http://assistant.sanglah.internal

  ## Skenario Testing

  ### Test 1: Pertanyaan Umum (FAQ)

  Coba tanyakan:

  - Jam besuk ICU
  - Jadwal dokter anak
  - Cara daftar BPJS
  - Lokasi poli gigi
  - Biaya rawat inap

  **Yang perlu diperhatikan:**

  - Apakah jawaban akurat?
  - Apakah mudah dipahami?
  - Apakah response cukup cepat?

  ### Test 2: Registrasi

  Coba katakan:

  - "Saya mau daftar"
  - "Gimana cara booking dokter"

  **Yang perlu diperhatikan:**

  - Apakah link muncul?
  - Apakah link mengarah ke halaman yang benar?

  ### Test 3: Percakapan Kontekstual

  Coba:

  1. "Jam besuk ICU jam berapa?"
  2. "Boleh bawa makanan?"
  3. "Berapa lama boleh stay?"

  **Yang perlu diperhatikan:**

  - Apakah bot paham konteks (bahwa kita masih bicara tentang ICU)?

  ## Form Feedback

  Setelah testing, isi form ini: [Google Form Link]
  ```

- [ ] **Setup feedback collection**

  - Create Google Form for structured feedback
  - Questions:
    - Seberapa puas dengan akurasi jawaban? (1-10)
    - Seberapa puas dengan kecepatan response? (1-10)
    - Apakah interface mudah digunakan? (1-10)
    - Fitur apa yang perlu ditambahkan?
    - Bug/masalah yang ditemukan?
    - Saran improvement?

- [ ] **Conduct UAT sessions**

  - Week 1: Testing & feedback collection
  - Daily monitoring of usage & errors
  - Quick fix critical bugs
  - Document all feedback

- [ ] **Analyze UAT results**

  ```python
  # Script to analyze feedback
  import pandas as pd

  df = pd.read_csv('uat_feedback.csv')

  print("=== UAT Results Summary ===")
  print(f"Average Accuracy Score: {df['accuracy'].mean():.2f}/10")
  print(f"Average Speed Score: {df['speed'].mean():.2f}/10")
  print(f"Average UX Score: {df['ux'].mean():.2f}/10")
  print(f"\nTotal Bugs Reported: {df['bugs'].notna().sum()}")
  print(f"Total Feature Requests: {df['features'].notna().sum()}")
  ```

### Day 43-45: Iterations Based on Feedback

- [ ] **Fix high-priority bugs**

  - Prioritize by severity:
    1. Critical (system crash, data loss)
    2. High (wrong answers, broken features)
    3. Medium (UX issues, slow performance)
    4. Low (minor UI glitches)

- [ ] **Implement quick wins**

  - Add most requested FAQ topics
  - Improve prompts for better answers
  - Fix navigation issues
  - Enhance error messages

- [ ] **Update documentation**

  - Document known limitations
  - Update user guide
  - Add FAQ for staff

- [ ] **Prepare UAT report**

  ```markdown
  # UAT Report - Ngoerah Smart Assistant

  ## Executive Summary

  - Testing Period: [dates]
  - Testers: 15 internal staff
  - Total Queries Tested: 450+

  ## Results

  - Overall Satisfaction: 8.2/10
  - Accuracy Rate: 87%
  - Average Response Time: 3.2 seconds
  - Bug-Free Sessions: 92%

  ## Key Findings

  ### Strengths

  - Fast and accurate for common queries
  - Easy to use interface
  - Helpful for reducing call center load

  ### Areas for Improvement

  - Need more documents (specialist schedules)
  - Occasionally gives generic answers
  - Mobile experience needs improvement

  ## Recommendations

  ✅ Ready for limited production (internal only)
  → Next: Develop mobile app for external users
  ```

- [ ] **Get stakeholder approval for Phase 5**

- [ ] **✅ Checkpoint:** UAT complete, ready for mobile development

---

## 21. Phase 5: Mobile App Development - Flutter

**Duration:** 21-28 days  
**Goal:** Create cross-platform mobile app (Android & iOS)

### Week 1: Flutter Setup & UI Design

#### Day 46-47: Environment Setup

- [ ] **Install Flutter SDK**

  ```bash
  # Download from flutter.dev
  git clone https://github.com/flutter/flutter.git -b stable
  export PATH="$PATH:`pwd`/flutter/bin"

  # Verify installation
  flutter doctor
  ```

- [ ] **Install Android Studio / Xcode**

  - Android Studio (for Android development)
  - Xcode (for iOS development, macOS only)

- [ ] **Create Flutter project**

  ```bash
  flutter create ngoerah_mobile
  cd ngoerah_mobile

  # Add dependencies to pubspec.yaml
  ```

- [ ] **Setup dependencies (pubspec.yaml)**

  ```yaml
  dependencies:
    flutter:
      sdk: flutter

    # UI
    google_fonts: ^6.1.0
    flutter_svg: ^2.0.9

    # State Management
    riverpod: ^2.4.9
    flutter_riverpod: ^2.4.9

    # HTTP & API
    dio: ^5.4.0
    retrofit: ^4.0.3
    json_annotation: ^4.8.1

    # Local Storage
    shared_preferences: ^2.2.2
    hive: ^2.2.3
    hive_flutter: ^1.1.0

    # Utils
    intl: ^0.18.1
    uuid: ^4.2.2
    url_launcher: ^6.2.2

  dev_dependencies:
    flutter_test:
      sdk: flutter
    build_runner: ^2.4.7
    json_serializable: ^6.7.1
    retrofit_generator: ^8.0.6
  ```

- [ ] **Run flutter pub get**

#### Day 48-50: UI/UX Design & Wireframes

- [ ] **Design app structure**

  ```
  Screens:
  1. Splash Screen (logo animation)
  2. Onboarding (swipeable intro, 3 slides)
  3. Home/Chat Screen (main interface)
  4. History Screen (past conversations)
  5. Settings Screen (about, privacy policy)
  6. Quick Actions (bottom sheet for common queries)
  ```

- [ ] **Create design system**

  ```dart
  // lib/core/theme/app_theme.dart
  class AppTheme {
    static const primaryColor = Color(0xFF007AFF);  // Blue
    static const secondaryColor = Color(0xFF34C759);  // Green
    static const backgroundColor = Color(0xFFF5F5F5);
    static const surfaceColor = Colors.white;
    static const errorColor = Color(0xFFFF3B30);

    static ThemeData lightTheme = ThemeData(
      primaryColor: primaryColor,
      scaffoldBackgroundColor: backgroundColor,
      appBarTheme: AppBarTheme(
        backgroundColor: surfaceColor,
        elevation: 0,
        iconTheme: IconThemeData(color: Colors.black),
      ),
      // ... more theme config
    );
  }
  ```

- [ ] **Create reusable widgets**

  ```dart
  // lib/widgets/message_bubble.dart
  class MessageBubble extends StatelessWidget {
    final String message;
    final bool isUser;
    final DateTime timestamp;

    @override
    Widget build(BuildContext context) {
      return Align(
        alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
        child: Container(
          margin: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
          padding: EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: isUser ? AppTheme.primaryColor : Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: Colors.black12,
                blurRadius: 4,
                offset: Offset(0, 2),
              ),
            ],
          ),
          child: Text(
            message,
            style: TextStyle(
              color: isUser ? Colors.white : Colors.black87,
              fontSize: 15,
            ),
          ),
        ),
      );
    }
  }
  ```

#### Day 51-52: Splash & Onboarding

- [ ] **Create splash screen**

  ```dart
  // lib/screens/splash_screen.dart
  class SplashScreen extends StatefulWidget {
    @override
    _SplashScreenState createState() => _SplashScreenState();
  }

  class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
    late AnimationController _controller;
    late Animation<double> _fadeAnimation;

    @override
    void initState() {
      super.initState();
      _controller = AnimationController(
        duration: Duration(seconds: 2),
        vsync: this,
      );
      _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(_controller);

      _controller.forward();

      // Navigate after 3 seconds
      Future.delayed(Duration(seconds: 3), () {
        Navigator.pushReplacementNamed(context, '/onboarding');
      });
    }

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        backgroundColor: AppTheme.primaryColor,
        body: Center(
          child: FadeTransition(
            opacity: _fadeAnimation,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(Icons.local_hospital, size: 100, color: Colors.white),
                SizedBox(height: 20),
                Text(
                  'Ngoerah Assistant',
                  style: TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ],
            ),
          ),
        ),
      );
    }
  }
  ```

- [ ] **Create onboarding screens**

  ```dart
  // lib/screens/onboarding_screen.dart
  class OnboardingScreen extends StatefulWidget {
    @override
    _OnboardingScreenState createState() => _OnboardingScreenState();
  }

  class _OnboardingScreenState extends State<OnboardingScreen> {
    final PageController _pageController = PageController();
    int _currentPage = 0;

    final List<OnboardingPage> pages = [
      OnboardingPage(
        icon: Icons.chat_bubble_outline,
        title: 'Tanya Apa Saja',
        description: 'Dapatkan informasi tentang jadwal, fasilitas, dan prosedur RS dengan cepat',
      ),
      OnboardingPage(
        icon: Icons.schedule,
        title: 'Layanan 24/7',
        description: 'Asisten virtual kami siap membantu Anda kapan saja',
      ),
      OnboardingPage(
        icon: Icons.security,
        title: 'Aman & Terpercaya',
        description: 'Data Anda aman, informasi dari sumber resmi RS',
      ),
    ];

    @override
    Widget build(BuildContext context) {
      return Scaffold(
        body: SafeArea(
          child: Column(
            children: [
              Expanded(
                child: PageView.builder(
                  controller: _pageController,
                  onPageChanged: (index) {
                    setState(() => _currentPage = index);
                  },
                  itemCount: pages.length,
                  itemBuilder: (context, index) => _buildPage(pages[index]),
                ),
              ),
              _buildIndicator(),
              _buildButtons(),
            ],
          ),
        ),
      );
    }
  }
  ```

### Week 2: Core Features Implementation

#### Day 53-55: API Integration

- [ ] **Create API service with Retrofit**

  ```dart
  // lib/data/api/api_service.dart
  @RestApi(baseUrl: "http://your-server-ip:8000/api/v1")
  abstract class ApiService {
    factory ApiService(Dio dio) = _ApiService;

    @POST("/chat")
    Future<ChatResponse> sendMessage(@Body() ChatRequest request);

    @POST("/feedback")
    Future<void> submitFeedback(@Body() FeedbackRequest request);

    @GET("/health")
    Future<HealthResponse> healthCheck();
  }
  ```

- [ ] **Create data models**

  ```dart
  // lib/data/models/chat_request.dart
  @JsonSerializable()
  class ChatRequest {
    final String message;
    @JsonKey(name: 'session_id')
    final String? sessionId;
    @JsonKey(name: 'user_id')
    final String? userId;

    ChatRequest({required this.message, this.sessionId, this.userId});

    factory ChatRequest.fromJson(Map<String, dynamic> json) =>
        _$ChatRequestFromJson(json);
    Map<String, dynamic> toJson() => _$ChatRequestToJson(this);
  }

  // lib/data/models/chat_response.dart
  @JsonSerializable()
  class ChatResponse {
    final String response;
    final String intent;
    final double confidence;
    final List<Source>? sources;
    @JsonKey(name: 'session_id')
    final String sessionId;
    @JsonKey(name: 'response_time_ms')
    final int responseTimeMs;

    ChatResponse({
      required this.response,
      required this.intent,
      required this.confidence,
      this.sources,
      required this.sessionId,
      required this.responseTimeMs,
    });

    factory ChatResponse.fromJson(Map<String, dynamic> json) =>
        _$ChatResponseFromJson(json);
  }
  ```

- [ ] **Generate code**

  ```bash
  flutter pub run build_runner build --delete-conflicting-outputs
  ```

- [ ] **Create repository pattern**

  ```dart
  // lib/data/repositories/chat_repository.dart
  class ChatRepository {
    final ApiService _apiService;

    ChatRepository(this._apiService);

    Future<Result<ChatResponse>> sendMessage(String message, String? sessionId) async {
      try {
        final request = ChatRequest(
          message: message,
          sessionId: sessionId,
        );

        final response = await _apiService.sendMessage(request);
        return Result.success(response);
      } catch (e) {
        return Result.error(e.toString());
      }
    }
  }
  ```

#### Day 56-58: State Management with Riverpod

- [ ] **Create providers**

  ```dart
  // lib/providers/chat_provider.dart
  final chatRepositoryProvider = Provider<ChatRepository>((ref) {
    final dio = Dio(BaseOptions(
      connectTimeout: Duration(seconds: 30),
      receiveTimeout: Duration(seconds: 30),
    ));

    return ChatRepository(ApiService(dio));
  });

  class ChatNotifier extends StateNotifier<ChatState> {
    final ChatRepository _repository;

    ChatNotifier(this._repository) : super(ChatState.initial());

    Future<void> sendMessage(String message) async {
      state = state.copyWith(isLoading: true);

      final result = await _repository.sendMessage(
        message,
        state.sessionId,
      );

      result.when(
        success: (response) {
          state = state.copyWith(
            isLoading: false,
            messages: [
              ...state.messages,
              Message(
                content: message,
                isUser: true,
                timestamp: DateTime.now(),
              ),
              Message(
                content: response.response,
                isUser: false,
                timestamp: DateTime.now(),
                sources: response.sources,
              ),
            ],
            sessionId: response.sessionId,
          );
        },
        error: (error) {
          state = state.copyWith(
            isLoading: false,
            error: error,
          );
        },
      );
    }
  }

  final chatProvider = StateNotifierProvider<ChatNotifier, ChatState>((ref) {
    return ChatNotifier(ref.watch(chatRepositoryProvider));
  });
  ```

- [ ] **Create state classes**

  ```dart
  // lib/providers/chat_state.dart
  @freezed
  class ChatState with _$ChatState {
    const factory ChatState({
      required List<Message> messages,
      required bool isLoading,
      String? sessionId,
      String? error,
    }) = _ChatState;

    factory ChatState.initial() => ChatState(
      messages: [],
      isLoading: false,
    );
  }
  ```

#### Day 59-60: Chat Screen Implementation

- [ ] **Create chat screen**

  ```dart
  // lib/screens/chat_screen.dart
  class ChatScreen extends ConsumerStatefulWidget {
    @override
    _ChatScreenState createState() => _ChatScreenState();
  }

  class _ChatScreenState extends ConsumerState<ChatScreen> {
    final TextEditingController _controller = TextEditingController();
    final ScrollController _scrollController = ScrollController();

    @override
    Widget build(BuildContext context) {
      final chatState = ref.watch(chatProvider);

      return Scaffold(
        appBar: AppBar(
          title: Text('Ngoerah Assistant'),
          actions: [
            IconButton(
              icon: Icon(Icons.history),
              onPressed: () => Navigator.pushNamed(context, '/history'),
            ),
          ],
        ),
        body: Column(
          children: [
            // Quick Actions
            _buildQuickActions(),

            // Messages List
            Expanded(
              child: chatState.messages.isEmpty
                  ? _buildEmptyState()
                  : ListView.builder(
                      controller: _scrollController,
                      padding: EdgeInsets.all(16),
                      itemCount: chatState.messages.length,
                      itemBuilder: (context, index) {
                        return MessageBubble(
                          message: chatState.messages[index],
                          onSourceTap: _showSources,
                        );
                      },
                    ),
            ),

            // Loading Indicator
            if (chatState.isLoading)
              Padding(
                padding: EdgeInsets.all(8),
                child: TypingIndicator(),
              ),

            // Input Field
            _buildInputField(),
          ],
        ),
      );
    }

    Widget _buildInputField() {
      return Container(
        padding: EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.black12,
              blurRadius: 4,
              offset: Offset(0, -2),
            ),
          ],
        ),
        child: Row(
          children: [
            Expanded(
              child: TextField(
                controller: _controller,
                decoration: InputDecoration(
                  hintText: 'Tanya sesuatu...',
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(24),
                  ),
                  contentPadding: EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 10,
                  ),
                ),
                maxLines: null,
                textInputAction: TextInputAction.send,
                onSubmitted: _sendMessage,
              ),
            ),
            SizedBox(width: 8),
            CircleAvatar(
              backgroundColor: AppTheme.primaryColor,
              child: IconButton(
                icon: Icon(Icons.send, color: Colors.white),
                onPressed: () => _sendMessage(_controller.text),
              ),
            ),
          ],
        ),
      );
    }

    void _sendMessage(String text) {
      if (text.trim().isEmpty) return;

      ref.read(chatProvider.notifier).sendMessage(text.trim());
      _controller.clear();

      // Auto scroll to bottom
      Future.delayed(Duration(milliseconds: 300), () {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }
  }
  ```

### Week 3: Additional Features & Polish

#### Day 61-62: Quick Actions & Suggestions

- [ ] **Implement quick action buttons**

  ```dart
  Widget _buildQuickActions() {
    final actions = [
      QuickAction('📅 Jadwal Dokter', 'Jadwal dokter hari ini'),
      QuickAction('🏥 Jam Besuk', 'Jam besuk ICU'),
      QuickAction('📝 Cara Daftar', 'Bagaimana cara daftar online?'),
      QuickAction('💰 Biaya', 'Estimasi biaya rawat inap'),
    ];

    return Container(
      height: 60,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        itemCount: actions.length,
        itemBuilder: (context, index) {
          return Padding(
            padding: EdgeInsets.only(right: 8),
            child: ActionChip(
              label: Text(actions[index].label),
              onPressed: () {
                _controller.text = actions[index].query;
                _sendMessage(actions[index].query);
              },
            ),
          );
        },
      ),
    );
  }
  ```

#### Day 63-64: History & Local Storage

- [ ] **Implement conversation history with Hive**

  ```dart
  // lib/data/local/conversation_dao.dart
  @HiveType(typeId: 0)
  class ConversationModel {
    @HiveField(0)
    final String id;

    @HiveField(1)
    final List<MessageModel> messages;

    @HiveField(2)
    final DateTime createdAt;

    @HiveField(3)
    final DateTime lastActivity;

    ConversationModel({
      required this.id,
      required this.messages,
      required this.createdAt,
      required this.lastActivity,
    });
  }

  class ConversationDao {
    final Box<ConversationModel> _box;

    ConversationDao(this._box);

    Future<void> saveConversation(ConversationModel conversation) async {
      await _box.put(conversation.id, conversation);
    }

    List<ConversationModel> getAllConversations() {
      return _box.values.toList()
        ..sort((a, b) => b.lastActivity.compareTo(a.lastActivity));
    }

    Future<void> deleteConversation(String id) async {
      await _box.delete(id);
    }
  }
  ```

- [ ] **Create history screen**

  ```dart
  // lib/screens/history_screen.dart
  class HistoryScreen extends ConsumerWidget {
    @override
    Widget build(BuildContext context, WidgetRef ref) {
      final conversations = ref.watch(conversationHistoryProvider);

      return Scaffold(
        appBar: AppBar(
          title: Text('Riwayat Percakapan'),
          actions: [
            IconButton(
              icon: Icon(Icons.delete_sweep),
              onPressed: () => _showClearAllDialog(context, ref),
            ),
          ],
        ),
        body: conversations.isEmpty
            ? Center(child: Text('Belum ada riwayat'))
            : ListView.builder(
                itemCount: conversations.length,
                itemBuilder: (context, index) {
                  final conv = conversations[index];
                  return ListTile(
                    leading: CircleAvatar(
                      child: Icon(Icons.chat),
                    ),
                    title: Text(
                      conv.messages.first.content,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                    subtitle: Text(
                      _formatDate(conv.lastActivity),
                    ),
                    trailing: IconButton(
                      icon: Icon(Icons.delete),
                      onPressed: () => _deleteConversation(ref, conv.id),
                    ),
                    onTap: () => _openConversation(context, conv),
                  );
                },
              ),
      );
    }
  }
  ```

#### Day 65-66: Feedback & Rating

- [ ] **Implement feedback mechanism**

  ```dart
  Widget _buildFeedbackButtons(Message message) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        IconButton(
          icon: Icon(Icons.thumb_up_outlined, size: 20),
          onPressed: () => _submitFeedback(message.id, 1),
        ),
        IconButton(
          icon: Icon(Icons.thumb_down_outlined, size: 20),
          onPressed: () => _showFeedbackDialog(message.id),
        ),
      ],
    );
  }

  void _showFeedbackDialog(int messageId) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Apa yang bisa diperbaiki?'),
        content: TextField(
          controller: _feedbackController,
          decoration: InputDecoration(
            hintText: 'Feedback Anda...',
          ),
          maxLines: 3,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Batal'),
          ),
          ElevatedButton(
            onPressed: () {
              _submitFeedback(messageId, -1, _feedbackController.text);
              Navigator.pop(context);
            },
            child: Text('Kirim'),
          ),
        ],
      ),
    );
  }
  ```

#### Day 67-68: Settings & About

- [ ] **Create settings screen**

  ```dart
  // lib/screens/settings_screen.dart
  class SettingsScreen extends StatelessWidget {
    @override
    Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(title: Text('Pengaturan')),
        body: ListView(
          children: [
            ListTile(
              leading: Icon(Icons.info),
              title: Text('Tentang Aplikasi'),
              onTap: () => _showAboutDialog(context),
            ),
            ListTile(
              leading: Icon(Icons.privacy_tip),
              title: Text('Kebijakan Privasi'),
              onTap: () => _openPrivacyPolicy(),
            ),
            ListTile(
              leading: Icon(Icons.phone),
              title: Text('Hubungi Kami'),
              subtitle: Text('(0361) 227911'),
              onTap: () => _callHospital(),
            ),
            Divider(),
            ListTile(
              leading: Icon(Icons.delete_forever),
              title: Text('Hapus Semua Riwayat'),
              onTap: () => _showClearHistoryDialog(context),
            ),
            ListTile(
              leading: Icon(Icons.logout),
              title: Text('Keluar'),
              onTap: () => _logout(context),
            ),
          ],
        ),
      );
    }

    void _showAboutDialog(BuildContext context) {
      showAboutDialog(
        context: context,
        applicationName: 'Ngoerah Smart Assistant',
        applicationVersion: '1.0.0',
        applicationIcon: Icon(Icons.local_hospital, size: 50, color: AppTheme.primaryColor),
        children: [
          Text('Asisten Virtual RSUP Prof. dr. I.G.N.G. Ngoerah'),
          SizedBox(height: 16),
          Text('Dikembangkan oleh Tim IT RSUP Sanglah'),
        ],
      );
    }

    void _openPrivacyPolicy() async {
      const url = 'https://sanglah.go.id/privacy-policy';
      if (await canLaunchUrl(Uri.parse(url))) {
        await launchUrl(Uri.parse(url));
      }
    }

    void _callHospital() async {
      const tel = 'tel:+62361227911';
      if (await canLaunchUrl(Uri.parse(tel))) {
        await launchUrl(Uri.parse(tel));
      }
    }
  }
  ```

#### Day 69-70: Error Handling & Offline Support

- [ ] **Implement error handling UI**

  ```dart
  // lib/widgets/error_widget.dart
  class ErrorMessageWidget extends StatelessWidget {
    final String error;
    final VoidCallback? onRetry;

    const ErrorMessageWidget({
      required this.error,
      this.onRetry,
    });

    @override
    Widget build(BuildContext context) {
      return Container(
        padding: EdgeInsets.all(16),
        margin: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: Colors.red.shade50,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: Colors.red.shade200),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline, color: Colors.red, size: 32),
            SizedBox(height: 8),
            Text(
              'Gagal menghubungi server',
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: Colors.red.shade700,
              ),
            ),
            SizedBox(height: 4),
            Text(
              error,
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.red.shade600),
            ),
            if (onRetry != null) ...[
              SizedBox(height: 12),
              ElevatedButton.icon(
                onPressed: onRetry,
                icon: Icon(Icons.refresh),
                label: Text('Coba Lagi'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                ),
              ),
            ],
          ],
        ),
      );
    }
  }
  ```

- [ ] **Add connectivity check**

  ```dart
  // lib/providers/connectivity_provider.dart
  final connectivityProvider = StreamProvider<ConnectivityResult>((ref) {
    return Connectivity().onConnectivityChanged;
  });

  // In chat_screen.dart
  Widget build(BuildContext context) {
    final connectivity = ref.watch(connectivityProvider);

    return connectivity.when(
      data: (result) {
        if (result == ConnectivityResult.none) {
          return _buildOfflineMode();
        }
        return _buildChatInterface();
      },
      loading: () => CircularProgressIndicator(),
      error: (e, _) => _buildChatInterface(),
    );
  }

  Widget _buildOfflineMode() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.wifi_off, size: 64, color: Colors.grey),
          SizedBox(height: 16),
          Text(
            'Tidak ada koneksi internet',
            style: TextStyle(fontSize: 18, color: Colors.grey[700]),
          ),
          SizedBox(height: 8),
          Text(
            'Riwayat percakapan tersimpan dapat dilihat di offline mode',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey[600]),
          ),
          SizedBox(height: 24),
          ElevatedButton.icon(
            onPressed: () => Navigator.pushNamed(context, '/history'),
            icon: Icon(Icons.history),
            label: Text('Lihat Riwayat'),
          ),
        ],
      ),
    );
  }
  ```

### Week 4: Testing & Build

#### Day 71-72: Widget Testing

- [ ] **Create unit tests for providers**

  ```dart
  // test/providers/chat_provider_test.dart
  import 'package:flutter_test/flutter_test.dart';
  import 'package:mocktail/mocktail.dart';

  class MockChatRepository extends Mock implements ChatRepository {}

  void main() {
    late ChatNotifier chatNotifier;
    late MockChatRepository mockRepository;

    setUp(() {
      mockRepository = MockChatRepository();
      chatNotifier = ChatNotifier(mockRepository);
    });

    group('ChatNotifier', () {
      test('initial state should be empty', () {
        expect(chatNotifier.state.messages, isEmpty);
        expect(chatNotifier.state.isLoading, false);
        expect(chatNotifier.state.error, isNull);
      });

      test('sendMessage should add user message and response', () async {
        // Arrange
        when(() => mockRepository.sendMessage(any(), any()))
            .thenAnswer((_) async => Result.success(
              ChatResponse(
                response: 'Test response',
                intent: 'FAQ_QUERY',
                confidence: 0.95,
                sessionId: 'test-session',
                responseTimeMs: 1000,
              ),
            ));

        // Act
        await chatNotifier.sendMessage('Test message');

        // Assert
        expect(chatNotifier.state.messages.length, 2);
        expect(chatNotifier.state.messages[0].isUser, true);
        expect(chatNotifier.state.messages[1].isUser, false);
        expect(chatNotifier.state.isLoading, false);
      });

      test('sendMessage should handle errors', () async {
        // Arrange
        when(() => mockRepository.sendMessage(any(), any()))
            .thenAnswer((_) async => Result.error('Network error'));

        // Act
        await chatNotifier.sendMessage('Test message');

        // Assert
        expect(chatNotifier.state.error, 'Network error');
        expect(chatNotifier.state.isLoading, false);
      });
    });
  }
  ```

- [ ] **Create widget tests**

  ```dart
  // test/widgets/message_bubble_test.dart
  import 'package:flutter/material.dart';
  import 'package:flutter_test/flutter_test.dart';

  void main() {
    testWidgets('MessageBubble displays user message correctly', (tester) async {
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: MessageBubble(
            message: Message(
              content: 'Test message',
              isUser: true,
              timestamp: DateTime.now(),
            ),
          ),
        ),
      ));

      expect(find.text('Test message'), findsOneWidget);

      // Check background color for user message
      final container = tester.widget<Container>(find.byType(Container).first);
      final decoration = container.decoration as BoxDecoration;
      expect(decoration.color, AppTheme.primaryColor);
    });

    testWidgets('MessageBubble displays bot message with sources', (tester) async {
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: MessageBubble(
            message: Message(
              content: 'Bot response',
              isUser: false,
              timestamp: DateTime.now(),
              sources: [
                Source(document: 'Pedoman.pdf', page: 5, similarity: 0.95),
              ],
            ),
          ),
        ),
      ));

      expect(find.text('Bot response'), findsOneWidget);
      expect(find.byIcon(Icons.source), findsOneWidget);
    });
  }
  ```

- [ ] **Run tests**

  ```bash
  flutter test --coverage

  # Generate coverage report
  genhtml coverage/lcov.info -o coverage/html
  open coverage/html/index.html
  ```

#### Day 73: Integration Testing

- [ ] **Create integration tests**

  ```dart
  // integration_test/app_test.dart
  import 'package:flutter_test/flutter_test.dart';
  import 'package:integration_test/integration_test.dart';

  void main() {
    IntegrationTestWidgetsFlutterBinding.ensureInitialized();

    group('End-to-end test', () {
      testWidgets('Complete chat flow', (tester) async {
        // Start app
        app.main();
        await tester.pumpAndSettle();

        // Wait for splash screen
        await tester.pumpAndSettle(Duration(seconds: 3));

        // Skip onboarding if shown
        if (find.text('Lewati').evaluate().isNotEmpty) {
          await tester.tap(find.text('Lewati'));
          await tester.pumpAndSettle();
        }

        // Enter chat message
        final textField = find.byType(TextField);
        await tester.enterText(textField, 'Jam besuk ICU');
        await tester.pumpAndSettle();

        // Tap send button
        await tester.tap(find.byIcon(Icons.send));
        await tester.pumpAndSettle();

        // Wait for response
        await tester.pumpAndSettle(Duration(seconds: 10));

        // Verify response appeared
        expect(find.textContaining('ICU'), findsWidgets);

        // Tap feedback button
        await tester.tap(find.byIcon(Icons.thumb_up_outlined));
        await tester.pumpAndSettle();

        // Verify feedback toast
        expect(find.textContaining('Terima kasih'), findsOneWidget);
      });
    });
  }
  ```

- [ ] **Run integration tests**
  ```bash
  flutter test integration_test/app_test.dart
  ```

#### Day 74-75: Build & Release

- [ ] **Configure app signing (Android)**

  ```bash
  # Generate keystore
  keytool -genkey -v -keystore android/app/upload-keystore.jks \
    -storetype JKS -keyalg RSA -keysize 2048 -validity 10000 \
    -alias upload

  # Create key.properties
  echo "storePassword=your-store-password
  keyPassword=your-key-password
  keyAlias=upload
  storeFile=upload-keystore.jks" > android/key.properties
  ```

- [ ] **Update android/app/build.gradle**

  ```gradle
  def keystoreProperties = new Properties()
  def keystorePropertiesFile = rootProject.file('key.properties')
  if (keystorePropertiesFile.exists()) {
      keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
  }

  android {
      signingConfigs {
          release {
              keyAlias keystoreProperties['keyAlias']
              keyPassword keystoreProperties['keyPassword']
              storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
              storePassword keystoreProperties['storePassword']
          }
      }
      buildTypes {
          release {
              signingConfig signingConfigs.release
              minifyEnabled true
              shrinkResources true
              proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
          }
      }
  }
  ```

- [ ] **Build release APK**

  ```bash
  # Build APK
  flutter build apk --release

  # Output: build/app/outputs/flutter-apk/app-release.apk

  # Build App Bundle (for Play Store)
  flutter build appbundle --release
  ```

- [ ] **Build iOS (macOS only)**

  ```bash
  # Build iOS
  flutter build ios --release

  # Archive in Xcode
  open ios/Runner.xcworkspace
  # Product > Archive
  ```

- [ ] **Test release build**

  ```bash
  # Install on device
  flutter install --release

  # Test all features:
  # - Splash screen animation
  # - Onboarding flow
  # - Send message & receive response
  # - View sources
  # - Give feedback
  # - View history
  # - Settings page
  # - Offline mode
  ```

- [ ] **✅ Checkpoint:** Mobile app complete and tested

---

## 22. Phase 6: Production Deployment

**Duration:** 7-14 days  
**Goal:** Deploy complete system for production use

### Day 76-77: Final System Check

- [ ] **Backend system verification**

  ```bash
  # Check all services running
  sudo systemctl status postgresql
  sudo systemctl status redis
  sudo systemctl status nginx
  sudo supervisorctl status

  # Check disk space
  df -h

  # Check memory usage
  free -m

  # Check Ollama model loaded
  ollama list

  # Test API health
  curl http://localhost:8000/health/detailed
  ```

- [ ] **Performance benchmarking**

  ```bash
  # Run final load test
  locust -f tests/locustfile.py --host=http://localhost:8000 \
    --users 50 --spawn-rate 5 --run-time 10m --headless

  # Expected results:
  # - Response time (p95): < 5s
  # - Error rate: < 1%
  # - Requests per second: > 10
  ```

- [ ] **Security audit**

  ```bash
  # Check open ports
  sudo netstat -tuln

  # Verify firewall rules
  sudo ufw status

  # Check SSL certificate (if using HTTPS)
  openssl s_client -connect assistant.sanglah.internal:443 -servername assistant.sanglah.internal

  # Scan for vulnerabilities
  pip install safety
  safety check -r requirements.txt
  ```

### Day 78-79: Documentation & Training

- [ ] **Create user manual**

  ```markdown
  # Panduan Penggunaan Ngoerah Smart Assistant

  ## Untuk Pasien & Keluarga

  ### Mengakses Chatbot

  1. Buka aplikasi Ngoerah Assistant di smartphone Anda
  2. Atau kunjungi: http://assistant.sanglah.internal

  ### Bertanya kepada Chatbot

  - Ketik pertanyaan Anda di kolom chat
  - Tekan tombol kirim atau Enter
  - Tunggu jawaban (biasanya 3-5 detik)

  ### Contoh Pertanyaan yang Bisa Dijawab

  - "Jam besuk ICU jam berapa?"
  - "Jadwal dokter anak hari ini siapa?"
  - "Bagaimana cara daftar online?"
  - "Persyaratan BPJS apa saja?"
  - "Di mana lokasi poli gigi?"

  ### Tips Bertanya

  ✅ DO: Pertanyaan jelas dan spesifik
  ❌ DON'T: Pertanyaan terlalu panjang atau tidak jelas

  ### Memberikan Feedback

  - Setelah menerima jawaban, Anda bisa memberikan feedback
  - Tekan 👍 jika puas dengan jawaban
  - Tekan 👎 jika tidak puas, dan berikan saran

  ## Untuk Staff RS

  ### Mengupload Dokumen Baru

  1. Akses Admin Panel
  2. Login dengan kredensial admin
  3. Pilih menu "Upload Dokumen"
  4. Pilih file PDF
  5. Isi judul dan kategori
  6. Klik Upload
  7. Tunggu proses selesai

  ### Melihat Analytics

  1. Akses Admin Panel > Dashboard
  2. Lihat statistik penggunaan
  3. Identifikasi pertanyaan populer
  4. Review feedback negatif untuk improvement
  ```

- [ ] **Conduct staff training**

  - [ ] Session 1: Overview sistem (30 menit)
  - [ ] Session 2: Hands-on penggunaan (45 menit)
  - [ ] Session 3: Admin panel & troubleshooting (30 menit)
  - [ ] Q&A session (15 menit)

- [ ] **Create troubleshooting guide**

  ````markdown
  # Troubleshooting Guide

  ## Common Issues

  ### Bot tidak merespons

  1. Cek koneksi internet
  2. Refresh halaman
  3. Coba lagi dalam beberapa menit
  4. Jika masih bermasalah, hubungi IT: ext. 1234

  ### Jawaban tidak akurat

  1. Coba rephrase pertanyaan
  2. Gunakan kata kunci yang lebih spesifik
  3. Laporkan via feedback button
  4. Tim akan review dan update

  ### Error "Server tidak tersedia"

  - Sistem mungkin sedang maintenance
  - Coba lagi dalam 5-10 menit
  - Jika berlanjut, hubungi IT

  ## Admin Troubleshooting

  ### Upload dokumen gagal

  1. Pastikan file format PDF
  2. Ukuran max 10MB
  3. Coba upload ulang
  4. Check server logs: /opt/ngoerah-assistant/logs/backend.log

  ### Server restart commands

  ```bash
  sudo supervisorctl restart all
  sudo systemctl restart nginx
  ```
  ````

  ```

  ```

### Day 80-81: Monitoring Setup

- [ ] **Install Prometheus**

  ```bash
  # Download Prometheus
  wget https://github.com/prometheus/prometheus/releases/download/v2.48.0/prometheus-2.48.0.linux-amd64.tar.gz
  tar xvfz prometheus-*.tar.gz

  # Configure prometheus.yml
  global:
    scrape_interval: 15s

  scrape_configs:
    - job_name: 'ngoerah-backend'
      static_configs:
        - targets: ['localhost:8000']
      metrics_path: /metrics
  ```

- [ ] **Install Grafana**

  ```bash
  sudo apt install -y software-properties-common
  sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
  wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
  sudo apt update
  sudo apt install grafana

  sudo systemctl start grafana-server
  # Access: http://localhost:3000
  ```

- [ ] **Create Grafana dashboards**

  - API latency over time
  - Request volume
  - Error rate
  - LLM inference time
  - Cache hit rate
  - Active users

- [ ] **Setup alerts**

  ```yaml
  # alertmanager.yml
  global:
    smtp_smarthost: "smtp.sanglah.go.id:587"
    smtp_from: "assistant-alert@sanglah.go.id"

  route:
    receiver: "it-team"

  receivers:
    - name: "it-team"
      email_configs:
        - to: "it-team@sanglah.go.id"
          subject: "[ALERT] Ngoerah Assistant: {{ .GroupLabels.alertname }}"

  # Alert rules
  groups:
    - name: ngoerah-assistant
      rules:
        - alert: HighErrorRate
          expr: rate(http_requests_total{status="500"}[5m]) > 0.1
          for: 5m
          labels:
            severity: critical
          annotations:
            summary: High error rate detected

        - alert: SlowResponseTime
          expr: http_request_duration_seconds{quantile="0.95"} > 10
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: Response time above threshold

        - alert: ServerDown
          expr: up == 0
          for: 1m
          labels:
            severity: critical
          annotations:
            summary: Server is down
  ```

### Day 82-83: Backup & Recovery

- [ ] **Setup automated backups**

  ```bash
  # /opt/ngoerah-assistant/scripts/backup.sh
  #!/bin/bash

  BACKUP_DIR="/backup/ngoerah-assistant"
  DATE=$(date +%Y%m%d_%H%M%S)

  # Create backup directory
  mkdir -p $BACKUP_DIR/$DATE

  # Backup database
  pg_dump -U ngoerah_user ngoerah_assistant > $BACKUP_DIR/$DATE/database.sql

  # Backup documents
  tar -czf $BACKUP_DIR/$DATE/documents.tar.gz /opt/ngoerah-assistant/data/documents/

  # Backup configuration
  cp /opt/ngoerah-assistant/.env $BACKUP_DIR/$DATE/
  cp -r /opt/ngoerah-assistant/logs $BACKUP_DIR/$DATE/

  # Remove backups older than 30 days
  find $BACKUP_DIR -type d -mtime +30 -exec rm -rf {} +

  # Log success
  echo "$(date): Backup completed successfully" >> /var/log/ngoerah-backup.log
  ```

- [ ] **Schedule daily backups**

  ```bash
  # Add to crontab
  crontab -e

  # Add line:
  0 2 * * * /opt/ngoerah-assistant/scripts/backup.sh
  ```

- [ ] **Create recovery procedure**

  ````markdown
  # Disaster Recovery Procedure

  ## Database Recovery

  1. Stop all services
     ```bash
     sudo supervisorctl stop all
     ```
  ````

  2. Restore database

     ```bash
     psql -U postgres -d ngoerah_assistant < /backup/ngoerah-assistant/YYYYMMDD/database.sql
     ```

  3. Restore documents

     ```bash
     tar -xzf /backup/ngoerah-assistant/YYYYMMDD/documents.tar.gz -C /
     ```

  4. Restart services

     ```bash
     sudo supervisorctl start all
     ```

  5. Verify system
     ```bash
     curl http://localhost:8000/health
     ```

  ```

  ```

### Day 84-85: Go-Live

- [ ] **Pre-launch checklist**

  - [ ] All tests passing
  - [ ] Performance targets met
  - [ ] Security audit completed
  - [ ] Backups configured
  - [ ] Monitoring active
  - [ ] Documentation complete
  - [ ] Staff trained
  - [ ] Rollback plan ready

- [ ] **Soft launch (Limited users)**

  - Enable access for 20-30 internal users
  - Monitor closely for 3 days
  - Collect feedback
  - Fix any issues

- [ ] **Full launch**

  - Announce to all staff via email/intranet
  - Publish mobile app to internal app store
  - Monitor usage and feedback

- [ ] **Post-launch monitoring (1 week)**

  - Daily check of error logs
  - Weekly analytics review
  - Address user feedback
  - Performance optimization if needed

- [ ] **✅ Checkpoint:** System live and stable

---

## 23. Appendix

### A. Prompt Templates

#### A.1. Intent Classification Prompt

```
Analyze this user message and classify the intent.

User Message: "{user_message}"

Possible Intents:
1. FAQ_QUERY - User asking for information about hospital services, schedules, facilities, procedures
2. REGISTRATION - User wants to register, book appointment, or get registration link
3. EMERGENCY - Urgent medical situation requiring immediate action
4. COMPLAINT - User has a complaint or negative feedback
5. GREETING - User is greeting or starting conversation
6. CHITCHAT - Casual conversation not related to hospital services
7. OUT_OF_SCOPE - Question not related to hospital services

Respond ONLY with JSON (no explanation):
{"intent": "FAQ_QUERY", "confidence": 0.95, "sub_intent": "doctor_schedule"}
```

#### A.2. RAG Generation Prompt

```
Kamu adalah asisten virtual RSUP Prof. dr. I.G.N.G. Ngoerah (Sanglah).
Tugasmu adalah menjawab pertanyaan pasien dengan ramah dan informatif.

KONTEKS DARI DOKUMEN RESMI RS:
{context}

PERTANYAAN PASIEN:
{question}

INSTRUKSI:
1. Jawab dalam bahasa Indonesia yang sopan dan mudah dipahami
2. HANYA gunakan informasi dari konteks di atas
3. Jika informasi tidak tersedia, katakan dengan jelas bahwa kamu tidak memiliki informasi tersebut
4. Jangan mengarang atau berasumsi informasi
5. Berikan jawaban yang ringkas (maksimal 3-4 kalimat)
6. Jika relevan, sebutkan sumber dokumen
7. Untuk pertanyaan urgent/darurat, selalu arahkan ke IGD atau call center

JAWABAN:
```

#### A.3. Fallback Response Prompt

```
User bertanya sesuatu yang tidak ada dalam knowledge base.

Pertanyaan: "{question}"

Berikan respons yang:
1. Meminta maaf karena tidak memiliki informasi
2. Menyarankan untuk menghubungi call center (0361) 227911
3. Jika memungkinkan, tawarkan topik terkait yang mungkin bisa dibantu
4. Tetap ramah dan helpful

Format respons dalam bahasa Indonesia yang sopan.
```

### B. Sample Test Questions

#### B.1. FAQ Questions (50)

| No  | Question                             | Expected Intent | Expected Keywords        |
| --- | ------------------------------------ | --------------- | ------------------------ |
| 1   | Jam besuk ICU kapan?                 | FAQ_QUERY       | 11.00, 17.00, ICU        |
| 2   | Jadwal dokter anak hari Senin siapa? | FAQ_QUERY       | Senin, anak, dokter      |
| 3   | Bagaimana cara daftar BPJS?          | FAQ_QUERY       | BPJS, daftar, syarat     |
| 4   | Di mana lokasi poli mata?            | FAQ_QUERY       | mata, poli, lokasi       |
| 5   | Berapa biaya rawat inap kelas 3?     | FAQ_QUERY       | biaya, rawat inap, kelas |
| 6   | Parkir pengunjung dimana?            | FAQ_QUERY       | parkir, lokasi           |
| 7   | Jam operasional IGD?                 | FAQ_QUERY       | IGD, jam, 24 jam         |
| 8   | Apa saja fasilitas untuk pasien?     | FAQ_QUERY       | fasilitas, pasien        |
| 9   | Syarat masuk ICU apa saja?           | FAQ_QUERY       | ICU, syarat              |
| 10  | Bagaimana prosedur operasi?          | FAQ_QUERY       | operasi, prosedur        |
| ... | ...                                  | ...             | ...                      |

#### B.2. Registration Questions (20)

| No  | Question                    | Expected Intent | Expected Link     |
| --- | --------------------------- | --------------- | ----------------- |
| 1   | Saya mau daftar             | REGISTRATION    | /daftar           |
| 2   | Gimana cara booking dokter? | REGISTRATION    | /daftar           |
| 3   | Daftar ke poli anak         | REGISTRATION    | /daftar?poli=anak |
| ... | ...                         | ...             | ...               |

#### B.3. Edge Cases (30)

| No  | Question                                   | Expected Behavior               |
| --- | ------------------------------------------ | ------------------------------- |
| 1   | (empty message)                            | Return error: message too short |
| 2   | asd                                        | Return error: message too short |
| 3   | Script injection <script>alert(1)</script> | Sanitize and process normally   |
| 4   | Very long message (500+ chars)             | Return error: message too long  |
| 5   | Offensive language                         | Return polite decline           |
| ... | ...                                        | ...                             |

### C. Glossary

| Term              | Definition                                                                                      |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| **RAG**           | Retrieval-Augmented Generation - AI technique combining document retrieval with text generation |
| **LLM**           | Large Language Model - AI model trained on large text datasets                                  |
| **Embedding**     | Vector representation of text for similarity comparison                                         |
| **Vector DB**     | Database optimized for storing and searching vector embeddings                                  |
| **Intent**        | The purpose or goal behind a user's message                                                     |
| **Hallucination** | When AI generates false or unsupported information                                              |
| **Chunk**         | A segment of document text used for retrieval                                                   |
| **pgvector**      | PostgreSQL extension for vector similarity search                                               |
| **Ollama**        | Tool for running LLMs locally                                                                   |
| **FastAPI**       | Modern Python web framework for building APIs                                                   |
| **Streamlit**     | Python library for creating web apps quickly                                                    |
| **Flutter**       | Google's UI toolkit for cross-platform apps                                                     |
| **Riverpod**      | State management library for Flutter                                                            |
| **Supervisor**    | Linux process manager to keep services running                                                  |
| **MVP**           | Minimum Viable Product - initial version with core features                                     |

### D. References & Resources

#### D.1. Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [PostgreSQL pgvector](https://github.com/pgvector/pgvector)
- [Flutter Documentation](https://docs.flutter.dev/)
- [Riverpod Documentation](https://riverpod.dev/)

#### D.2. Tutorials

- [Building RAG Applications with LangChain](https://python.langchain.com/docs/tutorials/rag/)
- [FastAPI + PostgreSQL Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Flutter State Management with Riverpod](https://codewithandrea.com/articles/flutter-state-management-riverpod/)

#### D.3. Related Papers

- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
- "Llama 2: Open Foundation and Fine-Tuned Chat Models" (Touvron et al., 2023)

### E. Project Timeline Summary

```mermaid
gantt
    title Ngoerah Smart Assistant Development Timeline
    dateFormat  YYYY-MM-DD

    section Phase 0
    Environment Setup     :p0, 2024-01-01, 5d

    section Phase 1
    LLM & RAG Foundation  :p1a, after p0, 7d
    RAG Pipeline          :p1b, after p1a, 7d
    API Endpoints         :p1c, after p1b, 7d

    section Phase 2
    Streamlit Frontend    :p2, after p1c, 7d

    section Phase 3
    Testing & Optimization:p3, after p2, 7d

    section Phase 4
    Deployment & UAT      :p4, after p3, 14d

    section Phase 5
    Flutter Development   :p5, after p4, 30d

    section Phase 6
    Production Launch     :p6, after p5, 14d
```

### F. Version History

| Version | Date       | Changes                                                              | Author |
| ------- | ---------- | -------------------------------------------------------------------- | ------ |
| 1.0.0   | 2024-01-01 | Initial PRD draft                                                    | Tim IT |
| 2.0.0   | 2026-01-13 | Complete PRD with detailed todolist, Flutter specs, deployment guide | Tim IT |

---

## 24. Final Notes

### Key Success Factors

1. **Focus on MVP** - Don't over-engineer. Get core features working first.
2. **Use Existing Tools** - LangChain, Ollama, Streamlit - don't reinvent the wheel.
3. **Iterate Fast** - Build, test, get feedback, improve. Repeat.
4. **Document Everything** - Future-you will thank present-you.
5. **Monitor Actively** - Set up alerts, check logs, respond to issues quickly.

### Estimated Total Timeline

| Phase               | Duration | Cumulative |
| ------------------- | -------- | ---------- |
| Phase 0: Setup      | 5 days   | 5 days     |
| Phase 1: Backend    | 21 days  | 26 days    |
| Phase 2: Streamlit  | 7 days   | 33 days    |
| Phase 3: Testing    | 7 days   | 40 days    |
| Phase 4: UAT        | 14 days  | 54 days    |
| Phase 5: Flutter    | 30 days  | 84 days    |
| Phase 6: Production | 14 days  | 98 days    |

**Total: ~3-4 months** (working full-time on this project)

For a side project with limited hours, expect 6-8 months.

### Contact

**Tim IT RSUP Prof. dr. I.G.N.G. Ngoerah**  
📧 Email: it@sanglah.go.id  
📞 Telp: (0361) 227911 ext. 1234

---

_Document generated with ❤️ for improving healthcare services at RSUP Sanglah_
