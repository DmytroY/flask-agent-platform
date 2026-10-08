from platform_core.llm_client import query_manager, query_coder

def test_local_ai_server():
    print("--- Testing Manager Model ---")
    manager_prompt = "Say hello and state your role in 1 sentence."
    manager_response = query_manager(manager_prompt)
    print(f"Manager Response:\n{manager_response}\n")

    print("--- Testing Coding Model ---")
    coder_prompt = "Write a Python function named 'add' that adds two numbers."
    coder_response = query_coder(coder_prompt)
    print(f"Coder Response:\n{coder_response}\n")

if __name__ == "__main__":
    test_local_ai_server()