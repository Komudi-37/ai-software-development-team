import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DevTeamState
from prompts.requirements_prompt import REQUIREMENTS_SYSTEM

load_dotenv()

# Change this in all 5 agent files:
llm = ChatOpenAI(
    model="nousresearch/hermes-3-llama-3.1-405b:free",   # ← updated model name
    temperature=0.3,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def requirements_agent(state: DevTeamState) -> DevTeamState:
    print("🔍 Requirements Agent running...")
    try:
        messages = [
            SystemMessage(content=REQUIREMENTS_SYSTEM),
            HumanMessage(content=f"Software Idea: {state['user_idea']}")
        ]
        response = llm.invoke(messages)
        return {**state, "requirements": response.content, "current_step": "requirements_done"}
    except Exception as e:
        print(f"❌ Requirements Agent error: {e}")
        return {**state, "error": str(e), "current_step": "requirements_failed"}