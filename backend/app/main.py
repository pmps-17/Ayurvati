import os
from fastapi import FastAPI, HTTPException, Query
from typing import List
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Load environment variables (e.g., DATABASE_URL, OPENAI_API_KEY)
load_dotenv()
# Import your pipeline runner
from .orchestrator import run_pipeline

# Import Async session factory and ORM models
from .models import SessionLocal, MoodLog, SymptomLog, MealLog


app = FastAPI(
    title="Ayurveda Personal Doctor AI",
    version="0.1.0",
    description="AI-driven diet & wellness recommendations rooted in Ayurveda"
)

# Include the DB-backed logging router
from .routes.logs import router as logs_router

app.include_router(logs_router)


@app.get("/recommendations/diet")
async def get_diet_plan(user_email: str = Query(..., description="End user’s email")):
    """
    1. Fetch the most recent 5 entries of mood, symptom, and meal logs for this user from the database.
    2. Build a summary string from those logs.
    3. Send to the RAG/agent pipeline and return the generated diet plan.
    """
    async with SessionLocal() as session:  # type: AsyncSession
        # Fetch last 5 MoodLog entries for this user, ordered by timestamp descending
        mood_rows = await session.execute(
            select(MoodLog)
            .where(MoodLog.user_email == user_email)
            .order_by(MoodLog.timestamp.desc())
            .limit(5)
        )
        recent_moods = mood_rows.scalars().all()

        # Fetch last 5 SymptomLog entries
        symptom_rows = await session.execute(
            select(SymptomLog)
            .where(SymptomLog.user_email == user_email)
            .order_by(SymptomLog.timestamp.desc())
            .limit(5)
        )
        recent_symptoms = symptom_rows.scalars().all()

        # Fetch last 5 MealLog entries
        meal_rows = await session.execute(
            select(MealLog)
            .where(MealLog.user_email == user_email)
            .order_by(MealLog.timestamp.desc())
            .limit(5)
        )
        recent_meals = meal_rows.scalars().all()

    # Build a simple summary dictionary
    logs_summary = {
        "mood_logs": [
            {
                "mood": m.mood,
                "intensity": m.intensity,
                "timestamp": m.timestamp.isoformat()
            }
            for m in recent_moods
        ],
        "symptom_logs": [
            {
                "symptom": s.symptom,
                "severity": s.severity,
                "timestamp": s.timestamp.isoformat()
            }
            for s in recent_symptoms
        ],
        "meal_logs": [
            {
                "meal_type": ml.meal_type,
                # split back into list[str] if needed
                "items": ml.items.split(","),
                "timestamp": ml.timestamp.isoformat()
            }
            for ml in recent_meals
        ],
    }

    user_input = f"{logs_summary}"
    try:
        plan = run_pipeline(user_input)
        return {"plan": plan}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run:
# uvicorn main:app --reload --port 8000
