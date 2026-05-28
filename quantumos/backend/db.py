import aiosqlite
import json
import os

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./quantumos.db").replace("sqlite:///", "")

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                plan JSON,
                implementations JSON,
                judgment JSON,
                validation JSON
            )
        """)
        await db.commit()

async def save_run(task, plan, implementations, judgment, validation):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO runs (task, plan, implementations, judgment, validation)
            VALUES (?, ?, ?, ?, ?)
        """, (
            task, 
            json.dumps(plan), 
            json.dumps(implementations), 
            json.dumps(judgment), 
            json.dumps(validation)
        ))
        await db.commit()
        return cursor.lastrowid

async def get_run(run_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM runs WHERE id = ?", (run_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "task": row["task"],
                    "plan": json.loads(row["plan"]),
                    "implementations": json.loads(row["implementations"]),
                    "judgment": json.loads(row["judgment"]),
                    "validation": json.loads(row["validation"]),
                }
            return None
