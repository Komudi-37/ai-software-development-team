import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DevTeamState
from prompts.architecture_prompt import ARCHITECTURE_SYSTEM

load_dotenv()

# Change this in all 5 agent files:
llm = ChatOpenAI(
    model="nousresearch/hermes-3-llama-3.1-405b:free",   # ← updated model name
    temperature=0.3,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def architecture_agent(state: DevTeamState) -> DevTeamState:
    print("🏗️ Architecture Agent running...")
    try:
        messages = [
            SystemMessage(content=ARCHITECTURE_SYSTEM),
            HumanMessage(content=f"""
Requirements Document:
{state['requirements']}

Original Idea: {state['user_idea']}
""")
        ]
        response = llm.invoke(messages)
        return {**state, "architecture": response.content, "current_step": "architecture_done"}
    except Exception as e:
        print(f"❌ Architecture Agent error: {e}")
        return {**state, "error": str(e), "current_step": "architecture_failed"}