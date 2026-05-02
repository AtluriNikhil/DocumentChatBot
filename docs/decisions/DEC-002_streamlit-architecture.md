# DEC-002: Streamlit UI Architecture

**Date:** 2026-01-24
**Category:** Architecture
**Status:** Accepted

---

## Context

Need to build an interactive frontend for the RAG Document Assistant that allows users to upload documents, ask questions, and view answers with source citations.

## Decision

Build a Streamlit application that communicates with the FastAPI backend via HTTP, using sidebar + main layout with native chat components.

## Alternatives Considered

### Backend Communication

1. **HTTP to FastAPI** - Selected
   - Decoupled architecture
   - Matches production deployment pattern
   - Can scale independently (UI on one server, API on another)
   - Forces proper API design

2. **Direct Python imports** - Rejected
   - Tight coupling between UI and backend
   - Cannot deploy separately
   - Harder to test independently
   - Bypasses API validation layer

### UI Layout

1. **Sidebar + Main (Recommended)** - Selected
   - Sidebar: Document upload, settings, provider selection
   - Main: Chat interface with message history
   - Standard pattern for chat applications
   - Clean separation of controls and content

2. **Single Column** - Rejected
   - Requires excessive scrolling
   - Poor UX for frequent setting changes

3. **Wide Mode with Side-by-side** - Rejected
   - Good for showing sources alongside answers
   - Deferred to Sprint 2 enhancement

### Chat Components

1. **st.chat_message (Native)** - Selected
   - Built-in Streamlit chat bubbles
   - Automatic styling and icons
   - User/assistant role support
   - Less code to maintain

2. **Custom cards with st.container** - Rejected
   - More control over styling
   - Significantly more code
   - Reinventing existing functionality

## Rationale

**HTTP Communication:**
The HTTP approach prepares the application for production deployment. It enforces a proper API contract, makes testing easier (can test UI and API separately), and allows horizontal scaling. The slight overhead of HTTP calls is negligible for this use case.

**Sidebar Layout:**
Users configure settings infrequently but chat frequently. The sidebar keeps controls accessible without cluttering the main chat area. This matches user expectations from other chat interfaces.

**Native Components:**
Streamlit's `st.chat_message` provides a polished chat experience out of the box. Using native components reduces maintenance burden and ensures consistency with Streamlit's design language.

## Implications

- FastAPI backend must be running for Streamlit app to function
- API must handle CORS for local development
- Session state management needed for chat history
- Error handling required for HTTP failures (backend offline, network issues)
- Can add WebSocket streaming later without UI redesign

## Implementation Details

**File Structure:**
```
app/
└── streamlit_app.py    # Main application
```

**Key Features:**
- Document uploader (PDF, MD, TXT) in sidebar
- LLM provider selector (OpenAI, Anthropic, Ollama)
- Document count display and clear function
- Chat interface with message history
- Expandable source citations below answers
- Error messages for backend communication issues

**API Base URL:**
- Development: `http://localhost:8000`
- Configurable via environment variable for production

## Related

- `src/api/main.py`: FastAPI backend with CORS enabled
- `src/api/routes.py`: REST endpoints for ingestion and query
- Sprint 2 Day 6 implementation

## Future Enhancements

- WebSocket streaming for real-time responses
- Conversation export (JSON, PDF)
- Multi-session support with saved conversations
- Advanced settings (chunk size, top-k retrieval)
