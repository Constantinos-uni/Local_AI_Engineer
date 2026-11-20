import httpx

from ai_workbench.config import get_settings

settings = get_settings()

payload = {
    "model": settings.model,
    "messages": [{"role":"user", "content": "reply with exactly: pong"}],
    "temperature": 0.0,
}

r = httpx.post(
    f"{settings.base_url}/chat/completions",
    json=payload,
    headers={"Authorization": f"Bearer {settings.api_key}"},
    timeout=60.0,
)

r.raise_for_status()
data = r.json()
print(data["choices"][0]["message"]["content"])

