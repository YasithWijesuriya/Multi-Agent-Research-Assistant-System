dev.to article

🚀 Using ChatPromptTemplate with create_tool_calling_agent in LangChain (Instead of create_agent)

Why modern LangChain users prefer explicit prompts + tool-calling agents

📌 Introduction

In early LangChain versions, many developers used helper functions like create_agent() to quickly spin up agents.
However, modern LangChain workflows (especially multi-agent systems and LangGraph pipelines) benefit more from:

Explicit prompts

Clear message roles

Tool-aware agents

That’s where ChatPromptTemplate + create_tool_calling_agent from langchain_classic comes in.

This article explains why and how to use this approach instead of create_agent().

🤔 Why not just use create_agent()?

create_agent() is convenient, but it has limitations:

❌ Limited prompt customization
❌ Less control over message roles
❌ Harder to debug tool usage
❌ Not ideal for multi-agent or graph-based workflows

If you want full control, you need to build your agent explicitly.

✅ The Modern Pattern (Recommended)

The recommended approach looks like this:

LLM

- Explicit Prompt (ChatPromptTemplate)
- Tools
- Tool-calling Agent
- AgentExecutor

This gives you:

Full prompt control

Clean separation of responsibilities

Better debugging

Easier scaling to multi-agent systems

🧠 Core Components Explained
1️⃣ ChatPromptTemplate

Instead of hidden prompts, we define the full structure ourselves:

from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

Example:

prompt = ChatPromptTemplate.from_messages([
("system", "You are a research agent that gathers accurate information."),
MessagesPlaceholder(variable_name="chat_history"),
("human", "{input}"),
MessagesPlaceholder(variable_name="agent_scratchpad")
])

📌 Why this matters

You control exactly what the LLM sees

Chat history and agent reasoning are injected cleanly

Perfect for multi-step reasoning

2️⃣ Why MessagesPlaceholder is Important
Placeholder Purpose
chat_history Keeps conversation context
agent_scratchpad Stores tool calls + reasoning

Sinhala note 🇱🇰
chat_history = agent එකේ “මතකය”
agent_scratchpad = agent එකේ “notebook”

3️⃣ create_tool_calling_agent (from langchain_classic)
from langchain_classic.agents import create_tool_calling_agent

This creates an agent that:

Understands tool schemas

Decides when to call tools

Integrates tool results into reasoning

Example:

agent = create_tool_calling_agent(
llm=llm,
tools=tools,
prompt=prompt
)

📌 This is more powerful than create_agent() because:

Tool calls are explicit

The prompt is fully customizable

The agent follows a structured reasoning flow

4️⃣ AgentExecutor – Running the Agent
from langchain_classic.agents import AgentExecutor

agent_executor = AgentExecutor(
agent=agent,
tools=tools,
verbose=True
)

This:

Executes the agent loop

Handles tool calls

Manages scratchpad updates

verbose=True is extremely useful for debugging.

🧪 Full Working Example
from langchain_openai import ChatOpenAI
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

llm = ChatOpenAI(
model="gpt-4o-mini",
temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
("system", "You are a research agent specialized in web search."),
MessagesPlaceholder(variable_name="chat_history"),
("human", "{input}"),
MessagesPlaceholder(variable_name="agent_scratchpad")
])

tools = create_search_tools()

agent = create_tool_calling_agent(
llm=llm,
tools=tools,
prompt=prompt
)

agent_executor = AgentExecutor(
agent=agent,
tools=tools,
verbose=True
)

result = agent_executor.invoke({
"input": "Research AI agents in 2025",
"chat_history": []
})

print(result["output"])

🔄 Comparison: create_agent() vs Tool-Calling Agent
Feature create_agent() create_tool_calling_agent
Prompt control ❌ Limited ✅ Full
Tool visibility ❌ Hidden ✅ Explicit
Debugging ❌ Hard ✅ Easy
Multi-agent ready ❌ ✅
LangGraph friendly ❌ ✅
🧠 When Should You Use This Pattern?

✅ You are building:

Research agents

Multi-agent workflows

LangGraph pipelines

Tool-heavy AI systems

❌ You just want a quick demo or prototype

🏁 Conclusion

If you want production-ready AI agents, stop relying on create_agent().

Instead:

Define prompts explicitly with ChatPromptTemplate

Use create_tool_calling_agent from langchain_classic

Manage execution via AgentExecutor

This approach gives you clarity, control, and scalability.

✍️ Final Tip (Sinhala)

“Agent එක smart වෙන්නෙ model එක නිසා නෙමෙයි —
prompt + memory + tools එකතු වෙද්දියි.”
# Multi-agent-research-Assistant
# Multi-Agent-Research-Assistant-System
