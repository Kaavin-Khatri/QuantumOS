import asyncio
import os
import json
from groq import AsyncGroq

AGENTS = [
    {"name": "The Pragmatist",  "model": "llama-3.3-70b-versatile",               "persona": "Ship the simplest working solution. No over-engineering. Minimal imports."},
    {"name": "The Architect",   "model": "qwen/qwen3-32b",            "persona": "Build for scale. Clean abstractions, separation of concerns, production patterns."},
    {"name": "The Speed Demon", "model": "openai/gpt-oss-120b",                "persona": "Fewest lines possible. Brute force if needed. Just make it work fast."},
    {"name": "The Purist",      "model": "meta-llama/llama-4-scout-17b-16e-instruct",                  "persona": "Follow best practices strictly. PEP8, type hints, docstrings, no shortcuts."},
    {"name": "The Veteran",     "model": "llama-3.3-70b-versatile",       "persona": "Write it like a senior engineer at a top company. Defensive code, edge cases covered."},
    {"name": "The Reasoner",    "model": "qwen/qwen3-32b", "persona": "Reason about the problem step by step before writing any code. Then implement."},
]

async def run_single(client, task, plan, agent):
    prompt = f"""Persona: {agent['persona']}
Task: {task}
Execution Plan: {json.dumps(plan, indent=2)}
Return ONLY valid JSON. No markdown fences. No explanation outside JSON.
{{"agent": "{agent['name']}", "model": "{agent['model']}", "files": [{{"path": "...", "content": "..."}}], "rationale": "...", "tradeoffs": "..."}}"""
    try:
        resp = await client.chat.completions.create(
            model=agent["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4000,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        raw = resp.choices[0].message.content.strip()
        parsed = json.loads(raw, strict=False)
        parsed["agent"] = agent["name"]
        parsed["model"] = agent["model"]
        return parsed
    except Exception as e:
        return {"agent": agent["name"], "model": agent["model"], "files": [], "rationale": str(e), "tradeoffs": "parse error", "error": True}

async def run_battle(task: str, plan: dict) -> list:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    results = await asyncio.gather(*[run_single(client, task, plan, agent) for agent in AGENTS])
    return list(results)
