# main.py
import sys
import os

# Ensure platform_core is in Python's module search path
sys.path.append(os.path.join(os.path.dirname(__file__), "platform_core"))

from agents import build_flask_app

def run_cli():
    print("==================================================")
    print("   Local Multi-Agent Flask Platform")
    print("==================================================")
    
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])
    else:
        user_prompt = input("\nDescribe the Flask app you want to build:\n> ")

    if not user_prompt.strip():
        print("Empty prompt provided. Exiting.")
        return

    print(f"\n[Starting Platform Execution for Request: '{user_prompt}']\n")
    build_flask_app(user_prompt)

if __name__ == "__main__":
    run_cli()