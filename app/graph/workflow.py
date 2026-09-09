from langgraph.graph import StateGraph, START, END
from app.graph.state import State
from app.graph.nodes import (
    summarizing_node,
    explanation_node,
    translation_node,
    podcast_node,
    router
)
workflow = StateGraph(State)
workflow.add_node("summarize", summarizing_node)
workflow.add_node("explain", explanation_node)
workflow.add_node("translate", translation_node)
workflow.add_node("podcast", podcast_node)
workflow.add_conditional_edges(
    START,
    router,
    {
        "summarize": "summarize",
        "explain": "explain",
        "translate": "translate",
        "podcast": "podcast"
    }
)
workflow.add_edge("summarize", END)
workflow.add_edge("explain", END)
workflow.add_edge("translate", END)
workflow.add_edge("podcast", END)
app = workflow.compile()