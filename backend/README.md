# AI-Powered Code Review Backend

## Overview

This backend module accepts source code, sends it to the Gemini API, and returns structured JSON containing:
- bugs
- security issues
- performance problems
- code smells
- maintainability issues
- fix suggestions
- overall code quality score

## Files

- `review_engine.py` - main backend logic and `review_code(code: str)` entry point
- `prompts.py` - prompt template for Gemini
- `formatter.py` - response cleanup and validation
- `.env` - local environment variables
- `requirements.txt` - dependencies

## Setup

1. Install dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

2. Add your Gemini API key to `backend/.env`:

```text
GENAI_API_KEY=your_gemini_api_key_here
```

## Run locally

From the workspace root:

```bash
python backend/review_engine.py
```

The sample code in `review_engine.py` will run and print the structured review JSON.

## Local mock mode

If you don't have a Gemini API key or want to run the project offline, the
script will automatically fall back to a local mock review mode when
`GENAI_API_KEY` is not set. This produces a small deterministic review
payload useful for development and tests.

Run the script the same way:

```bash
python backend/review_engine.py
```

CLI usage
---------

You can also run the reviewer from the command line using the lightweight
CLI wrapper. Use `--use-mock` to force local mock mode even if a key is present.

```bash
python backend/cli.py --file path/to/source.py --use-mock
# or read from stdin
cat path/to/source.py | python backend/cli.py --use-mock
```

## Sample usage

```python
from backend.review_engine import review_code

source_code = '''
for i in range(10):
    print(i)
'''

review = review_code(source_code)
print(review)
```

## Frontend integration

A frontend can integrate with this backend in two ways:

- import the review function when the backend is part of the same repository:

```python
from backend.review_engine import review_code

review = review_code(source_code, use_mock=True)
```

- call the CLI from a frontend build or deployment pipeline:

```bash
python backend/cli.py --file path/to/source.py --use-mock
```

If you want to expose this backend via an API, wrap `review_code` in a lightweight web service.

## REST API wrapper

A simple Flask server is available at `backend/server.py`.

Start it from the workspace root:

```bash
python backend/server.py
```

Then POST JSON to `/review`:

```bash
curl -X POST http://localhost:8000/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def f():\n    return 1", "use_mock": true}'
```

The server also exposes a health endpoint:

```bash
curl http://localhost:8000/health
```

## Test snippet

A simple test example can be built around the `review_code` function:

```python
from backend.review_engine import review_code

source_code = 'def add(a, b):\n    return a + b\n'

try:
    result = review_code(source_code)
    assert isinstance(result['score'], int)
    assert 'issues' in result
    print('Test passed')
except Exception as exc:
    print('Test failed:', exc)
```

> Note: The Gemini API call requires a valid API key and network access.
