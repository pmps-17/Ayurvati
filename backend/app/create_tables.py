# backend/app/create_tables.py

import asyncio
from dotenv import load_dotenv

# Load environment variables from a .env file into os.environ
load_dotenv()

# Now that os.environ["DATABASE_URL"] is available, import engine/Base
from models import engine, Base

async def init_db():
    async with engine.begin() as conn:
        # Create all tables defined on Base.metadata
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created!")

if __name__ == "__main__":
    asyncio.run(init_db())
