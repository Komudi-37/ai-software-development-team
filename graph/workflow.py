# graph/workflow.py
from langgraph.graph import StateGraph, END
from graph.state import DevTeamState
from agents.requirements_agent import requirements_agent
from agents.architecture_agent import architecture_agent
from agents.developer_agent import developer_agent
from agents.tester_agent import tester_agent
from agents.documentation_agent import documentation_agent

def build_workflow():
    # Create the graph
    workflow = StateGraph(DevTeamState)
    
    # Add all agent nodes
    workflow.add_node("requirements",   requirements_agent)
    workflow.add_node("architecture",   architecture_agent)
    workflow.add_node("developer",      developer_agent)
    workflow.add_node("tester",         tester_agent)
    workflow.add_node("documentation",  documentation_agent)
    
    # Define the linear pipeline flow
    workflow.set_entry_point("requirements")
    workflow.add_edge("requirements",  "architecture")
    workflow.add_edge("architecture",  "developer")
    workflow.add_edge("developer",     "tester")
    workflow.add_edge("tester",        "documentation")
    workflow.add_edge("documentation", END)
    
    return workflow.compile()

# This is what you import everywhere
app_graph = build_workflow()