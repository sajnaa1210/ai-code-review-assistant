from review_engine import review_code
from review_engine import ReviewEngineError
import subprocess
import sys
from pathlib import Path


def test_mock_non_empty():
    r = review_code("def f():\n    return 1", use_mock=True)
    assert isinstance(r.get("score"), int), "score must be an int"
    assert isinstance(r.get("issues"), list), "issues must be a list"


def test_mock_empty_raises():
    try:
        review_code("", use_mock=True)
        raise AssertionError("Expected ValueError for empty code")
    except ValueError:
        pass


def test_real_mode_raises_without_sdk_or_key():
    # When not running with mock and SDK/key absent, expect ReviewEngineError
    try:
        review_code("def f():\n    return 1", use_mock=False)
        raise AssertionError("Expected ReviewEngineError when Gemini SDK/key missing")
    except ReviewEngineError:
        pass


def test_cli_mock():
    # Run the CLI in mock mode and ensure it prints JSON
    cli = Path(__file__).with_name("cli.py")
    proc = subprocess.run([sys.executable, str(cli), "--use-mock"], input=b"def f():\n    return 1", capture_output=True)
    assert proc.returncode == 0, f"CLI failed: {proc.stderr.decode() }"
    out = proc.stdout.decode().strip()
    assert out.startswith("{") and "score" in out


if __name__ == "__main__":
    try:
        test_mock_non_empty()
        test_mock_empty_raises()
        print("All tests passed")
    except AssertionError as e:
        print("Test failed:", e)
        raise SystemExit(1)
