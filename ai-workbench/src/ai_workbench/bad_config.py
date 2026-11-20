import os

base_url = os.environ["OPENAI_BASE_URL"]
print(f"Talking to: {base_url}")


"""
Lessons: Got a KeyError value...because env vars were never found. So we need to:
    1. .env file wasnt loaded explicitly using python-dotenv
    2. Use .get() and set a sensible default.
    
Refer to config.py
"""

