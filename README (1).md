# Personal Ayurveda Doctor AI

A lightweight, open‑source project for an AI-powered personal doctor rooted in Ayurveda, built with free tools and a clear path for future expansion.

---

## 📖 Project Overview

This project delivers an AI-based Personal Doctor using Ayurvedic principles. It:
- Assesses your constitution (dosha) and current imbalances
- Tracks mood, symptoms, and meals
- Integrates local climate data
- Generates personalized meal plans and herbal advice using a hybrid RAG + multi-agent approach

All components run on open-source/free-tier resources.

---

## 🛠️ Tech Stack

- **Backend & Orchestration**: FastAPI + LangChain + AutoGen OSS  
  Leverages Retrieval-Augmented Generation (RAG) pipelines for contextually grounded Ayurvedic guidance and explicit multi-agent workflows for safety and precision.

- **LLM**: Local Llama 2 (7B) or Mistral 7B fine-tuned with LoRA/QLoRA; upgradeable to BioMedLM for enhanced medical accuracy.

- **Vector Store**: ChromaDB (local mode) for RAG; easily swappable to Qdrant or Pinecone in production.

- **Database**: SQLite for MVP (upgradable to PostgreSQL with Redis for session memory).

- **Frontend**: Next.js + Tailwind CSS

- **Local Dev**: Docker Compose

- **CI/CD**: GitHub Actions → Docker Hub / Railway / Heroku free tier

---

## 🚀 Getting Started

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/ayurveda-doctor-ai.git
   cd ayurveda-doctor-ai
   ```

2. **Configure environment**
   - Install Python 3.10+, Node.js 16+
   - Copy & adjust `.env.example` to `.env` with any API keys

3. **Build & run with Docker Compose**
   ```bash
   docker-compose up --build
   ```
   - FastAPI: http://localhost:8000/docs
   - Next.js: http://localhost:3000

4. **Load Ayurvedic embeddings**
   ```bash
   python scripts/generate_embeddings.py
   ```

5. **Test agent pipeline**
   ```bash
   curl -X GET http://localhost:8000/recommendations/diet
   ```

---

## 🔮 Roadmap & Milestones

### MVP: Core Agents & API (Weeks 1–2)
1. Scaffold FastAPI service and dependencies
2. Implement AutoGen agents for:
   - **UserProxyAgent**
   - **DoshaAssessmentAgent**
   - **MentalHealthAgent**
   - **ClimateAgent**
   - **DeficiencyAgent**
   - **MealPlannerAgent**
   - **HerbalAdvisorAgent**
   - **MemoryManager**
3. Expose `/log/mood`, `/log/symptom`, `/log/meal`, `/recommendations/diet`
4. Verify local LLM and RAG inference

### Phase 2: UI & Data Persistence (Weeks 3–4)
1. Build Next.js UI for logging & plan display
2. Persist logs in SQLite
3. Show historical trends
4. Containerize frontend and backend

### Phase 3: Expand Capabilities (Weeks 5–6)
1. Integrate Weather API
2. Add feedback loop with ratings
3. Write tests with pytest

### Phase 4+: Scaling & Production
1. Swap to Postgres + Redis
2. Deploy to free-tier hosting
3. Add CI/CD pipeline

---

## 🤖 Autogen Agent Implementation

1. **Environment & Dependencies**: `backend/requirements.txt`
2. **Config**: `backend/.env`
3. **Agents**: `backend/app/agents/*.py`
4. **Orchestrator**: `backend/app/orchestrator.py`
5. **FastAPI App**: `backend/app/main.py`
6. **Tests**: `backend/tests/`

---

## 📂 Project Structure

```text
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── orchestrator.py
│   │   └── agents/
│   ├── scripts/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
├── docker-compose.yml
└── README.md
```

---

## 👍 Contributing & Next Steps

- **Scaffold** the FastAPI backend and define agent prompts in `backend/app/agents/`
- **Populate** `data/ayurveda_corpus/` with trusted texts
- **Open an issue** for any bugs or feature suggestions
- **Submit PRs** following the roadmap milestones
