from langgraph.graph import StateGraph, END
from .chat_state import ClinicalChatState
from .chat_nodes import retrieval_node, drafter_node, guardrail_node

# Initialize the StateGraph with our specialized Chat State
graph_builder = StateGraph(ClinicalChatState)

# 1. Add the nodes to the graph
graph_builder.add_node("retrieve", retrieval_node)
graph_builder.add_node("draft", drafter_node)
graph_builder.add_node("evaluate", guardrail_node)

# 2. Define the execution flow (The Edges)
# Start by pulling the patient's verified timeline from SQLite/FAISS
graph_builder.set_entry_point("retrieve")

# Pass the retrieved context to the Clinical Assistant to draft a response
graph_builder.add_edge("retrieve", "draft")

# Intercept the draft and force it through the Chief Medical Officer Evaluator
graph_builder.add_edge("draft", "evaluate")

# Once evaluated (whether PASSED or FAILED), end the chain so the UI can render it
graph_builder.add_edge("evaluate", END)

# Compile the graph into a runnable application
chat_graph = graph_builder.compile()