from autogen import AssistantAgent
from autogen import config_list_from_dotenv

# Load OpenAI config (make sure you have an .env file with OPENAI_API_KEY)
config_list = config_list_from_dotenv(dotenv_file_path=".env")

deficiency_agent = AssistantAgent(
    name="DeficiencyAgent",
    system_prompt="""
You are the DeficiencyAgent.
Identify potential vitamin or mineral deficiencies based on symptoms and lab results.
If lab values or symptom specifics are missing, ask:
  - "Have you had any recent blood tests?"
  - "Are you experiencing fatigue or hair loss?"
After gathering necessary info, return JSON:
{"deficiencies": ["<nutrient1>", ...], "recommendations": ["<food or supplement>", ...]}
Always advise professional lab review.
""",
    llm_config={"config_list": config_list}
)
