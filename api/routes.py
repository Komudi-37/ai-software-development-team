from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from graph.workflow import app_graph
from tools.file_tools import save_outputs
from tools.github_tools import push_project_to_github
import uuid

router = APIRouter()

class IdeaRequest(BaseModel):
    user_idea:    str
    project_name: str = "my_project"
    push_to_github: bool = False

@router.post("/generate")
async def generate_project(request: IdeaRequest):
    project_id = str(uuid.uuid4())[:8]
    initial_state = {
        "user_idea":     request.user_idea,
        "project_name":  request.project_name,
        "requirements":  None,
        "architecture":  None,
        "source_code":   None,
        "test_cases":    None,
        "documentation": None,
        "error":         None,
        "current_step":  "starting"
    }
    try:
        final_state = app_graph.invoke(initial_state)
        save_outputs(project_id, final_state)

        github_url = None
        if request.push_to_github:
            github_url = push_project_to_github(request.project_name, final_state)

        return {
            "project_id":    project_id,
            "status":        "completed",
            "error":         final_state.get("error"),
            "github_url":    github_url,
            "requirements":  final_state.get("requirements"),
            "architecture":  final_state.get("architecture"),
            "source_code":   final_state.get("source_code"),
            "test_cases":    final_state.get("test_cases"),
            "documentation": final_state.get("documentation"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))