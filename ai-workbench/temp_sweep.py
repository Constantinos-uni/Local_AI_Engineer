"""1 prompt 3 temperatures, 3 personalities"""

from openai import OpenAI

from ai_workbench.config import get_settings

settings = get_settings()

client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)

PROMPT = "Give me a one-line tagline for a coffee shop run by robots."

for temp in (0.0, 0.7, 1.3):
    r = client.chat.completions.create(
        model=settings.model,
        messages=[{"role":"user", "content": PROMPT}],
        temperature=temp,
        max_tokens=40,
        
    )
    print(f"temp={temp}: {r.choices[0].message.content.strip()}")
    