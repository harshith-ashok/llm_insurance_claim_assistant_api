import subprocess
import json


def run_ollama_prompt(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    return result.stdout.strip()


def structure_query(raw_query):
    prompt = f"""
Extract the following fields from the input query:
- age (number)
- procedure (short string)
- location (city or region)
- policy_duration_months (convert things like "3-month-old" or "2 years" into months)

Input: "{raw_query}"

Respond ONLY in JSON format, like:
{{
  "age": 46,
  "procedure": "knee surgery",
  "location": "Pune",
  "policy_duration_months": 3
}}

Do NOT include markdown, extra text, or explanation.
"""
    response = run_ollama_prompt(prompt)
    try:
        return json.loads(response)
    except:
        return {
            "error": "Failed to parse structured query from LLM",
            "raw_response": response
        }
