import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DevTeamState
from prompts.tester_prompt import TESTER_SYSTEM

load_dotenv()

# Change this in all 5 agent files:
llm = ChatOpenAI(
    model="nousresearch/hermes-3-llama-3.1-405b:free",   # ← updated model name
    temperature=0.3,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def tester_agent(state: DevTeamState) -> DevTeamState:
    print("🧪 Tester Agent running...")
    try:
        messages = [
            SystemMessage(content=TESTER_SYSTEM),
            HumanMessage(content=f"""
Requirements:
{state['requirements']}

Source Code:
{state['source_code']}
""")
        ]
        response = llm.invoke(messages)
        return {**state, "test_cases": response.content, "current_step": "tester_done"}
    except Exception as e:
        print(f"❌ Tester Agent error: {e}")
        return {**state, "error": str(e), "current_step": "tester_failed"}