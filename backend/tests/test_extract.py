import types

from review_engine import _extract_response_text


def test_extract_from_simple_string_last():
    class R:
        last = "simple text"

    assert _extract_response_text(R()) == "simple text"


def test_extract_from_last_object_with_content():
    class Last:
        content = "hello from content"

    class R:
        last = Last()

    assert _extract_response_text(R()) == "hello from content"


def test_extract_from_dict_candidates():
    resp = {"candidates": [{"content": "candidate text"}]}
    assert _extract_response_text(resp) == "candidate text"


def test_extract_from_dict_text_key():
    resp = {"text": "raw text"}
    assert _extract_response_text(resp) == "raw text"


def test_extract_from_output_list():
    resp = {"output": [{"message": {"content": "deep content"}}]}
    assert _extract_response_text(resp) == "deep content"


def test_extract_from_object_with_candidates_attr():
    class C:
        def __init__(self):
            self.candidates = [types.SimpleNamespace(content="ns content")]

    assert _extract_response_text(C()) == "ns content"


def test_fallback_stringification():
    class Weird:
        def __str__(self):
            return "weird string"

    assert _extract_response_text(Weird()) == "weird string"
