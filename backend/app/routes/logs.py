from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.models import SessionLocal, MoodLog, SymptomLog, MealLog, ChatLog
import datetime

router = APIRouter()

# --- A. Mood Log Endpoint ---
class MoodLogRequest(BaseModel):
    user_email: str
    mood: str
    intensity: int

@router.post("/log/mood")
async def log_mood(entry: MoodLogRequest):
    async with SessionLocal() as session:
        mood_log = MoodLog(
            user_email=entry.user_email,
            mood=entry.mood,
            intensity=entry.intensity,
            timestamp=datetime.datetime.utcnow()
        )
        session.add(mood_log)
        await session.commit()
        return {"status": "logged", "entry": entry}

# --- B. Symptom Log Endpoint ---
class SymptomLogRequest(BaseModel):
    user_email: str
    symptom: str
    severity: int

@router.post("/log/symptom")
async def log_symptom(entry: SymptomLogRequest):
    async with SessionLocal() as session:
        symptom_log = SymptomLog(
            user_email=entry.user_email,
            symptom=entry.symptom,
            severity=entry.severity,
            timestamp=datetime.datetime.utcnow()
        )
        session.add(symptom_log)
        await session.commit()
        return {"status": "logged", "entry": entry}

# --- C. Meal Log Endpoint ---
class MealLogRequest(BaseModel):
    user_email: str
    meal_type: str
    items: list[str]

@router.post("/log/meal")
async def log_meal(entry: MealLogRequest):
    async with SessionLocal() as session:
        meal_log = MealLog(
            user_email=entry.user_email,
            meal_type=entry.meal_type,
            items=",".join(entry.items),  # Store as comma-separated string
            timestamp=datetime.datetime.utcnow()
        )
        session.add(meal_log)
        await session.commit()
        return {"status": "logged", "entry": entry}

# --- D. Chat Log Endpoint ---
class ChatLogRequest(BaseModel):
    user_email: str
    message: str
    sender: str

@router.post("/log/chat")
async def log_chat(entry: ChatLogRequest):
    async with SessionLocal() as session:
        chat_log = ChatLog(
            user_email=entry.user_email,
            message=entry.message,
            sender=entry.sender,
            timestamp=datetime.datetime.utcnow()
        )
        session.add(chat_log)
        await session.commit()
        return {"status": "logged", "entry": entry}

# --- E. Fetch Logs for User (example: mood logs) ---
@router.get("/logs/mood/{user_email}")
async def get_mood_logs(user_email: str):
    async with SessionLocal() as session:
        result = await session.execute(
            select(MoodLog).where(MoodLog.user_email == user_email)
        )
        return [row[0].__dict__ for row in result.fetchall()]
