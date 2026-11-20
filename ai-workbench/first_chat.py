from openai import OpenAI

from ai_workbench.config import get_settings

settings = get_settings()

client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)

response = client.chat.completions.create(
    model=settings.model,
    messages=[
        {"role": "system", 
         "content": "You are a concise security-triage assistant."},
        {"role": "user", 
         "content":"In one sentence: what is prompt injection?"},
    ],
    temperature=0.2, 
    max_tokens=150,
)

print(response.choices[0].message.content)
print("---")
print("finish_reason: ", response.choices[0].finish_reason)
print("usage: ", response.usage)

