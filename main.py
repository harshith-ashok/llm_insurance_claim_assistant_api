from fastapi import FastAPI, UploadFile, File, Form
from document_handler import save_and_extract
from query_processor import structure_query
from decision_engine import make_decision
from models.schemas import QueryRequest, DecisionResponse
import os
from typing import Optional


app = FastAPI()
documents_by_file = {}


@app.post("/upload")
async def upload_doc(file: UploadFile = File(...), filename: Optional[str] = Form(None)):
    used_name = filename or file.filename
    text = save_and_extract(file)
    documents_by_file[used_name] = text
    return {"message": f"{used_name} processed"}



@app.post("/evaluate", response_model=DecisionResponse)
async def evaluate_claim(payload: QueryRequest):
    structured = structure_query(payload.query)
    result = make_decision(structured, documents_by_file)
    return result
