"""AI-powered code review backend using Gemini API."""
import json
import os
from typing import Dict

try:
    import google.generativeai as genai
except Exception:
    genai = None
try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(*args, **kwargs):
        return None

from prompts import build_review_prompt
from formatter import ReviewFormatError, format_review_response

# Load environment variables from the local .env file in the backend folder.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

API_KEY_ENV_NAME = "GENAI_API_KEY"
MODEL_NAME = "gemini-1.5-flash"


class ReviewEngineError(Exception):
    """A generic exception for review engine failures."""


def _load_api_key() -> str:
    """Read the Gemini API key from environment variables."""
    api_key = os.getenv(API_KEY_ENV_NAME)
    if not api_key:
        raise ReviewEngineError(
            f"Missing environment variable: {API_KEY_ENV_NAME}."
            " Add your Gemini API key to backend/.env."
        )
    return api_key


def _configure_client(api_key: str) -> None:
    """Configure the Google generative AI client with the API key."""
    if genai is None:
        raise ReviewEngineError(
            "Gemini SDK not available. Install 'google-generativeai' to use real reviews."
        )
    genai.configure(api_key=api_key)


def _extract_response_text(response: object) -> str:
    """Extract the generated text from Gemini raw response object."""
    def _as_str(val):
        try:
            return str(val)
        except Exception:
            return None

    def _extract_from_candidate(cand):
        if cand is None:
            return None
        # dict-like
        if isinstance(cand, dict):
            for key in ("content", "text", "message", "output"):
                if key in cand and cand[key]:
                    val = cand[key]
                    if isinstance(val, (str, bytes)):
                        return _as_str(val)
                    if isinstance(val, dict):
                        return _extract_from_candidate(val)
                    if isinstance(val, (list, tuple)) and val:
                        return _extract_from_candidate(val[0])

        # object with attributes
        for attr in ("content", "text", "message", "output"):
            if hasattr(cand, attr):
                attr_val = getattr(cand, attr)
                if isinstance(attr_val, (str, bytes)):
                    return _as_str(attr_val)
                if isinstance(attr_val, dict) or hasattr(attr_val, "__dict__"):
                    return _extract_from_candidate(attr_val)

        return _as_str(cand)

    # 1) response.last can be a string or object
    if hasattr(response, "last") and response.last:
        extracted = _extract_from_candidate(response.last)
        if extracted:
            return extracted

    # 2) common top-level dict shapes
    if isinstance(response, dict):
        # direct content
        for key in ("content", "text", "output", "message", "result"):
            if key in response and response[key]:
                val = response[key]
                if isinstance(val, (str, bytes)):
                    return _as_str(val)
                try:
                    cand = val[0] if isinstance(val, (list, tuple)) and val else val
                except Exception:
                    cand = val
                extracted = _extract_from_candidate(cand)
                if extracted:
                    return extracted

        # candidates list
        candidates = response.get("candidates") or response.get("generations") or []
        if candidates:
            extracted = _extract_from_candidate(candidates[0])
            if extracted:
                return extracted

    # 3) response may have attribute candidates or output
    if hasattr(response, "candidates"):
        candidates = getattr(response, "candidates") or []
        if candidates:
            extracted = _extract_from_candidate(candidates[0])
            if extracted:
                return extracted

    if hasattr(response, "output"):
        out = getattr(response, "output")
        # output might be dict-like
        try:
            cand = out[0] if isinstance(out, (list, tuple)) and out else out
        except Exception:
            cand = out
        extracted = _extract_from_candidate(cand)
        if extracted:
            return extracted

    # fallback: try stringifying the response
    as_str = _as_str(response)
    if as_str:
        return as_str

    raise ReviewEngineError("Unable to extract the model response text.")


def _call_gemini(prompt: str) -> str:
    """Send the code review prompt to Gemini and return the raw response text."""
    if genai is None:
        raise ReviewEngineError(
            "Gemini SDK not installed. Install 'google-generativeai' or run with use_mock=True."
        )

    api_key = _load_api_key()
    _configure_client(api_key)

    try:
        response = genai.chat.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_output_tokens=1024,
        )
        return _extract_response_text(response)
    except Exception as exc:
        raise ReviewEngineError(f"Gemini API request failed: {exc}") from exc


def _mock_review(code: str) -> Dict[str, object]:
    """Return a deterministic, minimal mock review for local testing."""
    # Simple heuristics for a tiny mock: penalize empty code and flag use of bare indexes
    score = 90 if code.strip() else 0
    summary = "Mock review: basic static checks applied."
    issues = []
    if not code.strip():
        issues.append(
            {
                "issue_type": "empty_input",
                "severity": "high",
                "line_reference": "",
                "explanation": "No source code was provided.",
                "suggested_fix": "Pass a non-empty source string to review_code().",
            }
        )
    if "[" in code and "]" in code and "['value']" in code:
        issues.append(
            {
                "issue_type": "indexing",
                "severity": "medium",
                "line_reference": "unknown",
                "explanation": "Potential unsafe dictionary indexing may raise KeyError.",
                "suggested_fix": "Use .get() with defaults or check keys before access.",
            }
        )

    return {"score": score, "summary": summary, "issues": issues}


def review_code(code: str, use_mock: bool = False) -> Dict[str, object]:
    """Main entry point for reviewing source code.

    Args:
        code: The full source code as a single string.

    Returns:
        A validated JSON-like dictionary with score, summary, and issues.
    """
    if not isinstance(code, str) or not code.strip():
        raise ValueError("code must be a non-empty string.")

    if use_mock:
        return _mock_review(code)

    prompt = build_review_prompt(code)
    raw_response = _call_gemini(prompt)

    try:
        review = format_review_response(raw_response)
    except ReviewFormatError as exc:
        raise ReviewEngineError(
            "The AI response could not be parsed into the expected JSON format."
        ) from exc

    return review


if __name__ == "__main__":
    # Sample usage example while developing locally.
    sample_source_code = """
def add_items(items):
    total = 0
    for item in items:
        total += item['value']
    return total
"""

    # Prefer using a real API key when available; otherwise fall back to mock mode
    if os.getenv(API_KEY_ENV_NAME):
        try:
            result = review_code(sample_source_code)
            print(json.dumps(result, indent=2))
        except Exception as error:
            print(f"Review failed: {error}")
    else:
        print("No Gemini API key found — running in local mock mode.")
        result = review_code(sample_source_code, use_mock=True)
        print(json.dumps(result, indent=2))
