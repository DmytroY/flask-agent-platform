# Flask Agent Platform

This repository contains a small local multi-agent workflow that turns a natural-language request into a Flask application. The project does not ship a full web dashboard or installer; instead, it orchestrates a manager model and a coding model to plan tasks, generate app code and tests, write them into `workspace/`, and validate the result with Python unit tests.

## What this project does

- Accepts a user prompt describing a Flask app
- Uses a manager agent to break the request into file-generation tasks
- Uses a coder agent to generate application code and tests
- Writes generated files under `workspace/`
- Runs `unittest` in the workspace and retries when failures occur
- Connects to a local model cluster through `local_cluster_sdk`

## Current project structure

```text
.
├── main.py                     # CLI entry point
├── requirements.txt            # Project dependency for local-cluster-sdk
├── platform_core/
│   ├── agents.py              # Multi-agent orchestration and task loop
│   ├── config.py              # Local Cluster SDK client configuration
│   ├── llm_client.py          # Manager and coder model wrappers
│   ├── parser.py              # JSON parsing and code extraction utilities
│   ├── test_connection.py     # Quick smoke test for local model connectivity
│   ├── tester.py              # Runs workspace unit tests
│   ├── tools.py               # Safe workspace file writing and command execution
│   └── agents copy.py         # Snapshot/duplicate copy kept in repo
├── workspace/
│   ├── app.py                 # Generated Flask app (created at runtime)
│   ├── requirements.txt       # Generated app dependencies (created at runtime)
│   └── tests/
│       └── test_app.py        # Generated unittest file (created at runtime)
├── .gitignore
├── README.md
└── LICENSE                    # if added externally; not part of the current repo state
```

Note: the generated app files are created at runtime under `workspace/`; they are not checked in as part of the repository source.

## How it works

1. Run `python main.py` or pass a prompt directly as a command-line argument.
2. `main.py` forwards the prompt to `platform_core/agents.py`.
3. The manager model creates a JSON task plan.
4. The coder model writes the Flask app and test files.
5. Files are saved in `workspace/` using `platform_core/tools.py`.
6. `platform_core/tester.py` runs `python -m unittest tests/test_app.py` inside the workspace.
7. If tests fail, the error output is sent back to the coder and the app is regenerated.

## Requirements

- Python 3.9+
- Access to a local model server compatible with the `local_cluster_sdk` client
- The following model resources configured on the local server:
  - `orchestrator`
  - `coder`

## Installation

Clone the repository:

```bash
git clone https://github.com/DmytroY/flask-agent-platform.git
cd flask-agent-platform
```

Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project requirements:

```bash
pip install -r requirements.txt
```

## Local model configuration

The project connects to a local cluster using `local_cluster_sdk` in `platform_core/config.py`:

```python
from local_cluster_sdk import AIClusterClient

client = AIClusterClient(host="192.168.100.23", port=11434)

MANAGER_MODEL_NAME = "orchestrator"
CODING_MODEL_NAME = "coder"
```

If your local cluster uses a different host or port, update the values in `platform_core/config.py` before running the app.

## Usage

Run the app with a direct prompt:

```bash
python main.py "Create a basic Flask app with a GET /health endpoint returning JSON {'status': 'ok'}"
```

Or run it interactively:

```bash
python main.py
```

When prompted, describe the Flask app you want to generate.

## Project behavior details

The actual implementation is built around these files:

- `main.py`: launches the CLI and reads the user prompt
- `platform_core/agents.py`: orchestrates the Manager + Coder flow
- `platform_core/llm_client.py`: sends prompts to the configured local models
- `platform_core/parser.py`: strips markdown fences and parses JSON plans
- `platform_core/tools.py`: writes files and runs shell commands in the workspace
- `platform_core/tester.py`: executes the generated unit tests
- `platform_core/test_connection.py`: checks that the manager and coder models are reachable

## Generated app workflow

The generated code is expected to be placed inside `workspace/`. The project writes code in a flat workspace layout, for example:

```text
workspace/
├── app.py
├── requirements.txt
├── tests/
│   └── test_app.py
```

The code generation flow requires the generated app to import from the workspace package context, and tests are written to use Flask's `test_client()`.

## Example of a generated app

A generated app typically looks like:

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})
```

The generated app dependencies are stored under `workspace/requirements.txt` and usually include Flask, for example:

```txt
Flask==2.0.1
```

## Testing

The test loop executes the generated tests inside the workspace:

```bash
cd workspace
python -m unittest tests/test_app.py
```

The project can also run a connection check before generating anything:

```bash
python platform_core/test_connection.py
```

## Limitations

Like any AI tool, it works best when the task is described in detail and leaves no room for ambiguity. A query like this works well:

```bash
python main.py "Create Flask app. When user first enter to endpoint /hello it should display to user text field "What is your name?"  input field for {name} and button. After user input {name} and press button Flask should display text field "Hello, {name}!""
```

However, a query of this type may produce an unpredictable result:
```bash
python main.py "Let it ask my name and then say hello to me"
```


## Notes

- The root `requirements.txt` installs the SDK used to connect to the local cluster.
- The generated app's dependencies are separate and are written to `workspace/requirements.txt`.
- This project is intentionally lightweight and focused on local experimentation with AI-driven Flask generation.

## License

This repository does not currently declare a license in its source tree.

## Contributing

Contributions are welcome. If you want to improve the orchestration logic, generation prompts, testing flow, or reliability of generated Flask apps, please open a pull request.
