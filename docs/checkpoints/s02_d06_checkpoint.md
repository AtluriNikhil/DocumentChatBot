# Sprint 2 - Day 6 Checkpoint: Streamlit UI

**Date:** 2026-01-25
**Phase:** Phase 3 - User Interface

---

## Objectives

Build interactive Streamlit frontend for document upload and Q&A with source citations.

## Completed

- [x] Streamlit app architecture design (DEC-002)
- [x] HTTP client for FastAPI backend communication
- [x] Document upload interface (multiple files)
- [x] Chat interface with message history
- [x] LLM provider selection dropdown
- [x] Source citation display (expandable)
- [x] Document management (count, clear all)
- [x] Session state management
- [x] End-to-end testing with sample documents
- [x] Multi-source conflict detection experiment (EXP-001)
- [x] User guidance and limitations documentation

## Outputs

| Type | Path | Description |
|------|------|-------------|
| App | `app/streamlit_app.py` | Main Streamlit application (~250 lines) |
| Decision | `docs/decisions/DEC-002_streamlit-architecture.md` | Architecture decision record |
| Experiment | `docs/experiments/EXP-001_multi-source-detection.md` | Conflict detection experiment |
| Test Data | `data/experiments/policy_2023.md` | Test policy file (30-day refund) |
| Test Data | `data/experiments/policy_2024.md` | Test policy file (60-day refund) |

## Features Implemented

| Feature | Description |
|---------|-------------|
| **Sidebar Layout** | Settings, upload, and stats in sidebar; chat in main area |
| **Multi-file Upload** | Upload multiple PDFs, TXT, MD files simultaneously |
| **Backend Health Check** | Visual indicator if FastAPI backend is offline |
| **Provider Selection** | Choose between OpenAI, Anthropic, Ollama |
| **Chat Interface** | Native Streamlit chat bubbles with user/assistant roles |
| **Source Citations** | Expandable sections showing retrieved document chunks |
| **Document Stats** | Real-time count of indexed documents |
| **Clear All** | Remove all documents and reset chat history |
| **Duplicate Prevention** | Track uploaded files to prevent re-processing |

## Architecture Decisions

**HTTP Communication** (DEC-002):
- Streamlit communicates with FastAPI via REST API
- Enables decoupled deployment and independent scaling
- Base URL: `http://localhost:8000`

**UI Components**:
- Sidebar + Main layout pattern
- Native `st.chat_message` for chat bubbles
- `st.file_uploader` with `accept_multiple_files=True`
- Session state for messages, provider, processed files

## Test Results

**Manual Testing:**
- ✅ Backend health check displays correctly
- ✅ Multiple file upload works without flickering
- ✅ Document count updates after upload
- ✅ Chat interface responds to questions
- ✅ Source citations display in expandable sections
- ✅ Provider selection persists across reruns
- ✅ Clear all documents resets state

**Sample Interaction:**
```
User: "What is this document for testing?"
Assistant: "The document is a sample text document for testing the RAG system..."
Sources: 4 chunks from sample.txt and sample.md displayed
```

## Issues Encountered

| Issue | Resolution |
|-------|------------|
| API returns `providers` not `models` | Updated `get_available_models()` to parse correct field |
| Upload expects `files` parameter | Changed from `file` to `files` in request |
| Wrong response field `num_chunks` | Changed to `chunks_created` per API schema |
| File uploader flickering on rerun | Added session state to track processed files |

## Decisions Made

DEC-002: Streamlit UI Architecture
- HTTP communication over direct imports
- Sidebar + main layout
- Native chat components

---

## Experiments Conducted

### EXP-001: Multi-Source Conflict Detection

**Reference:** [docs/experiments/EXP-001_multi-source-detection.md](../experiments/EXP-001_multi-source-detection.md)

**Objective:** Test whether the RAG system can identify and cite different sources when documents contain conflicting information.

**Setup (per DSM C.1 Experiment Tracking):**
| Parameter | Value |
|-----------|-------|
| experiment_name | multi-source-conflict-detection |
| LLM Provider | OpenAI (gpt-4o-mini) |
| Retrieval k | 4 |
| Embeddings | text-embedding-ada-002 |
| Test Files | policy_2023.md, policy_2024.md |

**Results Summary:**

| Query Type | Multi-Source Detection | Conflict Identification |
|------------|------------------------|------------------------|
| Simple question | Partial | No |
| Explicit "differences" query | Yes | Yes |
| Question with implicit conflict | Yes | Yes |

**Key Findings:**
1. Retrieval works correctly - both conflicting sources retrieved
2. Citation inconsistent - simple queries may cite only one source
3. Conflict detection depends on query phrasing
4. LLM reasoning helps when context implies conflict

**Limitations Identified:**
- Single-answer queries may miss conflicts
- No automatic version/date awareness
- Relies on LLM reasoning, not systematic detection

**Documentation Added:**
- User guidance in UI (Tips & Limitations expander)
- Limitations section in README
- Future improvement roadmap in experiment doc

---

## Methodology Analysis

**DSM Gap Identified:** While documenting EXP-001, found that DSM C.1 Experiment Tracking is optimized for ML experiments with numeric metrics. Capability experiments (qualitative pass/fail/partial results) lack a standardized template.

**Action Taken:** Created enhancement proposal for DSM methodology:
- Location: `D:\data-science\agentic-ai-data-science-methodology\plan\backlog\BACKLOG-001_capability-experiment-template.md`
- Proposes C.1.1 Capability Experiment Template
- References existing frameworks (RAGAS, MLflow) and identifies documentation gap
- Status: Implemented

---

## Cumulative Progress

| Day | Feature | Status |
|-----|---------|--------|
| Day 1-5 | Sprint 1 | Complete (84 tests) |
| Day 6 | Streamlit UI | Complete |

## Ready for Day 7

- [x] Streamlit app functional
- [x] HTTP client working
- [x] All UI features tested
- [x] Architecture documented

## Next Day Preview

**Day 7: German Language Support**
- Multilingual embeddings (HuggingFace multilingual-e5)
- German prompt templates
- Language detection for queries
- German test documents
