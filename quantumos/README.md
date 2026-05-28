# QuantumOS ⚡

QuantumOS is a multi-model AI battle arena for software engineering. Submit a coding task, and 6 specialized AI agents (powered by Groq) will compete to implement the best solution. A Judge scores them, and you get a single, validated winning patch.

## Features
- **Parallel Execution**: 6 distinct models/personas write code simultaneously.
- **Judge Scoring**: Evaluated on Correctness, Maintainability, Simplicity, Testability.
- **Auto Validation**: AST syntax checking ensures the code is runnable.
- **Instant Demo**: Fast fallback mode for hackathon judging.

## Setup

### Backend
1. `cd backend`
2. `python -m venv .venv`
3. `source .venv/bin/activate` (or `.\.venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. Create a `.env` file in the root with `GROQ_API_KEY=your_key`
6. `uvicorn main:app --reload`

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`
4. Open `http://localhost:3000`

## Demo Mode
To bypass live AI calls during presentations, append `?demo=true` to the battle URL:
`http://localhost:3000/battle?demo=true`
