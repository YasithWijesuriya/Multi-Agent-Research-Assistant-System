import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import AIMessage

def create_analyst_agent():
    """Research data analyze කරන agent එක"""
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5  # Bit more creative for analysis
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an Analysis Agent specialized in extracting insights.
        
        Your job:
        1. Review the research data provided
        2. Identify key patterns, trends, and insights
        3. Synthesize information from multiple sources
        4. Highlight important takeaways and implications
        5. Organize analysis in a logical structure
        
        Be analytical and objective."""),
        
        ("human", """Research Data:
{research_data}

Please analyze this research and provide key insights.""")
    ])
    
    chain = prompt | llm
    return chain



def analyst_node(state):
    logs= state.get("logs", [])
    logs.append("Analyst node started.")
    start_time = time.time()

    print("🔹 ANALYST NODE STATE KEYS:", state.keys())
    """Analysis කරල state update කරනවා"""
    
    chain = create_analyst_agent()
    
    # Research data එක string එකක් කරනවා
    research_text = "\n\n".join(state["research_data"])

    # Analysis කරනවා
    result = chain.invoke({"research_data": research_text})


    
    messages = state.get("messages", [])
    messages.append(AIMessage(
        content=result.content,
        name="analyst"))
    
    logs.append("Analysis web search completed. 🥳")
    logs.append(f"Analyst node completed in {time.time() - start_time:.2f} seconds.")
    return {
        **state,
        "analysis": result.content,
        "messages": messages,
        "logs": logs,
        "next_agent": "writer"
    }


    #! හිතන්න ඔබ පර්යේෂකයෙක් කියලා.

        # ඔබේ මතකයේ (state) තොරතුරු ගොඩක් තියෙනවා.
        # ඔබ ඒ තොරතුරු කොළයක ලස්සනට ලියාගන්නවා (join).
        # ඊටපස්සේ ඔබ ඒක කියවලා වැදගත් කරුණු ටිකක් හිතාගන්නවා (invoke).
        # අන්තිමට ඔබ ඒ වැදගත් කරුණු ටික තව කෙනෙක්ට දීලා කියනවා "දැන් මේක ඇසුරෙන් ලිපියක් ලියන්න" (next_agent: writer) කියලා.

        # ("analyst", result.content) මගින් කරන්නේ "මෙය විශ්ලේෂක (analyst) විසින් ලබාදුන් පිළිතුරකි" යන ලේබලය සමඟ AI එකේ පිළිතුර පද්ධතියේ මතකයට (messages list එකට) එකතු කිරීමයි.