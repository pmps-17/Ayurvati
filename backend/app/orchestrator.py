from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from backend.app.models import SessionLocal  # Your SQLAlchemy session
from sqlalchemy import text
from sentence_transformers import SentenceTransformer

# Load embedding model for queries
model = SentenceTransformer("all-MiniLM-L6-v2")

# --- VECTOR DB (Postgres + pgvector) RAG Retriever ---
class PgVectorRetriever:
    def __init__(self, k=5):
        self.k = k

    async def __call__(self, query: str):
        query_emb = model.encode(query).tolist()
        async with SessionLocal() as session:
            sql = text("""
                SELECT id, title, content, embedding <#> :q_emb AS distance
                FROM ayurveda_docs
                ORDER BY embedding <#> :q_emb
                LIMIT :limit
            """)
            result = await session.execute(sql, {"q_emb": query_emb, "limit": self.k})
            docs = result.fetchall()
            return [
                {"title": row.title, "content": row.content, "distance": row.distance}
                for row in docs
            ]

retriever = PgVectorRetriever()

# --- Initialize agents (as before) ---
user_proxy = UserProxyAgent(name="user_proxy")
memory_manager = AssistantAgent(name="memory_manager")
dosha_agent = AssistantAgent(name="dosha_agent")
mental_health_agent = AssistantAgent(name="mental_health_agent")
climate_agent = AssistantAgent(name="climate_agent")
deficiency_agent = AssistantAgent(name="deficiency_agent")
meal_planner_agent = AssistantAgent(name="meal_planner_agent")
herbal_advisor_agent = AssistantAgent(name="herbal_advisor_agent")

agents = [
    user_proxy,
    memory_manager,
    dosha_agent,
    mental_health_agent,
    climate_agent,
    deficiency_agent,
    meal_planner_agent,
    herbal_advisor_agent
]

group_chat = GroupChat(agents=agents, tools=[retriever], max_rounds=10, verbose=False)
group_chat_manager = GroupChatManager(group_chat=group_chat)

# --- Orchestration Function ---
import asyncio

def run_pipeline(user_input: str) -> str:
    # If your pipeline/agents/tools are now async, run inside event loop
    return asyncio.run(group_chat_manager.run(user_input))
