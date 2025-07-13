import json
from query_processor import run_ollama_prompt


def make_decision(structured_query, documents_by_file):
    formatted_docs = ""
    for filename, text in documents_by_file.items():
        formatted_docs += f"\n### FILE: {filename}\n{text[:4000]}\n"

    prompt = f"""You are a claims evaluator AI.

You are given:
- A structured query
- A list of documents labeled with filenames like: `### FILE: CHOTGDP23004V012223.pdf`
- You must use only those exact filenames in your response.

Structured Query:
{json.dumps(structured_query, indent=2)}

Documents:
{formatted_docs}

Instructions:
1. Analyze the query using the documents.
2. If applicable, approve or reject the claim.
3. Always list the filename as exactly shown after `### FILE:` (no made-up names).
4. Output valid JSON in this exact format (no extra text):

{{
  "decision": "approved",
  "amount": 50000,
  "justification": "Clause 4.2 in CHOTGDP23004V012223.pdf mentions surgery after 90 days.",
  "clauses_used": [
    {{
      "file": "CHOTGDP23004V012223.pdf",
      "clause": "Clause 4.2: Knee surgery covered after 90 days."
    }}
  ]
}}
"""

    response = run_ollama_prompt(prompt)

    # Attempt to find the first JSON object in the response (in case extra tokens come before it)
    try:
        json_start = response.find("{")
        json_str = response[json_start:]
        return json.loads(json_str)
    except Exception:
        return {
            "decision": "rejected",
            "amount": 0,
            "justification": "LLM did not return valid JSON. Raw response:\n" + response,
            "clauses_used": []
        }
