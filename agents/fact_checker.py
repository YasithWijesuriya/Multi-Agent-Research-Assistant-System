import time
from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.messages import AIMessage

def create_fact_checker_agent():

    llm= ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2 # Low temperature for factual accuracy
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system","""You are a Fact-Checking Agent specialized in verifying information.
         your job:
         1. Review the draft report provided
         2. Cross-check facts, statistics, and claims against reliable sources
         3. Highlight inaccuracies or unsupported claims
            Respond ONLY with:
            - APPROVE if all facts are correct
            - or CORRECT: <list corrections>"""),
        ("human", "Draft Report:\n{draft_report}")
    ])

    return prompt | llm

MAX_ITERATIONS = 3  # maximum writer↔fact-checker revisions

def fact_checker_node(state):
    logs = state.get("logs", [])
    logs.append("Fact-Checker node started.")
    start_time = time.time()

    print("🔹 FACT-CHECKER NODE STATE KEYS:", state.keys())
    
    chain = create_fact_checker_agent()
    result = chain.invoke({
        "draft_report": state["draft_report"]
    })

    feedback = result.content.strip()
    messages = state.get("messages", [])
    messages.append(AIMessage(
        content=feedback,
        name="fact_checker"))

    iterations = state.get("iterations", 0)

    if "APPROVE" in feedback.upper():
        logs.append("Fact-Checking completed. All facts approved. ✅")
        logs.append(f"Fact-Checker node completed in {time.time() - start_time:.2f} seconds.")
        return {
            **state,
            "final_report": state["draft_report"],
            "messages": messages,
            "logs": logs,
            "next_agent": "critic"  # move forward
        }
    else:
        iterations += 1
        logs.append(f"Corrections needed. Iteration {iterations}/{MAX_ITERATIONS}.")

        # If max iterations reached, move on to critic
        next_agent = "writer" if iterations < MAX_ITERATIONS else "critic"

        corrected_report = state["draft_report"] + "\n\nCorrections:\n" + feedback

        return {
            **state,
            "draft_report": corrected_report,
            "messages": messages,
            "logs": logs,
            "iterations": iterations,
            "next_agent": next_agent
        }
