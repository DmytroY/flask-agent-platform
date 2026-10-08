# platform_core/agents.py
from llm_client import query_manager, query_coder
from tools import write_workspace_file, normalize_filepath
from parser import parse_json_plan, extract_code
from tester import execute_unit_tests

def generate_app_code(description: str, user_request: str, feedback: str = "") -> str:
    """Generates app.py using app-specific system instructions."""
    extra_context = f"\nPREVIOUS TEST FAILURE LOGS:\n{feedback}\nFix all issues listed above." if feedback else ""

    coder_prompt = f"""
    Requirement: "{user_request}"
    Task: {description}
    {extra_context}

    CRITICAL INSTRUCTIONS FOR APP.PY:
    - You are writing the Flask application (app.py).
    - Import Flask (`from flask import Flask, jsonify`).
    - Define `app = Flask(__name__)`.
    - Implement ALL requested API endpoints/routes.
    - Output ONLY valid executable Python code in markdown blocks.
    """
    code_output = query_coder(coder_prompt)
    cleaned_code = extract_code(code_output)
    write_workspace_file("app.py", cleaned_code)
    return cleaned_code

def generate_test_code(filepath: str, description: str, user_request: str) -> str:
    """Generates unittest files with strict template constraints."""
    coder_prompt = f"""
    Requirement to test: "{user_request}"
    Target File: {filepath}

    CRITICAL INSTRUCTIONS FOR UNIT TESTS:
    - You are writing Python unit tests using `unittest`.
    - DO NOT create a Flask app instance here.
    - MUST import the app from workspace: `from app import app`
    - MUST inherit from `unittest.TestCase`.
    - MUST use `self.client = app.test_client()` inside `setUp(self)`.
    - Write test methods (starting with `test_`) checking HTTP status codes and JSON payloads.
    
    TEMPLATE TO FOLLOW STRICTLY:
    ```python
    import unittest
    from app import app

    class AppTestCase(unittest.TestCase):
        def setUp(self):
            self.client = app.test_client()
            self.client.testing = True

        def test_endpoints(self):
            # Write tests here
            pass

    if __name__ == '__main__':
        unittest.main()
    ```

    Output ONLY the completed unittest Python code in markdown blocks.
    """
    code_output = query_coder(coder_prompt)
    cleaned_code = extract_code(code_output)
    write_workspace_file(filepath, cleaned_code)
    return cleaned_code

def build_flask_app(user_request: str, max_retries: int = 3):
    print("--- Step 1: Manager Agent Planning ---")
    planner_prompt = f"""
    The user wants a Flask app with this requirement: "{user_request}".
    
    Break this down into 3 specific file creation tasks:
    1. requirements.txt
    2. app.py (the Flask application with the required endpoints)
    3. tests/test_app.py (a Python unittest file using Flask's test_client to verify endpoints)

    Respond with ONLY a JSON list of tasks.
    Example format:
    [
      {{"file": "requirements.txt", "description": "Add flask dependency"}},
      {{"file": "app.py", "description": "Create main Flask app with endpoints"}},
      {{"file": "tests/test_app.py", "description": "Unit test using unittest and Flask test_client"}}
    ]
    """
    
    plan_raw = query_manager(planner_prompt)
    try:
        tasks = parse_json_plan(plan_raw)
    except ValueError as err:
        print(err)
        return

    print("\n--- Step 2: Code Generation ---")
    for task in tasks:
        filepath = normalize_filepath(task["file"])
        description = task["description"]
        print(f"Generating workspace/{filepath}...")
        
        if filepath == "app.py":
            generate_app_code(description, user_request)
        elif "test" in filepath:
            generate_test_code(filepath, description, user_request)
        else:
            # Handle requirements.txt or other static files
            code = query_coder(f"Task: {description}\nTarget File: {filepath}\nOutput ONLY raw file content.")
            write_workspace_file(filepath, extract_code(code))

    print("\n--- Step 3: Test-Driven Feedback Loop ---")
    for attempt in range(1, max_retries + 1):
        print(f"Running tests in workspace (Attempt {attempt}/{max_retries})...")
        test_res = execute_unit_tests("tests/test_app.py")
        
        if test_res["passed"]:
            print("\n🎉 ALL UNIT TESTS PASSED!")
            print(test_res["logs"])
            return
        
        print(f"\n❌ Test Failure Output:\n{test_res['logs']}")
        if attempt < max_retries:
            print("Sending test error back to Coder Model to rewrite app.py...")
            generate_app_code(
                description="Fix app.py so all unit tests pass.",
                user_request=user_request,
                feedback=test_res["logs"]
            )

    print(f"\nFailed to pass tests after {max_retries} attempts.")

if __name__ == "__main__":
    prompt = "Create a basic Flask app with a GET /health endpoint returning JSON {'status': 'ok'}."
    build_flask_app(prompt)