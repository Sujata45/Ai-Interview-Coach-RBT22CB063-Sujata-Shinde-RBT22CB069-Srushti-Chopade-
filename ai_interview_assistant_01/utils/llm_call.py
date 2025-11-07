from litellm import completion
import os
import json
from dotenv import load_dotenv

load_dotenv()

LLM_MODEL = os.getenv("LLM_MODEL", "mistral/mistral-large-latest")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

def get_response_from_llm(prompt):
    if not MISTRAL_API_KEY:
        raise ValueError("Missing MISTRAL_API_KEY. Set it in .env")

    try:
        response = completion(
            model=LLM_MODEL,
            api_key=MISTRAL_API_KEY,
            messages=[{"role":"user","content":prompt}],
        )
        content = response.choices[0].message.get("content") or ""
        return content
    except Exception as e:
        print("LLM call error:", e)
        return "{}"

def parse_json_response(response):
    try:
        text = response.strip()
        if text.startswith("```"):
            # remove code fences
            text = text.strip("```json").strip("```").strip()
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except Exception as e:
        print("JSON parse failed:", e)
        return {}
