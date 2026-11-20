"""ai_workbench.config - load settings fro the environment, safely."""
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Reads the .env file if present and copies its entires into os.environ.
# Existing real environment variables always win, so production can override. 
load_dotenv

@dataclass(frozen=True)
class Settings:
    """Everything the workbench needs to know about its model server."""
    
    base_url: str
    api_key: str
    model: str

def get_settings() -> Settings:
    """Build settings from the environment, with local-first defaults."""
    return Settings(
        base_url=os.environ.get("OPENAI_BASE_URL", "http://localhost:1234/v1"),
        api_key=os.environ.get("OPENAI_API_KEY", "default .get value for unnecessary key"),
        model=os.environ.get("LOCAL_MODEL", "smallthinker-4ba0.6b-instruct"),
    )

if __name__ == "__main__":
    s = get_settings()
    print(f"Server: {s.base_url}")
    print(f"Model: {s.model}")
    print(f"API key: {'set' if s.api_key else 'MISSING'} ")