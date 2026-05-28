import json
import os

def create_seed_data():
    seed_data = {
        "task": "Add JWT authentication to a FastAPI app",
        "plan": {
            "subtasks": [{"id": 1, "title": "Setup JWT", "description": "Add JWT auth logic", "files": ["auth.py", "main.py"], "constraints": []}],
            "risks": ["JWT secret must be env var"],
            "context": "FastAPI app"
        },
        "implementations": [
            {"agent": "The Pragmatist", "model": "llama3-70b-8192", "files": [], "rationale": "Simple implementation"},
            {"agent": "The Architect", "model": "mixtral-8x7b-32768", "files": [], "rationale": "Clean abstractions"},
            {"agent": "The Speed Demon", "model": "llama3-8b-8192", "files": [], "rationale": "Fast and dirty"},
            {"agent": "The Purist", "model": "gemma2-9b-it", "files": [], "rationale": "Strict typing"},
            {"agent": "The Veteran", "model": "llama-3.1-70b-versatile", "files": [
                {"path": "auth.py", "content": "import os\nfrom datetime import datetime, timedelta\nfrom jose import jwt\n\nSECRET_KEY = os.getenv('JWT_SECRET', 'supersecret')\nALGORITHM = 'HS256'\n\ndef create_access_token(data: dict):\n    to_encode = data.copy()\n    expire = datetime.utcnow() + timedelta(minutes=15)\n    to_encode.update({'exp': expire})\n    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)\n    return encoded_jwt\n"},
                {"path": "main.py", "content": "from fastapi import FastAPI, Depends, HTTPException, status\nfrom fastapi.security import OAuth2PasswordBearer\nfrom auth import create_access_token\n\napp = FastAPI()\noauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')\n\n@app.get('/users/me')\ndef read_users_me(token: str = Depends(oauth2_scheme)):\n    return {'token': token}\n"}
            ], "rationale": "Defensive code with env vars"},
            {"agent": "The Reasoner", "model": "deepseek-r1-distill-llama-70b", "files": [], "rationale": "Step-by-step logic"}
        ],
        "judgment": {
            "scores": {
                "The Pragmatist": {"correctness": 8, "maintainability": 6, "simplicity": 9, "testability": 6, "total": 29},
                "The Architect": {"correctness": 8, "maintainability": 9, "simplicity": 7, "testability": 8, "total": 32},
                "The Speed Demon": {"correctness": 7, "maintainability": 5, "simplicity": 9, "testability": 5, "total": 26},
                "The Purist": {"correctness": 9, "maintainability": 8, "simplicity": 7, "testability": 9, "total": 33},
                "The Veteran": {"correctness": 9, "maintainability": 8, "simplicity": 8, "testability": 9, "total": 34},
                "The Reasoner": {"correctness": 8, "maintainability": 7, "simplicity": 7, "testability": 8, "total": 30}
            },
            "winner": "The Veteran",
            "winner_model": "llama-3.1-70b-versatile",
            "reasoning": "The Veteran produced the most complete implementation with proper error handling and env-based secret management.",
            "runner_up": "The Purist",
            "eliminated": [{"agent": "The Speed Demon", "reason": "Missing token expiry handling, unsafe secret."}]
        },
        "validation": {
            "status": "PASS",
            "checked_files": ["auth.py", "main.py"],
            "notes": ["AST parse successful", "No undefined names detected"]
        }
    }

    os.makedirs('data', exist_ok=True)
    with open('data/demo_seed.json', 'w') as f:
        json.dump(seed_data, f, indent=2)
    print("Seed data written to data/demo_seed.json")

if __name__ == "__main__":
    create_seed_data()
