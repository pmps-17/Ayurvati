# backend/app/orchestrator.py

import asyncio
from sqlalchemy import text
from sentence_transformers import SentenceTransformer

# ─── Autogen 0.9.1 imports ───────────────────────────────────────────────────────
from autogen.agentchat.user_proxy_agent import UserProxyAgent
from autogen.agentchat.assistant_agent import AssistantAgent
from autogen.agentchat.groupchat import GroupChat, GroupChatManager

# ─── Your SQLAlchemy AsyncSession factory ────────────────────────────────────────
from .models import SessionLocal

# ─── Embedding model for RAG retrieval ─────────────────────────────────────────
model = SentenceTransformer("all-MiniLM-L6-v2")


# ─── VECTOR DB retriever class (Postgres + pgvector) ─────────────────────────────
class PgVectorRetriever:
    def __init__(self, k: int = 5):
        self.k = k

    async def __call__(self, query: str):
        """
        1. Encode the query string to a 768-dim embedding.
        2. Run async SQL against the `ayurveda_docs` table (using pgvector’s <#> operator).
        3. Return a list of dicts with keys: title, content, distance.
        """
        query_emb = model.encode(query).tolist()

        async with SessionLocal() as session:
            sql = text("""
                SELECT
                    id,
                    title,
                    content,
                    embedding <#> :q_emb AS distance
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


# One global retriever instance (don’t reload the model on every request)
retriever = PgVectorRetriever(k=5)


# ─── Initialize all Autogen agents ───────────────────────────────────────────────
# None of these accept `retriever=` or `tools=` in Autogen 0.9.1.
user_proxy           = UserProxyAgent(name="user_proxy")
memory_manager       = AssistantAgent(name="memory_manager")
dosha_agent          = AssistantAgent(name="dosha_agent")
mental_health_agent  = AssistantAgent(name="mental_health_agent")
climate_agent        = AssistantAgent(name="climate_agent")
deficiency_agent     = AssistantAgent(name="deficiency_agent")
meal_planner_agent   = AssistantAgent(name="meal_planner_agent")
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


# ─── Build the GroupChat ──────────────────────────────────────────────────────────
# According to Autogen 0.9.1, the signature is:
#    GroupChat.__init__(self, agents, messages=<factory>, max_round=10, admin_name="Admin", …)
#
# We will supply only the `agents` list and override `max_round` if desired.
group_chat = GroupChat(
    agents,          # required positional argument
    max_round=10     # override the default of 10 (if you want more/fewer rounds)
    # (all other keywords use their default values)
)


# ─── Build the GroupChatManager ───────────────────────────────────────────────────
# The signature is:
#    GroupChatManager.__init__(self, groupchat: GroupChat)
#
group_chat_manager = GroupChatManager(group_chat)


# ─── Orchestration entrypoint ─────────────────────────────────────────────────────
def run_pipeline(user_input: str) -> str:
    """
    1. Do a vector search (RAG) using PgVectorRetriever.
    2. Format the top-k docs into a “context” string.
    3. Prepend that context to the user’s question.
    4. Pass the combined prompt into group_chat_manager.run(...).
    5. Return the final text response.
    """
    async def _inner():
        # (1) Retrieve up to k documents for RAG
        docs = await retriever(user_input)

        # (2) Build a simple “context” string from the results
        if docs:
            lines = []
            for idx, doc in enumerate(docs, start=1):
                lines.append(
                    f"Doc {idx} – Title: {doc['title']}\n"
                    f"Content: {doc['content']}\n"
                    f"Score: {doc['distance']:.3f}\n"
                )
            rag_context = "\n".join(lines)
        else:
            rag_context = "No relevant documents found."

        # (3) Combine the RAG context + the user’s original question
        combined_prompt = f"Context:\n{rag_context}\n\nUser asks: {user_input}"

        # (4) Run the GroupChat pipeline (it’s async, so we await it)
        return await group_chat_manager.run(combined_prompt)

    # Since run(...) is async, wrap it in asyncio.run() for a synchronous API
    return asyncio.run(_inner())
