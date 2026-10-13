# platform_core/config.py
from local_cluster_sdk import AIClusterClient

# Initialize the Local Cluster SDK client
client = AIClusterClient(host="192.168.100.23", port=11434)

# Model names as configured on local server
MANAGER_MODEL_NAME = "orchestrator"
CODING_MODEL_NAME = "coder"