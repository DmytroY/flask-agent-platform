from tools import run_workspace_command

def execute_unit_tests(test_rel_path: str = "tests/test_app.py") -> dict:
    """Runs Python unit tests inside workspace and returns pass/fail status with output logs."""
    res = run_workspace_command(f"python -m unittest {test_rel_path}")
    return {
        "passed": res["success"],
        "logs": res["stderr"] if res["stderr"] else res["stdout"]
    }