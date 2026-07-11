# tools/file_tools.py
import os

def save_outputs(project_id: str, state: dict):
    """Saves all agent outputs to the output/ directory."""
    
    base = f"output/{project_id}"
    os.makedirs(f"{base}/code",  exist_ok=True)
    os.makedirs(f"{base}/tests", exist_ok=True)
    os.makedirs(f"{base}/docs",  exist_ok=True)
    
    files = {
        f"{base}/requirements.md":   state.get("requirements", ""),
        f"{base}/architecture.md":   state.get("architecture", ""),
        f"{base}/code/main.py":      state.get("source_code", ""),
        f"{base}/tests/test_main.py": state.get("test_cases", ""),
        f"{base}/docs/README.md":    state.get("documentation", ""),
    }
    
    for path, content in files.items():
        with open(path, "w", encoding="utf-8") as f:
            f.write(content or "# No content generated")
    
    print(f"✅ Outputs saved to {base}/")