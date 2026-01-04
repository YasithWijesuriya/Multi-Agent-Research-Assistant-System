import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import AIMessage

def create_writer_agent():
    """Professional report එකක් ලියන agent එක"""
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7  # More creative for writing
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Writing Agent specialized in creating professional reports.
        
        Your job:
        1. Take the research and analysis provided
        2. Write a comprehensive, well-structured report
        3. Use clear headings and sections
        4. Include: Introduction, Key Findings, Analysis, Conclusion
        5. Write in a professional, engaging style
        
        Make it publication-ready."""),
        
        ("human", """Topic: {topic}

Analysis:
{analysis}

Please write a professional research report.""")
    ])
    
    chain = prompt | llm
    return chain

def writer_node(state):
    logs = state.get("logs", [])
    logs.append("Writer node started.")
    time_start = time.time()
    print("🔹 WRITER NODE STATE KEYS:", state.keys())
    """Report එක ලියල state update කරනවා"""
    
    chain = create_writer_agent()
    
    result = chain.invoke({
        "topic": state["topic"],
        "analysis": state["analysis"]
    })


    messages = state.get("messages", [])
    messages.append(AIMessage(
        content="Draft completed",
        name="writer"))
    
    logs.append("Draft report web search completed. 🥳")
    logs.append(f"Writer node completed in {time.time() - time_start:.2f} seconds.")
    return {
        "draft_report": result.content,
        "messages": messages,
        "logs": logs,
        "next_agent": "fact_checker",
    }
    
    