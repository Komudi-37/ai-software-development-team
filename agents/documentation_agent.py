import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from graph.state import DevTeamState
from prompts.documentation_prompt import DOCUMENTATION_SYSTEM

load_dotenv()

# Change this in all 5 agent files:
llm = ChatOpenAI(
    model="nousresearch/hermes-3-llama-3.1-405b:free",   # ← updated model name
    temperature=0.3,
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

def documentation_agent(state: DevTeamState) -> DevTeamState:
    print("📚 Documentation Agent running...")
    try:
        messages = [
            SystemMessage(content=DOCUMENTATION_SYSTEM),
            HumanMessage(content=f"""
Original Idea: {state['user_idea']}

Requirements:
{state['requirements']}

Architecture:
{state['architecture']}

Source Code:
{state['source_code']}

Test Cases:
{state['test_cases']}
""")
        ]
        response = llm.invoke(messages)
        return {**state, "documentation": response.content, "current_step": "documentation_done"}
    except Exception as e:
        print(f"❌ Documentation Agent error: {e}")
        return {**state, "error": str(e), "current_step": "documentation_failed"}