import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import TIMESTAMP
from pgvector.sqlalchemy import Vector
import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class AyurvedaDoc(Base):
    __tablename__ = "ayurveda_docs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    embedding = Column(Vector(768))

class MoodLog(Base):
    __tablename__ = "mood_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    mood = Column(String)
    intensity = Column(Integer)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)

class SymptomLog(Base):
    __tablename__ = "symptom_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    symptom = Column(String)
    severity = Column(Integer)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)

class MealLog(Base):
    __tablename__ = "meal_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    meal_type = Column(String)
    items = Column(Text)  # store as comma-separated list or JSON
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)

class ChatLog(Base):
    __tablename__ = "chat_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True)
    message = Column(Text)
    sender = Column(String)
    timestamp = Column(TIMESTAMP, default=datetime.datetime.utcnow)
