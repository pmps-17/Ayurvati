from fastapi import APIRouter, HTTPException, Request
from backend.app.models import SessionLocal, MoodLog, SymptomLog, MealLog, ChatLog
from backend.app.orchestrator import run_pipeline, get_relevant_ayurveda_docs
from sqlalchemy.future import select

router = APIRouter()

@router.post("/recommend")
async def recommend(request: Request):
    data = await request.json()
    user_email = data.get("user_email")
    user_message = data.get("message")

    # 1. Fetch latest user logs (past 5-10 entries for each type)
    async with SessionLocal() as session:
        mood_logs = await session.execute(
            select(MoodLog).where(MoodLog.user_email == user_email).order_by(MoodLog.timestamp.desc()).limit(5)
        )
        symptom_logs = await session.execute(
            select(SymptomLog).where(SymptomLog.user_email == user_email).order_by(SymptomLog.timestamp.desc()).limit(5)
        )
        meal_logs = await session.execute(
            select(MealLog).where(MealLog.user_email == user_email).order_by(MealLog.timestamp.desc()).limit(5)
        )
        # Optionally chat logs as well

        mood_logs = [row[0].__dict__ for row in mood_logs.fetchall()]
        symptom_logs = [row[0].__dict__ for row in symptom_logs.fetchall()]
        meal_logs = [row[0].__dict__ for row in meal_logs.fetchall()]

    # 2. Fetch relevant Ayurveda docs via RAG search
    rag_docs = await get_relevant_ayurveda_docs(user_message, k=3)  # can adjust k

    # 3. Build context for your agent pipeline
    context = {
        "user_message": user_message,
        "mood_logs": mood_logs,
        "symptom_logs": symptom_logs,
        "meal_logs": meal_logs,
        "rag_docs": rag_docs
    }

    # 4. Call your multi-agent orchestrator (can adapt run_pipeline to accept context dict)
    try:
        result = await run_pipeline(context)  # You may need to make run_pipeline async and accept context
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
