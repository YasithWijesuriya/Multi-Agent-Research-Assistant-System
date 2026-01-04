from typing import TypedDict, List
from langchain_core.messages import BaseMessage

class ResearchState(TypedDict, total=False):
    """Research process එකේ state එක track කරන්න"""
    topic: str  # Research topic
    research_data: List[str]  # Web search results
    analysis: str  # Analyzed insights
    draft_report: str  # Initial report
    final_report: str  # Polished report

    messages: List[BaseMessage]  # Chat history

    logs: List[str]  # Process logs

    iterations: int  # Revision count
    next_agent: str  # Next agent to execute
    corrections: List[str]  # optional for fact_checker


def create_initial_state(topic: str) -> ResearchState:
    """Initial state එක හදන helper function"""
    return {
        "topic": topic,
        "research_data": [],
        "analysis": "",
        "draft_report": "",
        "final_report": "",
        "messages": [],
        "logs": [],
        "iterations": 0,
        "next_agent": "researcher",
        "corrections": []
    }