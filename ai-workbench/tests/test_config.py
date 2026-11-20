"""tests/test_Config.py - prove the config layer behaves."""

import os

from ai_workbench.config import get_settings

def test_defaults_are_local_first(monkeypatch):
    """With no env vars set, we default to LM Studio on localhost."""
    for var in ("OPENAI_BASE_URL", "OPENAI_API_KEY", "LOCAL_MODEL"):
        monkeypatch.delenv(var, raising=False)
    s = get_settings()
    assert s.base_url == "http://localhost:1234/v1"
    assert s.model == "meta-llama-3.1-8b-instruct"
    
def test_env_overrides_defaults(monkeypatch):
    """A real environment variable must beat the built-in default"""
    monkeypatch.setenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
    assert get_settings().base_url == "http://localhost:11434/v1"