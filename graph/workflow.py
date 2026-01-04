from langgraph.graph import StateGraph, END
from utils.state import ResearchState
from agents.researcher import researcher_node
from agents.analyst import analyst_node
from agents.writer import writer_node
from agents.fact_checker import fact_checker_node
from agents.critic import critic_node

def create_research_workflow():
    """Multi-agent workflow එක build කරනවා"""
    
    # StateGraph එක initialize කරනවා
    workflow = StateGraph(ResearchState)
    
    # හැම agent එකම nodes විදිහට add කරනවා
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("fact_checker", fact_checker_node)
    workflow.add_node("critic", critic_node)
    
    # Workflow එකේ starting point එක set කරනවා
    workflow.set_entry_point("researcher")
    
    # Agent අතර connections හදනවා (conditional routing)
    workflow.add_conditional_edges(
        "researcher",
        lambda state: state["next_agent"],#Lambda = Small, quick function එකක් (name එකක් නැතිව)
        {
            "analyst": "analyst",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "analyst",
        lambda state: state["next_agent"],
        {
            "writer": "writer",
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "writer",
        lambda state: state["next_agent"],
        {
        "fact_checker": "fact_checker",  # Normal flow
        "writer": "writer",              # Revision path
        "critic": "critic",              # If you allow skipping fact-checker
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "fact_checker",
        lambda state: state["next_agent"],{
        "writer": "writer",   # if corrections needed
        "critic": "critic",   # if approved
        "end": END            # optional
    }
    )
    
    workflow.add_conditional_edges(
        "critic",
        lambda state: state["next_agent"],
        {
            "writer": "writer",  # Revision වලට
            "end": END
        }
    )
    
    # Workflow compile කරනවා
    app = workflow.compile()
    return app