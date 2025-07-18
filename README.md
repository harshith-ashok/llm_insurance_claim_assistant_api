# Insurance Claim Assistant using LLMs API
> Project built for HackRx 6.0 - Bajaj Finserv

This system allows users to upload insurance documents (PDF, Word, HTML) and ask natural-language questions like:
`“46-year-old male, knee surgery in Pune, 3-month-old insurance policy”`

The system then:
- Parses the query into structured data
- Retrieves relevant clauses from uploaded documents
- Uses an LLM (via Ollama) to evaluate claim eligibility
- Returns a structured JSON decision, referencing specific clauses

##  File Overview

| File / Folder             | Purpose |
|--------------------------|---------|
| `main.py`                | Main file that routes to `api.py` |
| `app/query_processor.py`     | Calls Ollama LLM with prompt and returns result |
| `app/decision_maker.py`     | Prepares prompt and parses structured JSON decision |
| `app/document_parser.py`    | Extracts text from PDFs, DOCX, HTML files |
| `api/api.py`      | Defines request/response routes for FastAPI |
| `storage/documents/`             | Stores uploaded documents (temporary storage) |

---

## Running the App

1. Start Ollama with your model (e.g. `llama3`, `mistral`, etc):
`ollama run llama3`

2. Start the FastAPI server:
`uvicorn main:app --reload`

1. The API runs at:
`http://localhost:8000`

You can upload documents and enter queries via the UI.

## Curl Test
- Upload a Document

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/Users/harshith/Downloads/dfs/CHOTGDP23004V012223.pdf"
```

- Submit a Query

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/Users/harshith/Downloads/dfs/ICIHLIP22012V012223.pdf"
```

- Sample Output

```json
{
  "decision": "approved",
  "amount": 50000,
  "justification": "Clause 4.2 in CHOTGDP23004V012223.pdf mentions surgery after 90 days.",
  "clauses_used": [
    {
      "file": "CHOTGDP23004V012223.pdf",
      "clause": "Clause 4.2: Knee surgery covered after 90 days."
    }
  ]
}
```

## Features
- Local LLM with Ollama (no cloud dependency)

- Upload PDFs, DOCX, HTML

- Natural language query support

- Clause-based justification from source documents

- JSON-based API for downstream use

- API Endpoints at / for web & app interface

## Requirements

- `fastapi`
- `uvicorn`
- `python-multipart`
- `pymupdf`
- `python-docx`
- `beautifulsoup4`
- `faiss-cpu`
- `sentence-transformers`
- `httpx`