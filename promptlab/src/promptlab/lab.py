"""Run 1 prompt across many parameter combinations"""

import itertools
import time
from dataclasses import asdict, dataclass

from openai import OpenAI

from ai_workbench.config import get_settings

@dataclass
class Experiment:
    """One recorded run: what we asked, with which dials, what came back."""
    
    prompt: str
    system: str
    model: str
    temperature: float
    top_p: float
    output: str
    prompt_tokens: int
    completion_tokens: int
    seconds: float
    
def run_once(client: OpenAI, prompt: str, 
             system: str, model: str, 
             temperature: float, top_p: float,
             max_tokens: int = 200) -> Experiment:
    """Execute a single experiment and measure it."""
    start = time.perf_counter()
    r = client.chat.completions.create(
        model=model, 
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens, 
    )
    elapsed = time.perf_counter() - start
    return Experiment(
        prompt=prompt, system=system, model=model,  
        temperature=temperature, top_p=top_p,
        output=r.choices[0].message.content or "",
        prompt_tokens=r.usage.prompt_tokens,
        completion_tokens=r.usage.completion_tokens,
        seconds=round(elapsed, 2),
    )
    
def sweep(client: OpenAI, prompt:str, system:str, model: str,
          temperatures: list[float], top_ps: list[float]
          ) -> list[Experiment]:
    """Run the full grid: every temperature x every top_p."""
    results = []
    for temp, top_p in itertools.product(temperatures, top_ps):
        results.append(run_once(client, prompt, system, model, temp, top_p))
    return results

def experiment_to_dict(exp: Experiment) -> dict:
    return asdict(exp)

if __name__ == "__main__":
    settings = get_settings()
    client = OpenAI(base_url=settings.base_url, api_key=settings.api_key)
    for exp in sweep(
        client, 
        prompt="Explain AI text tokens (used by Large Language Models) to a barista using a coffee analogy, in 2 sentences.",
        system="You are a patient teacher.",
        model=settings.model,
        temperatures=[0.0,0.8],
        top_ps=[0.9],
    ):
        print(f"[temp={exp.temperature}] ({exp.completion_tokens} tok, {exp.seconds}s)")
        print(exp.output, "\n")

    