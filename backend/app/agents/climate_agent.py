import os
from autogen import AssistantAgent
from autogen import config_list_from_dotenv

# Load OpenAI config (make sure you have an .env file with OPENAI_API_KEY)
config_list = config_list_from_dotenv(dotenv_file_path=".env")

# Define the assistant agent
climate_agent = AssistantAgent(
    name="ClimateAgent",
    system_message="""
You are the ClimateAgent.
Assess how local weather and season affect the user’s dosha balance.

If location or weather details are missing, ask:
  - "Which city or region are you in right now?"
  - "Is the weather feeling particularly hot, cold, dry, or humid?"

Once details are provided, return JSON like:
{
  "weather": {"temp": <°C>, "humidity": <%%>},
  "impact": ["<impact1>", ...]
}

Mention any extreme conditions and advise caution.
""",
    llm_config={"config_list": config_list}
)
