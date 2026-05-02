# Project Plan: RAG Document Assistant

**Repository:** `rag-document-assistant`
**Created:** 2026-01-17
**Status:** Sprint 2 Complete
**Last Updated:** 2026-01-26

---

## GitHub Metadata

### Repository Name
```
rag-document-assistant
```

### Description
```
Production-ready RAG system with multi-provider LLM support (OpenAI, Claude, Ollama), vector database integration, FastAPI backend, and MLflow evaluation. Features German language support and Streamlit UI.
```

### Topics
```
rag, langchain, langgraph, llm, vector-database, chromadb, pinecone, fastapi, mlflow, streamlit, openai, anthropic, ollama, python, nlp, retrieval-augmented-generation, document-qa, embeddings
```

---

## Project Rationale

Based on analysis of 19 job openings (Senior Data Scientist / ML Engineer / AI Engineer) in Germany, this project addresses the most in-demand skills:

| Skill | Job Coverage | Project Feature |
|-------|--------------|-----------------|
| RAG Systems | 80% | Core functionality |
| LLMs/GenAI | 90% | Multi-provider support |
| Vector Databases | 60% | ChromaDB + Pinecone |
| MLOps/MLflow | 85% | Evaluation pipeline |
| FastAPI | 40% | REST backend |
| German Language | 25% | Unique differentiator |

---

## Tech Stack

### Core
- **LangChain** ; RAG chain orchestration
- **LangGraph** ; Advanced agent workflows
- **OpenAI API** ; GPT-4o, embeddings
- **Anthropic Claude** ; Alternative LLM provider
- **Ollama** ; Local model support

### Vector Database
- **ChromaDB** ; Local development
- **Pinecone** ; Cloud option (optional)

### Embeddings
- **OpenAI text-embedding-ada-002** ; Primary
- **HuggingFace multilingual-e5-large** ; German support

### Backend
- **FastAPI** ; REST API
- **Pydantic** ; Validation
- **uvicorn** ; ASGI server

### Evaluation
- **MLflow** ; Experiment tracking
- **Custom metrics** ; Faithfulness, relevance, latency

### UI
- **Streamlit** ; Interactive interface

### Testing
- **pytest** ; Unit/integration tests
- **pytest-cov** ; Coverage (target 80%+)

### Deployment
- **Docker** ; Containerization
- **Streamlit Cloud** ; Live demo

---

## Sprint 1 (5 Days): Core RAG System ✓ COMPLETE

### Day 1: Project Setup & Document Ingestion ✓

**Tasks:**
- [x] Initialize repository with proper structure
- [x] Set up environment (Poetry/uv, pre-commit hooks, pytest)
- [x] Implement document loaders (PDF, Markdown, TXT) using LangChain
- [x] Create chunking strategy with configurable overlap/size
- [x] Write unit tests for document processing

**Deliverables:**
- ✓ Working document ingestion pipeline
- ✓ Tests passing for loaders and chunking

---

### Day 2: Vector Database & Embeddings ✓

**Tasks:**
- [x] Integrate ChromaDB (local)
- [x] Implement embedding generation (OpenAI ada-002)
- [x] Build vector store abstraction layer
- [x] Create document indexing pipeline with metadata
- [x] Add similarity search with configurable top-k

**Deliverables:**
- ✓ Vector store with document indexing
- ✓ Embedding provider abstraction

---

### Day 3: RAG Chain & LLM Integration ✓

**Tasks:**
- [x] Build retrieval chain with LangChain
- [x] Implement multi-provider LLM support (OpenAI, Claude, Ollama)
- [x] Create prompt templates with source attribution
- [x] Add conversation memory for multi-turn queries
- [ ] ~~Implement streaming responses~~ (deferred)

**Deliverables:**
- ✓ Working RAG chain with LLM integration
- ✓ Multi-provider switching capability

---

### Day 4: FastAPI Backend ✓

**Tasks:**
- [x] Build REST API endpoints (/ingest, /query, /health, /models)
- [x] Add async document processing
- [x] Implement request validation (Pydantic)
- [x] Create OpenAPI documentation
- [x] Add basic error handling

**Deliverables:**
- ✓ FastAPI server with documented endpoints
- ✓ Async ingestion support

---

### Day 5: MLflow Evaluation & Testing ✓

**Tasks:**
- [x] Set up MLflow experiment tracking
- [x] Implement evaluation metrics (faithfulness, relevance, latency)
- [x] Create test dataset with ground-truth Q&A pairs
- [x] Log metrics per query (retrieval quality, generation quality)
- [x] Write integration tests (84 tests, 73% coverage)

**Deliverables:**
- ✓ MLflow evaluation pipeline
- ✓ Test coverage report

---

## Sprint 1 Milestone ✓ ACHIEVED

**Working RAG system with:**
- ✓ FastAPI backend
- ✓ Multi-provider LLM support
- ✓ Vector database integration
- ✓ MLflow evaluation

---

## Sprint 2 (1 Day): User Interface ✓ COMPLETE

### Day 6: Streamlit Interface ✓

**Tasks:**
- [x] Build document upload interface (multiple files)
- [x] Create chat interface with message history
- [x] Add source visualization (expandable sections)
- [x] Implement conversation history display
- [x] Add configuration sidebar (model selection)
- [x] Conduct capability experiment (EXP-001: Multi-source conflict detection)
- [x] Document limitations in UI and README

**Deliverables:**
- ✓ Interactive Streamlit UI (`app/streamlit_app.py`)
- ✓ Document upload and chat functionality
- ✓ Architecture decision (DEC-002)
- ✓ Experiment documentation (EXP-001)

**Documentation:**
- Checkpoint: `docs/checkpoints/s02_d06_checkpoint.md`
- Decision: `docs/decisions/DEC-002_streamlit-architecture.md`
- Experiment: `docs/experiments/EXP-001_multi-source-detection.md`

---

## Sprint 2 Milestone ✓ ACHIEVED

**User interface complete:**
- ✓ Streamlit UI with HTTP backend communication
- ✓ Multi-file upload with duplicate prevention
- ✓ Chat interface with source citations
- ✓ First capability experiment conducted and documented

---

## Sprint 3: Experiments & Optimization

**See:** [sprint-3-plan.md](sprint-3-plan.md)

*Days 7-10 reorganized with experiment-driven approach following DSM C.1.1 Capability Experiment Template.*

---

## Folder Structure

```
rag-document-assistant/
├── src/
│   ├── __init__.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── loaders.py
│   │   └── chunking.py
│   ├── vectorstore/
│   │   ├── __init__.py
│   │   ├── embeddings.py
│   │   └── store.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   ├── chain.py
│   │   └── reranker.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── providers.py
│   │   └── prompts.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes.py
│   └── evaluation/
│       ├── __init__.py
│       └── metrics.py
├── app/
│   └── streamlit_app.py
├── tests/
│   ├── __init__.py
│   ├── test_ingestion.py
│   ├── test_retrieval.py
│   └── test_api.py
├── docs/
│   └── architecture.md
├── data/
│   └── sample_docs/
├── .env.example
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Test Coverage | 80%+ |
| Retrieval Accuracy | 85%+ (on test set) |
| Response Latency | <3s (p95) |
| Cost per Query | <$0.05 |
| German Performance | Within 10% of English |

---

## Portfolio Differentiators

1. **Multi-provider LLM support** (like DevFlow Analyzer)
2. **German language capability** (unique for Optimus Search, MHP, N26)
3. **Production patterns**: FastAPI, monitoring, cost tracking
4. **MLflow evaluation pipeline** (rigorous, not just a demo)
5. **Clean architecture** with proper testing
6. **Hybrid search** (advanced RAG technique)
7. **Real-time cost tracking** (production awareness)

---

## Target Companies (Direct Match)

| Company | Role | Key Match |
|---------|------|-----------|
| N26 | Data Scientist - GenAI | LangChain/LangGraph, agentic |
| intive | Senior ML Engineer | Vector DBs, MLOps |
| Delivery Hero | Senior AI Engineer | RAG, agentic systems |
| MHP | Senior DS AI & GenAI | RAG, LLMs, German |
| Zalando | ML Platform Engineer | LLM serving, RAG at scale |

---

## Next Steps

1. ~~Create GitHub repository~~ ✓
2. ~~Initialize project structure~~ ✓
3. ~~Complete Sprint 1 (Days 1-5)~~ ✓
4. ~~Complete Sprint 2 (Day 6)~~ ✓
5. Begin Sprint 3 (Days 7-10) - Experiments & Optimization
