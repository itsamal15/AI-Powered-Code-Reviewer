# # tests/test_llm_integration.py
# """Tests for LLM integration with mocking."""

# import pytest
# from ai_powered.core.docstring_engine import llm_integration


# def test_llm_returns_dict(monkeypatch):
#     """Test that LLM integration returns structured dict."""
#     def fake_llm(fn):
#         return {
#             "summary": "Generated description",
#             "args": {a["name"]: "Description" for a in fn.get("args", [])},
#             "returns": "Result description",
#             "raises": {}
#         }
    
#     monkeypatch.setattr(
#         llm_integration,
#         "generate_docstring_content",
#         fake_llm
#     )
    
#     fn = {"name": "test_fn", "args": [{"name": "x"}], "returns": "int"}
#     result = llm_integration.generate_docstring_content(fn)
    
#     assert isinstance(result, dict)
#     assert "summary" in result
#     assert "args" in result
#     assert "returns" in result
    
#     # ✅ Validate content quality
#     assert len(result["summary"]) > 0, "Summary should not be empty"
#     assert isinstance(result["args"], dict), "Args should be a dict"
#     assert "x" in result["args"], "Should document the function argument"


# def test_llm_returns_all_required_fields(monkeypatch):
#     """Test that LLM response contains all required fields."""
#     def fake_llm(fn):
#         return {
#             "summary": "Test summary",
#             "args": {"param1": "First parameter"},
#             "returns": "Return value description",
#             "raises": {"ValueError": "When input is invalid"}
#         }
    
#     monkeypatch.setattr(
#         llm_integration,
#         "generate_docstring_content",
#         fake_llm
#     )
    
#     fn = {"name": "test_fn", "args": [{"name": "param1"}], "returns": "str"}
#     result = llm_integration.generate_docstring_content(fn)
    
#     # ✅ Verify all expected keys exist
#     required_keys = ["summary", "args", "returns", "raises"]
#     for key in required_keys:
#         assert key in result, f"Missing required key: {key}"
    
#     # ✅ Verify types
#     assert isinstance(result["summary"], str)
#     assert isinstance(result["args"], dict)
#     assert isinstance(result["returns"], str)
#     assert isinstance(result["raises"], dict)


# def test_llm_fallback_on_error():
#     """Test that LLM handles errors gracefully (or raises appropriately)."""
#     fn = {"name": "test", "args": [{"name": "x"}], "returns": "int"}
    
#     # ✅ OPTION 1: If your LLM has try-catch fallback, test that
#     # This test checks if the implementation handles errors internally
#     try:
#         result = llm_integration.generate_docstring_content(fn)
#         # If we get here, there's a fallback mechanism
#         assert isinstance(result, dict), "Fallback should return dict"
#         assert "summary" in result, "Fallback should have summary"
#     except Exception as e:
#         # ✅ OPTION 2: If LLM is supposed to raise errors, that's valid too
#         # In this case, we just verify it raises a meaningful error
#         assert len(str(e)) > 0, "Error should have a message"
#         # This is acceptable behavior - the test documents that errors propagate


# def test_llm_handles_function_without_args(monkeypatch):
#     """Test LLM integration with function that has no arguments."""
#     def fake_llm(fn):
#         return {
#             "summary": "Simple function with no arguments",
#             "args": {},
#             "returns": "A result",
#             "raises": {}
#         }
    
#     monkeypatch.setattr(
#         llm_integration,
#         "generate_docstring_content",
#         fake_llm
#     )
    
#     fn = {"name": "simple_fn", "args": [], "returns": "str"}
#     result = llm_integration.generate_docstring_content(fn)
    
#     # ✅ Should handle empty args gracefully
#     assert isinstance(result, dict)
#     assert result["args"] == {} or len(result["args"]) == 0
#     assert len(result["summary"]) > 0


# def test_llm_handles_function_without_return(monkeypatch):
#     """Test LLM integration with function that returns None."""
#     def fake_llm(fn):
#         return {
#             "summary": "Function with no return value",
#             "args": {"x": "Input parameter"},
#             "returns": "None",
#             "raises": {}
#         }
    
#     monkeypatch.setattr(
#         llm_integration,
#         "generate_docstring_content",
#         fake_llm
#     )
    
#     fn = {"name": "void_fn", "args": [{"name": "x"}], "returns": None}
#     result = llm_integration.generate_docstring_content(fn)
    
#     # ✅ Should handle None return type
#     assert isinstance(result, dict)
#     assert "returns" in result
#     # Returns field should indicate no return value
#     assert result["returns"] is not None or result["returns"] == "None"

# tests/test_llm_integration.py
"""Tests for LLM integration (mocked)."""

import json
import pytest
from ai_powered.core.docstring_engine import llm_integration


class FakeResponse:
    """Mimics LangChain response object."""
    def __init__(self, content):
        self.content = content


def test_llm_returns_structured_dict(monkeypatch):
    """LLM valid JSON → structured dict."""

    def fake_invoke(self, messages):
        return FakeResponse(json.dumps({
            "summary": "Add two numbers",
            "args": {"x": "First number"},
            "returns": "Sum of inputs",
            "raises": {}
        }))

    monkeypatch.setattr(
        llm_integration.ChatGroq,
        "invoke",
        fake_invoke
    )

    fn = {"name": "add", "args": [{"name": "x"}], "returns": "int"}

    result = llm_integration.generate_docstring_content(fn)

    assert isinstance(result, dict)
    assert result["summary"]
    assert "x" in result["args"]
    assert isinstance(result["returns"], str)
    assert isinstance(result["raises"], dict)


def test_llm_fills_missing_args(monkeypatch):
    """Missing args in LLM response → auto-filled."""

    def fake_invoke(self, messages):
        return FakeResponse(json.dumps({
            "summary": "Process value",
            "args": {},
            "returns": "Processed result",
            "raises": {}
        }))

    monkeypatch.setattr(
        llm_integration.ChatGroq,
        "invoke",
        fake_invoke
    )

    fn = {
        "name": "process",
        "args": [{"name": "value"}],
        "returns": "int"
    }

    result = llm_integration.generate_docstring_content(fn)

    assert "value" in result["args"]
    assert result["args"]["value"] == "DESCRIPTION"


def test_llm_fallback_on_invalid_json(monkeypatch):
    """Invalid JSON → safe fallback."""

    def fake_invoke(self, messages):
        return FakeResponse("THIS IS NOT JSON")

    monkeypatch.setattr(
        llm_integration.ChatGroq,
        "invoke",
        fake_invoke
    )

    fn = {
        "name": "broken",
        "args": [{"name": "x"}],
        "returns": "int"
    }

    result = llm_integration.generate_docstring_content(fn)

    assert isinstance(result, dict)
    assert result["summary"].startswith("Describe the purpose")
    assert "x" in result["args"]


def test_llm_handles_no_args(monkeypatch):
    """Function without arguments."""

    def fake_invoke(self, messages):
        return FakeResponse(json.dumps({
            "summary": "Do something",
            "args": {},
            "returns": "Result",
            "raises": {}
        }))

    monkeypatch.setattr(
        llm_integration.ChatGroq,
        "invoke",
        fake_invoke
    )

    fn = {"name": "noop", "args": [], "returns": None}

    result = llm_integration.generate_docstring_content(fn)

    assert isinstance(result, dict)
    assert result["args"] == {}


def test_llm_requires_api_key(monkeypatch):
    """Missing GROQ_API_KEY → RuntimeError."""

    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    fn = {"name": "test", "args": [], "returns": None}

    with pytest.raises(RuntimeError):
        llm_integration.generate_docstring_content(fn)

