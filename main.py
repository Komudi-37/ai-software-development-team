# main.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from graph.workflow import app_graph
from tools.file_tools import save_outputs
import uuid
from api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI Software Development Team",
    description="Multi-agent system that builds software from ideas",
    version="1.0.0"
)
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok", "agents": 5}
class IdeaRequest(BaseModel):
    user_idea: str
    project_name: str = "my_project"

class PipelineResponse(BaseModel):
    project_id: str
    status: str
    requirements: str | None = None
    architecture: str | None = None
    source_code:  str | None = None
    test_cases:   str | None = None
    documentation: str | None = None

@app.post("/generate", response_model=PipelineResponse)
async def generate_project(request: IdeaRequest):
    """
    Main endpoint — takes a software idea, runs all 5 agents,
    returns the complete deliverable package.
    """
    project_id = str(uuid.uuid4())[:8]
    
    # Initial state
    initial_state = {
        "user_idea": request.user_idea,
        "project_name": request.project_name,
        "requirements": None,
        "architecture": None,
        "source_code": None,
        "test_cases": None,
        "documentation": None,
        "error": None,
        "current_step": "starting"
    }
    
    try:
        # Run the full LangGraph pipeline
        final_state = app_graph.invoke(initial_state)
        
        # Save outputs to disk
        save_outputs(project_id, final_state)
        
        return PipelineResponse(
            project_id=project_id,
            status="completed",
            **{k: final_state[k] for k in [
                "requirements", "architecture",
                "source_code", "test_cases", "documentation"
            ]}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "agents": 5}