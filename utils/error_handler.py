from functools import wraps
from graph.state import DevTeamState

def safe_agent(agent_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(state: DevTeamState) -> DevTeamState:
            try:
                return func(state)
            except Exception as e:
                print(f"❌ Error in {agent_name}: {e}")
                return {
                    **state,
                    "error": f"{agent_name}: {str(e)}",
                    "current_step": f"{agent_name}_failed"
                }
        return wrapper
    return decorator