# BanglaSupport-LLM Backend Service

Enterprise FastAPI backend delivering real-time streaming customer support using QLoRA fine-tuned Bangla models, Pinecone RAG, and agentic order tracking tools.

## Setup & Running

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Start Server**:
```bash
python -m uvicorn Backend.main:app --reload --port 8000
```

3. **API Endpoints**:
- `POST /api/chat/stream`: Streamed SSE endpoint for chat requests.
- `POST /api/admin/documents/upload`: Upload policy PDFs/TXT/MD into vector store.
