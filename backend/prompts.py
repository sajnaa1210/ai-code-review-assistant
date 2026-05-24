"""Prompt utilities for the AI code review backend."""

CODE_REVIEW_PROMPT_TEMPLATE = """
You are an expert software engineer and security-conscious code reviewer.
Analyze the provided source code and return ONLY valid JSON following this schema:
{
  "score": 0,
  "summary": "",
  "issues": [
    {
      "issue_type": "",
      "severity": "",
      "line_reference": "",
      "explanation": "",
      "suggested_fix": ""
    }
  ]
}

Your analysis must include:
- bugs
- security vulnerabilities
- code smells
- performance issues
- maintainability issues
- bad coding practices

Use severity values like: low, medium, high, critical.
For line references, use human-friendly text such as "line 8" or "lines 10-14".
Do not return markdown, code fences, or any text outside the JSON object.
Do not add additional keys beyond the schema above.

Source code:
"""  # noqa: E501


def build_review_prompt(source_code: str) -> str:
    """Build the Gemini prompt used to request a code review."""
    return CODE_REVIEW_PROMPT_TEMPLATE + source_code.strip() + "\n"
