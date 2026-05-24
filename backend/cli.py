"""Simple CLI for running the code review engine.

Usage examples:

python backend/cli.py --file path/to/source.py
python backend/cli.py --use-mock
"""
import argparse
import json
import sys
from pathlib import Path

from review_engine import review_code, ReviewEngineError


def main(argv=None):
    p = argparse.ArgumentParser(description="Run code review on a source file or stdin.")
    p.add_argument("--file", "-f", help="Path to source file. Reads stdin if omitted.")
    p.add_argument("--use-mock", action="store_true", help="Use local mock review mode.")

    args = p.parse_args(argv)

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            raise SystemExit(2)
        source = path.read_text(encoding="utf-8")
    else:
        source = sys.stdin.read()

    try:
        review = review_code(source, use_mock=args.use_mock)
        print(json.dumps(review, indent=2))
    except ReviewEngineError as exc:
        print(f"Review failed: {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
