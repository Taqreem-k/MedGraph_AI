from langgraph.graph import StateGraph, START, END
from .state import MedGraphState
from .nodes import vision_extraction_node, timeline_structuring_node

def route_after_extraction(state: MedGraphState) -> str:
    if state.get("status") == "failed":
        return END
    return "structure_timeline"

# 1. Initialize the StateGraph using your strict TypedDict
workflow = StateGraph(MedGraphState)

# 2. Add the Lego blocks (Nodes) to the graph
workflow.add_node("vision_extractor", vision_extraction_node)
workflow.add_node("structure_timeline", timeline_structuring_node)

# 3. Define the pipeline (Edges)
workflow.add_edge(START, "vision_extractor")

# Add conditional routing to catch any API or vision errors safely
workflow.add_conditional_edges(
    "vision_extractor",
    route_after_extraction,
    {
        "structure_timeline": "structure_timeline",
        END: END
    }
)

# Once structuring is complete, the graph finishes execution
workflow.add_edge("structure_timeline", END)

# 4. Compile the graph into an executable object
compiled_graph = workflow.compile()