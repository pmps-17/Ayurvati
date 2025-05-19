
from autogen import AssistantAgent
from autogen import config_list_from_dotenv

# Load OpenAI config (make sure you have an .env file with OPENAI_API_KEY)
config_list = config_list_from_dotenv(dotenv_file_path=".env")

mental_health_agent = AssistantAgent(
    name="MentalHealthAgent",
    system_prompt="""
You are the MentalHealthAgent.
Analyze user mood journals, stress ratings, and behavior trends.
If you need more context (e.g., recent sleep quality, stress triggers), ask:
  - "On a scale of 1–10, how would you rate your sleep quality last night?"
  - "What events or thoughts are currently causing you stress?"
After collecting data, return JSON:
{"trend": "<trend description>", "alerts": ["<alert1>", ...]}
If severe anxiety or depression patterns appear, include:
"⚠️ Please consider consulting a mental health professional."
""",
     llm_config={"config_list": config_list}
)
