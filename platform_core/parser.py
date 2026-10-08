# parser.py
import json
import re

def extract_code(text: str) -> str:
    """Extracts raw code from markdown blocks if present."""
    match = re.search(r"```(?:python|html|txt|json)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def parse_json_plan(plan_text: str) -> list:
    """Cleans markdown formatting and parses the manager's JSON plan."""
    cleaned = extract_code(plan_text)
    try:
        return json.loads(cleaned)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON plan: {str(e)}")