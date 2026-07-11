# graph/state.py
from typing import TypedDict, Optional

class DevTeamState(TypedDict):
    # Input
    user_idea: str
    
    # Agent outputs (each agent fills its slot)
    requirements: Optional[str]
    architecture: Optional[str]
    source_code: Optional[str]
    test_cases: Optional[str]
    documentation: Optional[str]
    
    # Metadata
    project_name: Optional[str]
    error: Optional[str]
    current_step: Optional[str]