from langchain_tavily import TavilySearch
from langchain_core.tools import tool

def create_search_tools():
    """අන්තර්ජාලය සෙවීමට අවශ්‍ය tools සකස් කරයි."""
    
    tavily_search = TavilySearch(
        max_results=5,
        search_depth="advanced",
        include_answer=True,
        include_raw_content=True
    )
    
    @tool
    def web_search(query: str) -> str:
        """Search the web for current information on any topic. 
        Use this when you need recent data or facts."""
        return tavily_search.invoke(query)
    
    return [web_search]