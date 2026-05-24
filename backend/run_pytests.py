import runpy
import sys
from pathlib import Path

# Simple test runner: import all files in tests/ and run functions starting with 'test_'

def run_tests():
    tests_dir = Path(__file__).with_name("tests")
    if not tests_dir.exists():
        print("No tests directory found.")
        return 1

    failed = 0
    for py in sorted(tests_dir.glob("test_*.py")):
        ns = {}
        try:
            code = py.read_text(encoding="utf-8")
            exec(compile(code, str(py), 'exec'), ns)
            for name, obj in list(ns.items()):
                if name.startswith("test_") and callable(obj):
                    try:
                        obj()
                        print(f"{py.name}::{name} - OK")
                    except AssertionError as e:
                        failed += 1
                        print(f"{py.name}::{name} - FAIL: {e}")
                    except Exception as e:
                        failed += 1
                        print(f"{py.name}::{name} - ERROR: {e}")
        except Exception as e:
            failed += 1
            print(f"Failed to import {py}: {e}")

    if failed:
        print(f"{failed} tests failed")
        return 1
    print("All tests passed")
    return 0


if __name__ == '__main__':
    raise SystemExit(run_tests())
