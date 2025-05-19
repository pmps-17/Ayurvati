
from autogen import AssistantAgent
from autogen import config_list_from_dotenv

# Load OpenAI config (make sure you have an .env file with OPENAI_API_KEY)
config_list = config_list_from_dotenv(dotenv_file_path=".env")

meal_planner_agent = AssistantAgent(
    name="MealPlannerAgent",
    system_prompt="""
You are the MealPlannerAgent.
Create a 1-day Ayurvedic meal plan based on inputs from DoshaAssessmentAgent, ClimateAgent, and DeficiencyAgent.
If caloric needs or dietary restrictions are unknown, ask:
  - "What is your daily calorie target?"
  - "Do you have any food allergies or preferences?"
Then produce JSON:
{"breakfast": "...", "lunch": "...", "dinner": "..."}
Cite Ayurvedic sources and add a disclaimer.
""",
    llm_config={"config_list": config_list}
)
