import asyncio
from agents.planner import plan_task
from agents.battle import run_battle
from agents.judge import judge_battle
from agents.validator import validate_patch

async def run_pipeline(task: str) -> dict:
    plan = await plan_task(task)
    implementations = await run_battle(task, plan)
    judgment = await judge_battle(plan, implementations)
    winner_name = judgment.get("winner") if judgment else None
    winning_impl = next((i for i in implementations if i.get("agent") == winner_name), None)
    
    validation = {"status": "FAIL", "checked_files": [], "notes": ["Winner not found"]}
    if winning_impl and "files" in winning_impl:
        validation = await validate_patch(winning_impl["files"])
        
    return {
        "task": task,
        "plan": plan,
        "implementations": implementations,
        "judgment": judgment,
        "validation": validation
    }
