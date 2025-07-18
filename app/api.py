import os
from fastapi import APIRouter, UploadFile, File, Form
from app.document_parser import parse_and_index_file
from app.query_processor import parse_query_to_csv, parse_query_to_json
from app.vector_store import retrieve_relevant_chunks
from app.decision_maker import make_decision

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    filepath = os.path.join("storage/documents", file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())
    parse_and_index_file(filepath)
    return {"message": f"{file.filename} uploaded and indexed successfully"}


@router.post("/conclude")
async def conclude_claim(query: str = Form(...)):
    csv_string = parse_query_to_csv(query)
    structured = parse_query_to_json(query)
    chunks = retrieve_relevant_chunks(csv_string)
    decision = make_decision(structured, chunks)
    return decision
