import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DevTeamState
from prompts.developer_prompt import DEVELOPER_SYSTEM

load_dotenv()

# Change this in all 5 agent files:
llm = ChatOpenAI(
    model="nousresearch/hermes-3-llama-3.1-405b:free",   # ← updated model name
    temperature=0.3,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def developer_agent(state: DevTeamState) -> DevTeamState:
    print("💻 Developer Agent running...")
    try:
        messages = [
            SystemMessage(content=DEVELOPER_SYSTEM),
            HumanMessage(content=f"""
Requirements:
{state['requirements']}

Architecture Design:
{state['architecture']}
""")
        ]
        response = llm.invoke(messages)
        return {**state, "source_code": response.content, "current_step": "developer_done"}
    except Exception as e:
        print(f"❌ Developer Agent error: {e}")
        return {**state, "error": str(e), "current_step": "developer_failed"}