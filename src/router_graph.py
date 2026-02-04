from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END

from .rag_agent import get_rag_answer
from .coding_agents import solve_with_retry


# -----------------------------
# State definition
# -----------------------------
class AgentState(TypedDict):
    question: str
    route: Literal["rag", "code"]
    answer: str


# -----------------------------
# Keyword-based routing
# -----------------------------
HR_KEYWORDS = [
    "policy", "leave", "time off", "vacation", "benefits",
    "hr", "notice", "separation", "travel", "office"
]

CODE_KEYWORDS = [
    "python", "code", "calculate", "fibonacci",
    "prime", "algorithm", "compute", "square root"
]


# -----------------------------
# Router node
# -----------------------------
def route_node(state: AgentState) -> AgentState:
    q = state["question"].lower()

    if any(k in q for k in CODE_KEYWORDS):
        state["route"] = "code"
    elif any(k in q for k in HR_KEYWORDS):
        state["route"] = "rag"
    else:
        # default to RAG for company-related questions
        state["route"] = "rag"

    return state


# -----------------------------
# RAG node
# -----------------------------
def rag_node(state: AgentState) -> AgentState:
    state["answer"] = get_rag_answer(state["question"])
    return state


# -----------------------------
# Coding node
# -----------------------------
def code_node(state: AgentState) -> AgentState:
    state["answer"] = solve_with_retry(state["question"])
    return state



# -----------------------------
# Build LangGraph
# -----------------------------
def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("route", route_node)
    graph.add_node("rag", rag_node)
    graph.add_node("code", code_node)

    graph.set_entry_point("route")

    graph.add_conditional_edges(
        "route",
        lambda state: state["route"],
        {
            "rag": "rag",
            "code": "code",
        }
    )

    graph.add_edge("rag", END)
    graph.add_edge("code", END)

    return graph.compile()
