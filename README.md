# rag-document-assistant

A document Q&A app built with FastAPI, Streamlit, LangChain, and Novita AI.

It lets you:
- upload `pdf`, `txt`, and `md` files
- index them with embeddings
- ask questions against the uploaded documents
- use Novita AI for both chat generation and embeddings

## Stack

- FastAPI backend
- Streamlit frontend
- LangChain orchestration
- Novita AI OpenAI-compatible chat + embeddings
- Persisted in-memory vector store

## Requirements

- Python 3.10+
- A Novita AI API key

## Setup

Clone the repo and create a virtual environment:

```powershell
py -3 -m venv venv
.\venv\Scripts\python -m pip install --upgrade pip
.\venv\Scripts\python -m pip install -e .
```

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:

```env
NOVITA_API_KEY=your_novita_api_key
```

## Run

Start the backend:

```powershell
.\venv\Scripts\Activate.ps1
python -m uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

In a second terminal, start the UI:

```powershell
.\venv\Scripts\Activate.ps1
streamlit run app/streamlit_app.py
```

Open:

- `http://127.0.0.1:8501` for Streamlit
- `http://127.0.0.1:8000/health` for backend health

## How To Use

1. Start the backend and Streamlit UI.
2. Open the Streamlit app in your browser.
3. Upload one or more documents from the sidebar.
4. Wait for indexing to finish.
5. Ask questions in the chat input.

## Environment

Important settings in `.env`:

```env
LLM_PROVIDER=novita
NOVITA_MODEL=meta-llama/llama-3.3-70b-instruct
NOVITA_BASE_URL=https://api.novita.ai/openai

EMBEDDING_PROVIDER=novita
EMBEDDING_MODEL=baai/bge-m3
```

`.env` is ignored by Git. Commit `.env.example`, not `.env`.

## Notes

- The app is configured to use `127.0.0.1` for local backend calls.
- Uvicorn `--reload` can be noisy on some Windows setups, so the recommended command above does not use it.
- Indexed document state is stored locally under `data/`.

## Troubleshooting

If uploads fail:

- confirm `NOVITA_API_KEY` is set in `.env`
- confirm the backend is still running
- confirm `http://127.0.0.1:8000/health` responds
- test embeddings directly:

```powershell
.\venv\Scripts\python -c "from src.vectorstore.embeddings import get_embeddings; e=get_embeddings(); print(e.embed_query('ping')[:5])"
```

## Git

Recommended push flow:

```powershell
git add .
git commit -m "Switch RAG app to Novita and stabilize local runtime"
git push origin main
```
