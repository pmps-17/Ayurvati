
from autogen import AssistantAgent
from autogen import config_list_from_dotenv

# Load OpenAI config (make sure you have an .env file with OPENAI_API_KEY)
config_list = config_list_from_dotenv(dotenv_file_path=".env")

memory_manager = AssistantAgent(
    name="MemoryManager",
    system_prompt="""
You are the MemoryManager.
Store and retrieve user history: moods, meals, symptoms, climate impacts, past plans.
If an agent asks for recent data, provide anonymized summaries.
Never expose personal identifiers. If data is missing, inform the UserProxyAgent:
"Missing data: [describe]".
""",
    llm_config={"config_list": config_list}
)
