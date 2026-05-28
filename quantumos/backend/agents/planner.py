import os
import json
from groq import AsyncGroq

async def plan_task(task: str) -> dict:
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    model = os.getenv("GROQ_PLANNER_MODEL", "llama3-70b-8192")
    
    prompt = f"""You are a senior software engineer acting as a tech lead.
Your job is to break down a coding task into a clear execution plan.
Return ONLY valid JSON. No markdown. No explanation outside the JSON.
Task: {task}

Output schema:
{{
  "subtasks": [
    {{
      "id": 1,
      "title": "...",
      "description": "...",
      "files": ["main.py", "auth.py"],
      "constraints": ["must not break existing routes"]
    }}
  ],
  "risks": ["JWT secret must be env var, not hardcoded"],
  "context": "FastAPI app using standard routing, no existing auth layer"
}}
"""
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        raw = resp.choices[0].message.content.strip()
        # sometimes they wrap in markdown
        if raw.startswith("```json"):
            raw = raw[7:-3].strip()
        elif raw.startswith("```"):
            raw = raw[3:-3].strip()
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e), "subtasks": []}
