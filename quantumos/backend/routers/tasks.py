from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import orchestrator
import db
import json
import os

router = APIRouter()

class TaskRequest(BaseModel):
    task: str

@router.post("/run")
async def run_task(request: TaskRequest):
    try:
        result = await orchestrator.run_pipeline(request.task)
        run_id = await db.save_run(
            result["task"],
            result["plan"],
            result["implementations"],
            result["judgment"],
            result["validation"]
        )
        result["id"] = run_id
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=traceback.format_exc())

@router.get("/run/{run_id}")
async def get_run(run_id: int):
    run = await db.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.get("/demo")
async def get_demo():
    seed_path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "demo_seed.json")
    if os.path.exists(seed_path):
        with open(seed_path, "r") as f:
            return json.load(f)
    return {"message": "Demo seed not found. Please run scripts/seed_demo.py first."}
