import time
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent,AgentExecutor
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from tools.search_tools import create_search_tools
from langchain_core.messages import AIMessage



def create_researcher_agent():
    """Web search කරල information gather කරන agent එක"""
    
    # LLM model එක initialize කරනවා
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Cost-effective model
        temperature=0.3  # Creative නෙමෙයි, factual වියයුතු
    )
    
    # Agent එකේ prompt එක define කරනවා
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Research Agent specialized in gathering information.
        
        Your job:
        1. Take the research topic and search the web thoroughly
        2. Find 5-10 reliable sources with recent information
        3. Extract key facts, statistics, and important details
        4. Organize findings in a clear, structured format
        
        Be thorough but concise. Focus on credible sources."""),
        
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
                #add current user input for the prompt
        MessagesPlaceholder(variable_name="agent_scratchpad") 
                #agent_scratchpad = Agentගේ private thinking + tool usage memory

    ])
    
    # Tools එක්ක agent එක හදනවා
    tools = create_search_tools()
    agent = create_tool_calling_agent(
            llm=llm,
            tools=tools,
            prompt=prompt
            )
    return agent, tools

def researcher_node(state):
    logs = state.get("logs", [])
    logs.append("Researcher node started.")
    start_time = time.time()

    print("🔹 RESEARCHER NODE STATE KEYS:", state.keys())
    """Graph node function - state update කරනවා"""    
    agent, tools = create_researcher_agent() 

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True
        )
    

    result = agent_executor.invoke({
        "input": f"Research this topic thoroughly: {state['topic']}",
        "chat_history": state.get("messages", [])
    })
    
    end_time = time.time()
    duration = end_time - start_time

    logs.append("Researcher finished web search.🥳")
    logs.append(f"Research duration: {duration:.2f} seconds.") 
    research_message = AIMessage(
        content=result["output"],#මේක agent executor return කරන dictionary එකේ key එකේ නම.
#?        result = {
#?             "output": "AI in healthcare is growing rapidly. 70% of hospitals adopt AI."
#?       }

        name="researcher"  # Optional: agent name track කරන්න
    )

    messages = state.get("messages", [])
    #!👉 state කියන්නේ dictionary එකක්
        # state.get("messages", []) කියන්නේ?
        # state තුළ "messages" key එක තියෙනවා නම් → 
        # ඒ value එක ගන්නවා
        # "messages" key එක නැත්තම් → [] (empty list) use කරනවා

        # 📌 ඒක safe way එක:
            #? messages = state["messages"]  ->  crash වෙන්න පුළුවන්
        # වෙනුවට:
            #? messages = state.get("messages", [])

    messages.append(research_message)
         # messages list එකට අලුත් message එක add කරනවා

#! Before append:
    #?     messages = [
    #?         AIMessage(content="Hi", name="user")
    #?     ]
#! After append: 
    #?     messages = [
    #?    AIMessage(content="Hi", name="user"),
    #?     AIMessage(content="AI in healthcare is growing fast...", name="researcher")
    #? ]


    return {
    **state,
    "research_data": state.get("research_data", []) + [result["output"]],
        #*state.get("research_data", [])
            #state තුළ "research_data" තියෙනවා නම් → ඒ list එක ගන්නවා
            #නැත්නම් → [] (empty list)

        #*[result["output"]]
            #result["output"] → agent එක generate කළ new research text 
    
    "logs": logs,
    "messages": messages,
    "next_agent": "analyst"
}

# **state මේක කියන්නේ:
            # “state එකේ තියෙන
            # topic, research_data, analysis…
            # ඔක්කොම තියාගෙන
            # messages key එක update කරන්න”
            #!පරණ state එකේ තියෙන හැම key එකක්ම copy කරනවා