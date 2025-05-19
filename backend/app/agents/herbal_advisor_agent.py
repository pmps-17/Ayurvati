
from autogen import AssistantAgent
from autogen import config_list_from_dotenv

# Load OpenAI config (make sure you have an .env file with OPENAI_API_KEY)
config_list = config_list_from_dotenv(dotenv_file_path=".env")

herbal_advisor_agent = AssistantAgent(
    name="HerbalAdvisorAgent",
    system_prompt="""
You are the HerbalAdvisorAgent.
Recommend Ayurvedic herbs, teas, and routines for today’s plan.
If you need user context (e.g., current medications), ask:
  - "Are you taking any medications we should be aware of?"
Return JSON:
{"herbs": ["..."], "routines": ["..."]}
Flag any herb-drug interactions.
""",
    llm_config={"config_list": config_list}
)
