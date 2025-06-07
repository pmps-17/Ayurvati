from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from ..models import SessionLocal, MoodLog, SymptomLog, MealLog, ChatLog
import datetime

router = APIRouter()


# A. Mood Log Endpoint
class MoodLogRequest(BaseModel):
    user_email: str
    mood: str
    intensity: int

@router.post("/log/mood", status_code=201)
async def log_mood(entry: MoodLogRequest):
    async with SessionLocal() as session:
        try:
            mood_log = MoodLog(
                user_email=entry.user_email,
                mood=entry.mood,
                intensity=entry.intensity,
                timestamp=datetime.datetime.utcnow()
            )
            session.add(mood_log)
            await session.commit()
            return {"status": "logged", "entry": entry}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# B. Symptom Log Endpoint
class SymptomLogRequest(BaseModel):
    user_email: str
    symptom: str
    severity: int

@router.post("/log/symptom", status_code=201)
async def log_symptom(entry: SymptomLogRequest):
    async with SessionLocal() as session:
        try:
            symptom_log = SymptomLog(
                user_email=entry.user_email,
                symptom=entry.symptom,
                severity=entry.severity,
                timestamp=datetime.datetime.utcnow()
            )
            session.add(symptom_log)
            await session.commit()
            return {"status": "logged", "entry": entry}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# C. Meal Log Endpoint
class MealLogRequest(BaseModel):
    user_email: str
    meal_type: str
    items: list[str]

@router.post("/log/meal", status_code=201)
async def log_meal(entry: MealLogRequest):
    async with SessionLocal() as session:
        try:
            meal_log = MealLog(
                user_email=entry.user_email,
                meal_type=entry.meal_type,
                # Store as comma-separated string for simplicity
                items=",".join(entry.items),
                timestamp=datetime.datetime.utcnow()
            )
            session.add(meal_log)
            await session.commit()
            return {"status": "logged", "entry": entry}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# D. Chat Log Endpoint
class ChatLogRequest(BaseModel):
    user_email: str
    message: str
    sender: str

@router.post("/log/chat", status_code=201)
async def log_chat(entry: ChatLogRequest):
    async with SessionLocal() as session:
        try:
            chat_log = ChatLog(
                user_email=entry.user_email,
                message=entry.message,
                sender=entry.sender,
                timestamp=datetime.datetime.utcnow()
            )
            session.add(chat_log)
            await session.commit()
            return {"status": "logged", "entry": entry}
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# E. Fetch Mood Logs for a User
@router.get("/logs/mood/{user_email}")
async def get_mood_logs(user_email: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(MoodLog).where(MoodLog.user_email == user_email)
        )
        rows = result.scalars().all()
        # Convert each SQLAlchemy object to a JSON‐serializable dict
        return [
            {
                "id": row.id,
                "user_email": row.user_email,
                "mood": row.mood,
                "intensity": row.intensity,
                "timestamp": row.timestamp.isoformat()
            }
            for row in rows
        ]
