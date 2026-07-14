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


# =====================================================
# STATE
# =====================================================

class AgentState(TypedDict):
    action: str
    input: dict
    output: dict


# =====================================================
# ROUTER
# =====================================================

def router(state: AgentState):

    action = state["action"]

    if action == "extract":
        return "extract"

    elif action == "edit":
        return "edit"

    elif action == "search":
        return "search"

    elif action == "chat":
        return "chat"

    else:
        return "extract"


# =====================================================
# TOOL 1
# Extract Interaction
# =====================================================

def extract_node(state: AgentState):

    extracted = extract_interaction(
        state["input"]["query"]
    )

    state["output"] = extracted

    return state


# =====================================================
# TOOL 2
# Generate Summary
# =====================================================

def summary_node(state: AgentState):

    summary = summarize_interaction(
        state["output"]["discussion"]
    )

    state["output"]["summary"] = summary

    return state


# =====================================================
# TOOL 3
# Generate Followup
# =====================================================

def followup_node(state: AgentState):

    followup = suggest_followup(
        state["output"]["discussion"]
    )

    state["output"]["follow_up"] = followup

    return state


# =====================================================
# TOOL 4
# Log Interaction
# =====================================================

def log_node(state: AgentState):

    result = log_interaction(
        state["output"]
    )

    state["output"]["database"] = result

    return state


# =====================================================
# TOOL 5
# Edit Interaction
# =====================================================

def edit_node(state: AgentState):

    data = state["input"]

    result = edit_interaction(
        data["interaction_id"],
        data["updates"],
    )

    state["output"] = result

    return state


# =====================================================
# TOOL 6
# Search HCP
# =====================================================

def search_node(state: AgentState):

    result = search_hcp(
        state["input"]["hcp_name"]
    )

    state["output"] = {
        "results": result
    }

    return state


# =====================================================
# TOOL 7
# Chat Assistant
# =====================================================

def chat_node(state: AgentState):

    result = chat_assistant(
        state["input"]["query"]
    )

    state["output"] = {
        "response": result
    }

    return state


# =====================================================
# BUILD GRAPH
# =====================================================

builder = StateGraph(AgentState)

builder.add_node("extract", extract_node)
builder.add_node("summary", summary_node)
builder.add_node("followup", followup_node)
builder.add_node("log", log_node)

builder.add_node("edit", edit_node)
builder.add_node("search", search_node)
builder.add_node("chat", chat_node)


builder.set_conditional_entry_point(
    router,
    {
        "extract": "extract",
        "edit": "edit",
        "search": "search",
        "chat": "chat",
    },
)


# =====================================================
# Main AI Flow
# =====================================================

builder.add_edge("extract", "summary")
builder.add_edge("summary", "followup")
builder.add_edge("followup", "log")
builder.add_edge("log", END)


# =====================================================
# Other Tools
# =====================================================

builder.add_edge("edit", END)
builder.add_edge("search", END)
builder.add_edge("chat", END)


graph = builder.compile()