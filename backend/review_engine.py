import os
import json
import re
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

BACKEND_DIR = Path(__file__).resolve().parent

primary_env = BACKEND_DIR / ".env"
if primary_env.exists():
    load_dotenv(primary_env, override=True)
else:
    fallback_env = BACKEND_DIR / ".env.txt"
    if fallback_env.exists():
        load_dotenv(fallback_env, override=True)

load_dotenv(override=True)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class ReviewEngineError(Exception):
    pass


def _extract_json(text: str) -> Dict[str, Any]:
    """Extract JSON from text, handling markdown code blocks."""
    text = text.strip()

    # Remove markdown code block markers
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text.strip(), flags=re.IGNORECASE)
        text = re.sub(r"```$", "", text.strip())

    # Try direct JSON parsing
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to extract JSON object from text
    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ReviewEngineError("Gemini did not return valid JSON.")

    return json.loads(match.group(0))


def review_code(code: str) -> Dict[str, Any]:
    """Review code using Google Gemini AI."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    
    if not api_key:
        raise ReviewEngineError("Missing GEMINI_API_KEY in environment variables.")

    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""You are a professional AI code reviewer.

Analyze the following code and return ONLY valid JSON with no additional text.

Return the response in this exact format:

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
    }},
    {{
      "type": "Performance",
      "severity": "Medium",
      "title": "Inefficient loop",
      "explanation": "Why this is an issue",
      "fix": "How to fix it"
    }}
  ]
}}

Code to review:
```
{code}
```

Return ONLY the JSON, nothing else."""

    try:
        response = model.generate_content(prompt)
        raw_text = response.text
        return _extract_json(raw_text)
    except Exception as e:
        raise ReviewEngineError(f"Error calling Gemini API: {str(e)}")