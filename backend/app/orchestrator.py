from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from chromadb import Client as ChromaClient

# Initialize retrieval tool
chroma = ChromaClient().get_or_create_collection("ayurveda")

class RetrieverTool:
    def __call__(self, query: str, k: int = 5):
        results = chroma.query(query_texts=[query], n_results=k)
        return [m["documents"][0] for m in results["matches"]]

retriever = RetrieverTool()

# Initialize agents
user_proxy = UserProxyAgent(name="user_proxy")
memory_manager = AssistantAgent(name="memory_manager")
dosha_agent = AssistantAgent(name="dosha_agent")
mental_health_agent = AssistantAgent(name="mental_health_agent")
climate_agent = AssistantAgent(name="climate_agent")
deficiency_agent = AssistantAgent(name="deficiency_agent")
meal_planner_agent = AssistantAgent(name="meal_planner_agent")
herbal_advisor_agent = AssistantAgent(name="herbal_advisor_agent")

# Create a list of agents
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

# Initialize GroupChat
group_chat = GroupChat(agents=agents, tools=[retriever], max_rounds=10, verbose=False)

# Initialize GroupChatManager
group_chat_manager = GroupChatManager(group_chat=group_chat)

def run_pipeline(user_input: str) -> str:
    return group_chat_manager.run(user_input)
