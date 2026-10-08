# Configuration for local AI API endpoints

# Replace with the actual IP address/port of your local AI server
API_BASE_URL = "http://192.168.100.23:11434"

# Define endpoints or model identifiers
MANAGER_MODEL_ENDPOINT = f"{API_BASE_URL}/v1/chat/completions"
CODING_MODEL_ENDPOINT = f"{API_BASE_URL}/v1/chat/completions"

# Model names as configured on your local server
MANAGER_MODEL_NAME = "orchestrator"
CODING_MODEL_NAME = "coder"