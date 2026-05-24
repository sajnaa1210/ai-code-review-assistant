"""Formatter and parser utilities for the code review response."""
import json
import re
from typing import Any, Dict, List


class ReviewFormatError(Exception):
    """Raised when the Gemini response cannot be parsed into valid review JSON."""


def _strip_code_blocks(text: str) -> str:
    """Remove markdown fences or surrounding code block markers."""
    text = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE)
    return text.strip()


def _find_outer_json(text: str) -> str:
    """Extract the outermost JSON object from a string."""
    text = _strip_code_blocks(text)
    start = text.find("{")
    if start == -1:
        raise ReviewFormatError("Could not find a JSON object in the AI response.")

    depth = 0
    for index, char in enumerate(text[start:], start=start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]

    raise ReviewFormatError("Incomplete JSON object found in AI response.")


def _parse_json(text: str) -> Any:
    """Parse text into JSON after extracting the most likely JSON payload."""
    json_text = _find_outer_json(text)
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ReviewFormatError(f"Failed to decode JSON: {exc}") from exc


def _normalize_issue(issue: Dict[str, Any]) -> Dict[str, str]:
    """Normalize issue fields and ensure string values."""
    required_fields = [
        "issue_type",
        "severity",
        "line_reference",
        "explanation",
        "suggested_fix",
    ]
    normalized = {}
    for field in required_fields:
        value = issue.get(field, "") if isinstance(issue, dict) else ""
        normalized[field] = str(value).strip() if value is not None else ""
    return normalized


def _validate_structure(payload: Any) -> Dict[str, Any]:
    """Validate the response structure and normalize values."""
    if not isinstance(payload, dict):
        raise ReviewFormatError("Response JSON is not an object.")

    for key in ("score", "summary", "issues"):
        if key not in payload:
            raise ReviewFormatError(f"Missing required field: {key}")

    score = payload["score"]
    try:
        score_value = int(score)
    except (TypeError, ValueError):
        raise ReviewFormatError("Score must be an integer.") from None

    if score_value < 0 or score_value > 100:
        raise ReviewFormatError("Score must be between 0 and 100.")

    summary = str(payload["summary"]).strip()
    issues_raw = payload["issues"]
    if not isinstance(issues_raw, list):
        raise ReviewFormatError("Issues must be a list.")

    issues = []
    for item in issues_raw:
        if not isinstance(item, dict):
            continue
        issues.append(_normalize_issue(item))

    return {
        "score": score_value,
        "summary": summary,
        "issues": issues,
    }


def format_review_response(raw_text: str) -> Dict[str, Any]:
    """Convert raw Gemini output into a validated review JSON object."""
    parsed = _parse_json(raw_text)
    return _validate_structure(parsed)
