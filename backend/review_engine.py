
import os
import json
import re
from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

import google.generativeai as genai

class ReviewEngineError(Exception):
    pass


def _extract_json(text: str) -> Dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text.strip(), flags=re.IGNORECASE)
        text = re.sub(r"```$", "", text.strip())

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ReviewEngineError("Gemini did not return valid JSON.")

    return json.loads(match.group(0))


def review_code(code: str) -> Dict[str, Any]:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ReviewEngineError("Missing GEMINI_API_KEY.")

    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
You are a professional AI code reviewer.

Analyze the code and return ONLY valid JSON.

Format:

{{
  "score": 85,
  "high_count": 1,
  "medium_count": 2,
  "low_count": 1,
  "total_issues": 4,
  "issues": [
    {{
      "type": "Bug",
      "severity": "High",
      "title": "Possible division by zero",
      "explanation": "Why this is an issue",
      "fix": "How to fix it"
    }}
  ]
}}

Code:
{code}
"""

    response = model.generate_content(prompt)

    raw_text = response.text

    return _extract_json(raw_text)
