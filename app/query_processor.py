import subprocess
import json
import re
def parse_query_to_csv(query):
    prompt = f"""Extract the following fields from the text:

- age (number)
- gender (M or F)
- procedure (short)
- city (short)
- policy duration in days (number)

Input: "{query}"

Respond ONLY like this: age,gender,procedure,city,policy_duration_days

Example: 46,M,knee surgery,Pune,90
"""
    res = subprocess.run(["ollama", "run", "llama3", prompt],
                         capture_output=True, text=True)
    return res.stdout.strip()


def parse_query_to_json(query):
    prompt = f"""Extract and return JSON like this:
{{
  "age": 46,
  "gender": "M",
  "procedure": "knee surgery",
  "city": "Pune",
  "policy_duration_days": 90
}}

Input: {query}
Only return JSON.
"""
    res = subprocess.run(["ollama", "run", "llama3", prompt],
                         capture_output=True, text=True)
    output = res.stdout.strip()

    if not output:
        raise ValueError("LLM returned empty response. Is Ollama running?")

    # Extract the first JSON block from the response using regex
    match = re.search(r"{.*}", output, re.DOTALL)
    if not match:
        raise ValueError(f"LLM returned non-JSON output:\n{output}")

    json_str = match.group(0)
    return json.loads(json_str)
