import os
import subprocess

def write_file(filepath: str, content: str) -> str:
    """Writes code content to a specific file on disk."""
    try:
        # Create directory path if it does not exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {filepath}"
    except Exception as e:
        return f"Error writing file {filepath}: {str(e)}"

def run_command(command: str) -> dict:
    """Executes a terminal command and captures stdout/stderr."""
    try:
        result = subprocess.run(
            command,
            shell=True,
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
    print(write_file("output_test/hello.txt", "Hello from tools.py!"))
    
    # Test executing a command
    res = run_command("python --version")
    print(f"Command success: {res['success']}, Output: {res['stdout']}")