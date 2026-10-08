import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_DIR = os.path.join(BASE_DIR, "workspace")

def get_workspace_path(relative_path: str) -> str:
    """Resolves a relative file path safely inside the workspace directory."""
    return os.path.normpath(os.path.join(WORKSPACE_DIR, relative_path))

def normalize_filepath(filepath: str) -> str:
    """Ensures test files are explicitly routed to the tests/ directory."""
    if "test" in filepath.lower() and not filepath.startswith("tests/"):
        return f"tests/{filepath}"
    return filepath

def write_workspace_file(relative_path: str, content: str) -> str:
    """Writes generated code content directly into the workspace folder."""
    target_path = get_workspace_path(relative_path)
    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {relative_path} in workspace."
    except Exception as e:
        return f"Error writing file {relative_path}: {str(e)}"

def run_workspace_command(command: str) -> dict:
    """Executes a terminal command inside the workspace directory as CWD."""
    os.makedirs(WORKSPACE_DIR, exist_ok=True)
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,  # Ensures commands run inside workspace/
            capture_output=True,
            text=True,
            timeout=30
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

if __name__ == "__main__":
    # Test writing a file
    print(write_workspace_file("output_test/hello.txt", "Hello from tools.py!"))
    
    # Test executing a command
    res = run_workspace_command("python --version")
    print(f"Command success: {res['success']}, Output: {res['stdout']}")