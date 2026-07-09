from typing import TypedDict

from langgraph.graph import StateGraph, END

from ai_agent.tools import (
    extract_interaction,
    log_interaction,
    edit_interaction,
    search_hcp,
    summarize_interaction,
    suggest_followup,
    chat_assistant,
)

# ============================================================
# STATE
# ============================================================

class AgentState(TypedDict):
    action: str
    input: dict
    output: dict


# ============================================================
# ROUTER
# ============================================================

def router(state: AgentState):

    action = state["action"]

    if action == "extract":
        return "extract"

    elif action == "log":
        return "log"

    elif action == "edit":
        return "edit"

    elif action == "search":
        return "search"

    elif action == "summary":
        return "summary"

    elif action == "followup":
        return "followup"

    else:
        return "chat"


# ============================================================
# EXTRACT NODE (NEW)
# ============================================================

def extract_node(state: AgentState):

    result = extract_interaction(
        state["input"]["query"]
    )

    state["output"] = result

    return state


# ============================================================
# LOG NODE
# ============================================================

def log_node(state: AgentState):

    result = log_interaction(
        state["input"]
    )

    state["output"] = result

    return state


# ============================================================
# EDIT NODE
# ============================================================

def edit_node(state: AgentState):

    data = state["input"]

    result = edit_interaction(
        data["interaction_id"],
        data["updates"]
    )

    state["output"] = result

    return state


# ============================================================
# SEARCH NODE
# ============================================================

def search_node(state: AgentState):

    result = search_hcp(
        state["input"]["hcp_name"]
    )

    state["output"] = result

    return state


# ============================================================
# SUMMARY NODE
# ============================================================

def summary_node(state: AgentState):

    result = summarize_interaction(
        state["input"]["discussion"]
    )

    state["output"] = {
        "summary": result
    }

    return state


# ============================================================
# FOLLOWUP NODE
# ============================================================

def followup_node(state: AgentState):

    result = suggest_followup(
        state["input"]["discussion"]
    )

    state["output"] = {
        "follow_up": result
    }

    return state


# ============================================================
# CHAT NODE
# ============================================================

def chat_node(state: AgentState):

    result = chat_assistant(
        state["input"]["query"]
    )

    state["output"] = {
        "response": result
    }

    return state


# ============================================================
# BUILD GRAPH
# ============================================================

builder = StateGraph(AgentState)

builder.add_node("extract", extract_node)
builder.add_node("log", log_node)
builder.add_node("edit", edit_node)
builder.add_node("search", search_node)
builder.add_node("summary", summary_node)
builder.add_node("followup", followup_node)
builder.add_node("chat", chat_node)

builder.set_conditional_entry_point(
    router,
    {
        "extract": "extract",
        "log": "log",
        "edit": "edit",
        "search": "search",
        "summary": "summary",
        "followup": "followup",
        "chat": "chat",
    },
)

builder.add_edge("extract", END)
builder.add_edge("log", END)
builder.add_edge("edit", END)
builder.add_edge("search", END)
builder.add_edge("summary", END)
builder.add_edge("followup", END)
builder.add_edge("chat", END)

graph = builder.compile()