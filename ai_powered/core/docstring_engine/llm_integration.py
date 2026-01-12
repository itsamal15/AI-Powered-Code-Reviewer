"""
LLM integration for docstring content generation.

Responsibilities:
- Generate semantic docstring content ONLY
- Return structured JSON
- Never format docstrings
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

#load_dotenv()
from pathlib import Path

def load_env():
    """
    Search upwards from this file until a .env file is found.
    Works reliably with Streamlit.
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        env_file = parent / ".env"
        if env_file.exists():
            load_dotenv(dotenv_path=env_file)
            return env_file
    return None


ENV_FILE = load_env()
print("ENV file found at:", ENV_FILE)
print("GROQ_API_KEY loaded:", bool(os.getenv("GROQ_API_KEY")))




# -------------------------
# Internal helpers
# -------------------------

def _safe_fallback(fn: Dict[str, Any]) -> Dict[str, Any]:
    """Return minimal safe content if LLM fails."""
    arg_names = [a["name"] for a in fn.get("args", [])]

    return {
        "summary": f"Describe the purpose of {fn.get('name', 'this function')}.",
        "args": {name: "DESCRIPTION" for name in arg_names},
        "returns": "DESCRIPTION",
        "raises": {}
    }


def _validate_and_fix(payload: dict, fn: dict) -> dict:
    """
    Ensure payload strictly follows schema and PEP 257 rules.
    """
    if not isinstance(payload, dict):
        return _safe_fallback(fn)

    payload.setdefault("summary", "")
    payload.setdefault("args", {})
    payload.setdefault("returns", "")
    payload.setdefault("raises", {})

    if not isinstance(payload["args"], dict):
        payload["args"] = {}

    if not isinstance(payload["raises"], dict):
        payload["raises"] = {}

    # Ensure all function args are present
    for arg in fn.get("args", []):
        payload["args"].setdefault(arg["name"], "DESCRIPTION")


    # Enforce imperative mood safety
    # Enforce imperative mood safety (do NOT break valid summaries)
    summary = payload["summary"].strip()

    INVALID_STARTS = ("adds ", "calculates ", "returns ", "fetches ", "gets ")

    if not summary or summary.lower().startswith(INVALID_STARTS):
        payload["summary"] = f"Describe the purpose of {fn['name']}."


    return payload


# -------------------------
# Public API
# -------------------------

def generate_docstring_content(fn: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate structured docstring content using LLM.

    Returns:
    {
        "summary": str,
        "args": {arg_name: description},
        "returns": str,
        "raises": {ExceptionName: description}
    }
    """

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY not set (env file not found or key missing)")


    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    arg_names = [a["name"] for a in fn.get("args", [])]
    
    raises = fn.get("raises", [])

    prompt = f"""
Return ONLY valid JSON in this exact format:

{{
  "summary": "1–2 line description of what the function does",
  "args": {{
    "arg_name": "description"
  }},
  "returns": "description of the return value",
  "raises": {{
    "ExceptionName": "reason"
  }}
}}

Rules:
- Summary MUST be imperative (Add, Calculate, Fetch, Validate)
- No third-person verbs
- No markdown
- No triple quotes
- Do NOT invent exceptions
- If no exceptions exist, return "raises": {{}}
- JSON must be strictly valid

Function name: {fn["name"]}
Arguments: {arg_names}
Return behavior: infer from function name and arguments
Known raises: {raises}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        payload = json.loads(response.content)
        return _validate_and_fix(payload, fn)

    except Exception:
        return _safe_fallback(fn)
