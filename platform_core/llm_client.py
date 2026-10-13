# platform_core/llm_client.py
from local_cluster_sdk import AgentWorkload
from config import client, MANAGER_MODEL_NAME, CODING_MODEL_NAME

def query_manager(prompt: str, system_prompt: str = "You are an orchestration manager.") -> str:
    workload = AgentWorkload(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.2,
        num_ctx=4096
    )
    return client.execute(workload, resource=MANAGER_MODEL_NAME)

def query_coder(prompt: str, system_prompt: str = "You are a senior Python engineer.") -> str:
    workload = AgentWorkload(
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=0.2,
        num_ctx=4096
    )
    return client.execute(workload, resource=CODING_MODEL_NAME)