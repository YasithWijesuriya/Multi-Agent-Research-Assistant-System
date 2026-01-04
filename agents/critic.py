import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import AIMessage

def create_critic_agent():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Critic Agent specialized in quality review.

Your job:
1. Review the draft report critically
2. Check for clarity, accuracy, and completeness
3. Decide if report needs revision or is ready
Respond ONLY with:
- APPROVE
- or REVISE: <feedback>
"""),
        ("human", "Draft Report:\n{draft_report}")
    ])
    
    return prompt | llm


def critic_node(state):
    logs = state.get("logs", [])
    logs.append("Critic node started.")
    time_start = time.time()
    print("🔍 CRITIC STATE KEYS:", state.keys())  
    
    chain = create_critic_agent()
    result = chain.invoke({"draft_report": state["draft_report"]})

    feedback = result.content.strip()

    messages = state.get("messages", [])
    messages.append(AIMessage(
        content=feedback, 
        name="critic"))

    # ✅ APPROVE
    if "APPROVE" in feedback.upper():
        return {
            **state,
            "final_report": state["draft_report"],
            "messages": messages,
            "next_agent": "end"
        }

    # 🔁 REVISE
    iterations = state.get("iterations", 0) + 1

    if iterations < 2:
        return {
            **state,
            "iterations": iterations,
            "messages": messages,
            "next_agent": "writer"
        }

    logs.append("Max revisions reached. Approving draft.🥳")
    logs.append(f"Critic node completed in {time.time() - time_start:.2f} seconds.")
    return {
        **state,
        "final_report": state["draft_report"],
        "messages": messages,
        "logs": logs,
        "next_agent": "end"
    }
