# agents.py
import json
import re
from llm_client import query_manager, query_coder
from tools import write_file, run_command

def extract_code(text: str) -> str:
    """Extracts raw code from markdown code blocks if present."""
    match = re.search(r"```(?:python|html|txt|json)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def generate_file(filepath: str, description: str, extra_instructions: str = "") -> str:
    """Generates code for a specific task using the Coder Model."""
    coder_prompt = f"""
    Task: {description}
    Target File: {filepath}
    {extra_instructions}
    
    Output ONLY valid code inside code blocks. Do not include markdown commentary.
    """
    code_output = query_coder(coder_prompt)
    cleaned_code = extract_code(code_output)
    write_file(filepath, cleaned_code)
    return cleaned_code

def build_flask_app_with_tests(user_request: str, max_retries: int = 3):
    print("--- Step 1: Manager Agent Planning ---")
    planner_prompt = f"""
    The user wants a Flask app with this requirement: "{user_request}".
    
    Break this down into 3 specific file creation tasks:
    1. requirements.txt
    2. app.py (the Flask application with the required endpoints)
    3. test_app.py (a Python unittest file using Flask's test_client to verify endpoints)

    Respond with ONLY a JSON list of tasks.
    Example format:
    [
      {{"file": "requirements.txt", "description": "Add flask dependency"}},
      {{"file": "app.py", "description": "Create main Flask app with /health endpoint"}},
      {{"file": "test_app.py", "description": "Unit test using unittest and Flask test_client to verify GET /health returns 200 and json"}}
    ]
    """
    
    plan_response = query_manager(planner_prompt)
    cleaned_plan = extract_code(plan_response)
    
    try:
        tasks = json.loads(cleaned_plan)
    except Exception as e:
        print(f"Error parsing manager plan JSON: {str(e)}")
        return

    print("\n--- Step 2: Coder Agent Code Generation ---")
    for task in tasks:
        print(f"Generating {task['file']}...")
        extra_inst = ""
        if task["file"] == "app.py":
            extra_inst = "CRITICAL: You MUST import Flask (`from flask import Flask`) and define the requested routes."
        elif task["file"] == "test_app.py":
            extra_inst = "CRITICAL: Use Python's `unittest` framework and `app.test_client()` to make real HTTP requests to app.py."
            
        generate_file(task["file"], task["description"], extra_inst)

    print("\n--- Step 3: Running Real Unit Tests ---")
    feedback = ""
    for attempt in range(1, max_retries + 1):
        print(f"Executing Unit Tests (Attempt {attempt}/{max_retries})...")
        
        # Execute the generated unittest file
        test_res = run_command("python -m unittest test_app.py")
        
        if test_res["success"]:
            print("\n🎉 ALL UNIT TESTS PASSED!")
            print(test_res["stderr"])  # unittest prints test summary to stderr
            return
        else:
            print(f"\n❌ Unit tests failed on attempt {attempt}:")
            print(test_res["stderr"])
            
            if attempt < max_retries:
                feedback = f"Unit test execution failed with this output:\n{test_res['stderr']}\nFix app.py so tests pass."
                print("\nSending error feedback back to Coder Model to fix app.py...")
                generate_file("app.py", "Fix app.py to resolve test failures.", f"FEEDBACK FROM TEST FAILURE:\n{feedback}")

    print(f"\nFailed to pass unit tests after {max_retries} attempts.")

if __name__ == "__main__":
    prompt = "Create a basic Flask app with a GET /health endpoint returning JSON {'status': 'ok'}."
    build_flask_app_with_tests(prompt)