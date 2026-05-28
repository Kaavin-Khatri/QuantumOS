import os
import json
from groq import AsyncGroq

async def judge_battle(plan: dict, implementations: list) -> dict:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    model = os.getenv("GROQ_JUDGE_MODEL", "llama3-70b-8192")
    
    # Exclude failed implementations from being fully judged if we want, but let's pass them all
    impl_summary = []
    for i in implementations:
        if i.get("error"):
            impl_summary.append(f"Agent: {i.get('agent')} - FAILED: {i.get('rationale')}")
        else:
            files_info = [f["path"] for f in i.get("files", [])]
            impl_summary.append(f"Agent: {i.get('agent')}\nFiles: {files_info}\nRationale: {i.get('rationale')}")
            
    prompt = f"""You are a principal engineer and technical judge.
You will receive 6 different implementations of the same coding task.
Score each on 4 dimensions (0-10 each): correctness, maintainability, simplicity, testability.
Pick the winner. Be decisive.
Return ONLY valid JSON. No markdown.

Plan: {json.dumps(plan)}
Implementations Summary:
{chr(10).join(impl_summary)}

Output schema:
{{
  "scores": {{
    "The Pragmatist":  {{ "correctness": 8, "maintainability": 6, "simplicity": 9, "testability": 6, "total": 29 }},
    "The Architect":   {{ "correctness": 8, "maintainability": 9, "simplicity": 7, "testability": 8, "total": 32 }},
    ...
  }},
  "winner": "The Veteran",
  "winner_model": "llama-3.1-70b-versatile",
  "reasoning": "...",
  "runner_up": "The Purist",
  "eliminated": [
    {{ "agent": "The Speed Demon", "reason": "..." }}
  ]
}}
"""
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = resp.choices[0].message.content.strip()
        if raw.startswith("```json"):
            raw = raw[7:-3].strip()
        elif raw.startswith("```"):
            raw = raw[3:-3].strip()
        return json.loads(raw)
    except Exception as e:
        # Fallback judgment if failed
        winner = next((i["agent"] for i in implementations if not i.get("error")), "No Winner")
        return {
            "scores": {},
            "winner": winner,
            "winner_model": "unknown",
            "reasoning": "Fallback judgment due to error: " + str(e),
            "runner_up": "",
            "eliminated": []
        }
