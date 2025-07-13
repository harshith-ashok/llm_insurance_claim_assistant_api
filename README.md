# Insurance Claim Assistant using LLMs
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
| `main.py`                | FastAPI web server with file upload, query, and web UI |
| `query_processor.py`     | Calls Ollama LLM with prompt and returns result |
| `decision_engine.py`     | Prepares prompt and parses structured JSON decision |
| `document_handler.py`    | Extracts text from PDFs, DOCX, HTML files |
| `models/schemas.py`      | Defines request/response models for FastAPI |
| `data/pdfs/`             | Stores uploaded documents (temporary storage) |

---

## Running the App

1. Start Ollama with your model (e.g. `llama3`, `mistral`, etc):
`ollama run llama3`

2. Start the FastAPI server:
`uvicorn main:app --reload`

3. Open your browser at:
`http://localhost:8000`

You can upload documents and enter queries via the UI.

## Curl Test
- Upload a Document

```
curl -X POST http://localhost:8000/upload \
  -F 'file=@/path/to/your/policy.pdf'
```

- Submit a Query

```
curl -X POST http://localhost:8000/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
}
```

- Sample Output

```{
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

- Web form at / for human interaction

## Requirements

- `python 3.9+`
- `ollama`
- `fastapi`
- `uvicorn`
- `python-docx`
- `PyMuPDF`
- `beautifulsoup4`
- `pydantic`
