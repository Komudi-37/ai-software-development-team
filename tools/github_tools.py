# tools/github_tools.py
import requests
import base64
import os
from dotenv import load_dotenv
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER  = os.getenv("GITHUB_USERNAME")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_repo(repo_name: str) -> str:
    """Creates a new GitHub repo and returns its URL."""
    response = requests.post(
        "https://api.github.com/user/repos",
        headers=HEADERS,
        json={"name": repo_name, "private": False, "auto_init": True}
    )
    response.raise_for_status()
    return response.json()["html_url"]

def push_file(repo_name: str, file_path: str, content: str, commit_msg: str):
    """Pushes a single file to the GitHub repo."""
    encoded = base64.b64encode(content.encode()).decode()
    url = f"https://api.github.com/repos/{GITHUB_USER}/{repo_name}/contents/{file_path}"
    
    # Check if file exists (to get its sha for updates)
    existing = requests.get(url, headers=HEADERS)
    sha = existing.json().get("sha") if existing.status_code == 200 else None
    
    payload = {"message": commit_msg, "content": encoded}
    if sha:
        payload["sha"] = sha
    
    requests.put(url, headers=HEADERS, json=payload).raise_for_status()

def push_project_to_github(project_name: str, state: dict):
    """Pushes all generated files to a new GitHub repository."""
    repo_url = create_repo(project_name)
    
    files_to_push = {
        "requirements.md": state["requirements"],
        "architecture.md": state["architecture"],
        "src/main.py":     state["source_code"],
        "tests/test_main.py": state["test_cases"],
        "README.md":       state["documentation"],
    }
    
    for path, content in files_to_push.items():
        if content:
            push_file(project_name, path, content, f"Add {path} via AI Dev Team")
    
    return repo_url