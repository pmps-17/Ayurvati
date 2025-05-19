
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Import your pipeline runner
from backend.app.orchestrator import run_pipeline

app = FastAPI(
    title="Ayurveda Personal Doctor AI",
    version="0.1.0",
    description="AI-driven diet & wellness recommendations rooted in Ayurveda"
)

# --- Data Models --- #
class MoodLog(BaseModel):
    mood: str = Field(..., description="User mood description")
    intensity: int = Field(..., ge=1, le=10, description="Mood intensity 1-10")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SymptomLog(BaseModel):
    symptom: str = Field(..., description="Physical or mental symptom")
    severity: int = Field(..., ge=1, le=10, description="Severity 1-10")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class MealLog(BaseModel):
    meal_type: str = Field(..., description="Breakfast, Lunch, Dinner, Snack")
    items: List[str] = Field(..., description="List of foods consumed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# In‑memory store (swap for DB later)
mood_logs: List[MoodLog] = []
symptom_logs: List[SymptomLog] = []
meal_logs: List[MealLog] = []

# --- Endpoints --- #
@app.post("/log/mood", status_code=201)
async def log_mood(entry: MoodLog):
    mood_logs.append(entry)
    return {"status": "logged", "entry": entry}

@app.post("/log/symptom", status_code=201)
async def log_symptom(entry: SymptomLog):
    symptom_logs.append(entry)
    return {"status": "logged", "entry": entry}

@app.post("/log/meal", status_code=201)
async def log_meal(entry: MealLog):
    meal_logs.append(entry)
    return {"status": "logged", "entry": entry}

@app.get("/recommendations/diet")
async def get_diet_plan():
    """
    Collate latest logs and climate → run the multi-agent pipeline → return plan.
    """
    # Build a single input string for the agents
    logs_summary = {
        "mood_logs": [l.dict() for l in mood_logs[-5:]],
        "symptom_logs": [s.dict() for s in symptom_logs[-5:]],
        "meal_logs": [m.dict() for m in meal_logs[-5:]],
    }
    user_input = f"{logs_summary}"
    try:
        plan = run_pipeline(user_input)
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Run with: uvicorn app.main:app --reload --port 8000 ---
