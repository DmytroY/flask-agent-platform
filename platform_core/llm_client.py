import requests
from config import MANAGER_MODEL_ENDPOINT, CODING_MODEL_ENDPOINT, MANAGER_MODEL_NAME, CODING_MODEL_NAME

def call_llm(endpoint: str, model_name: str, system_prompt: str, user_prompt: str) -> str:
    """Generic function to send a chat completion request to local AI API."""
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(endpoint, json=payload, timeout=300)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error calling {model_name}: {str(e)}"

def query_manager(user_prompt: str) -> str:
    """Sends prompt to the Manager Model (simple text model)."""
    system_prompt = "You are a software architect manager. Break down app features into logical execution steps."
    return call_llm(MANAGER_MODEL_ENDPOINT, MANAGER_MODEL_NAME, system_prompt, user_prompt)

def query_coder(task_prompt: str) -> str:
    """Sends prompt to the Coding Model."""
    system_prompt = "You are a Python software engineer. Output valid, clean code only without extra explanation."
    return call_llm(CODING_MODEL_ENDPOINT, CODING_MODEL_NAME, system_prompt, task_prompt)