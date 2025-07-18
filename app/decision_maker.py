import subprocess
import json


def make_decision(structured_query, docs):
    context = ""
    for doc in docs:
        context += f"\n### FILE: {doc['source']}\n{doc['text'][:4000]}\n"

    prompt = f"""
    You are an insurance claim assistant AI. Based only on the documents below, do the following:

    1. Decide if the claim is APPROVED or REJECTED.
    2. Estimate the CLAIM AMOUNT based on clauses such as sub-limits, sum insured, surgery cost limits, or any financial constraints mentioned in the documents. DO NOT GUESS or use average values.
    3. Justify your decision with exact clause references.
    4. Clearly mention the FILE NAME from which each part of the justification or amount was derived.

    QUERY:
    {structured_query}

    DOCUMENTS:
    {docs}

    Respond ONLY in valid JSON like this:
    {{
    "decision": "approved",
    "amount": "₹24000",
    "justification": "Knee surgery is covered under 'Special Treatment' (File: ABC123.pdf) and the sub-limit for such surgeries is ₹24000 as per clause 4(b) of the same file."
    }}

    IMPORTANT RULES:
    - If amount can't be calculated from document clauses, say "₹0" and explain why.
    - NEVER invent or hallucinate any details.
    """

    res = subprocess.run(["ollama", "run", "llama3", prompt],
                         capture_output=True, text=True)
    return json.loads(res.stdout.strip())
