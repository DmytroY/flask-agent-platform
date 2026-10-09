# Flask Agent Platform

A lightweight Python project that uses a local multi-agent workflow to generate a Flask application from a natural-language description. The system splits the work between a manager agent and a coding agent, writes generated files into a `workspace/` directory, and runs unit tests against the generated app.

## Features

- Natural-language request to Flask app generation
- Manager agent creates a task plan
- Coder agent generates `requirements.txt`, `app.py`, and tests
- Generated app is written to `workspace/`
- Unit test execution and feedback loop for iteration
- Local LLM integration via HTTP API endpoints

## Project Structure

```text
.
├── main.py                 # CLI entry point
├── platform_core/
│   ├── agents.py           # Multi-agent orchestration
│   ├── config.py           # Local AI API configuration
│   ├── llm_client.py       # LLM request helper
│   ├── parser.py           # JSON/markdown parsing utilities
│   ├── tester.py           # Test runner wrapper
│   └── tools.py            # Workspace file management and command execution
├── workspace/
│   ├── app.py              # Generated Flask app
│   ├── requirements.txt    # Generated dependencies
│   └── tests/
│       └── test_app.py     # Generated tests
├── .gitignore
└── README.md
```

## How it Works

1. Run the CLI from the repo root.
2. Provide a prompt describing the Flask app you want.
3. The manager model plans the tasks.
4. The coding model generates the application and test files.
5. Files are written under `workspace/`.
6. The app is tested with `unittest`.
7. If tests fail, the code is regenerated with the error output as feedback.

## Requirements

- Python 3.9+
- Flask
- Access to a local LLM API compatible with OpenAI-style chat completions

## Configuration

Before running the app, configure your local LLM endpoints in `platform_core/config.py`.

```python
API_BASE_URL = "http://192.168.100.23:11434"
MANAGER_MODEL_ENDPOINT = f"{API_BASE_URL}/v1/chat/completions"
CODING_MODEL_ENDPOINT = f"{API_BASE_URL}/v1/chat/completions"
MANAGER_MODEL_NAME = "orchestrator"
CODING_MODEL_NAME = "coder"
```

Update the URL and model names to match your local AI server.

## Installation

Clone the repository:

```bash
git clone https://github.com/DmytroY/flask-agent-platform.git
cd flask-agent-platform
```

Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r workspace/requirements.txt
```

## Usage

Run the CLI:

```bash
python main.py "Create a Flask app with health and version endpoints"
```

Or run interactively:

```bash
python main.py
```

The system will generate files in `workspace/` and run tests automatically.

## Example Generated App

The generated app from the workspace follows a simple structure similar to:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/version', methods=['GET'])
def version():
    return jsonify({"version": "1.0.0"})
```

## Testing

Tests are executed inside the `workspace/` directory. For example:

```bash
cd workspace
python -m unittest tests/test_app.py
```

## Notes

This project is intended as a local experimentation platform for agent-driven app generation. It is intentionally simple and easy to extend for more complex Flask APIs or additional validation flows.

## License

This project does not currently specify a license.

## Contributing

Contributions are welcome. If you want to improve the orchestration, generator prompts, testing flow, or app generation quality, feel free to open a pull request.
