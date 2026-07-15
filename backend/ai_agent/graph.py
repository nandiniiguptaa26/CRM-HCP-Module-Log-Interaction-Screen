from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from ai_agent.tools import (
    extract_interaction,
    log_interaction,
    edit_interaction,
    search_hcp,
    summarize_interaction,
    suggest_followup,
    chat_assistant,
    validate_interaction,
)


# =====================================================
# STATE
# =====================================================

class AgentState(TypedDict):
    action: str
    input: dict
    output: dict
    history: list
    errors: list


# =====================================================
# ROUTER
# =====================================================

def router(state: AgentState):

    action = state.get("action", "").lower()

    routes = {
        "extract": "extract",
        "edit": "edit",
        "search": "search",
        "chat": "chat",
        "log": "extract",
    }

    return routes.get(action, "extract")


# =====================================================
# TOOL 1
# Extract Interaction
# =====================================================

def extract_node(state: AgentState):

    query = state["input"].get("query", "")

    extracted = extract_interaction(query)

    state["output"] = extracted
    state["errors"] = []

    return state


# =====================================================
# VALIDATION NODE
# =====================================================

def validate_node(state: AgentState):

    result = validate_interaction(state["output"])

    if result["status"] == "error":

        state["errors"] = result["errors"]

        state["output"] = {
            "status": "error",
            "message": "Validation Failed",
            "errors": result["errors"]
        }

        return state

    return state


# =====================================================
# SEARCH HISTORY NODE
# =====================================================

def history_node(state: AgentState):

    doctor = state["output"].get("hcp_name", "")

    if doctor:

        history = search_hcp(doctor)

    else:

        history = []

    state["history"] = history

    return state


# =====================================================
# SUMMARY NODE
# =====================================================

def summary_node(state: AgentState):

    if state.get("errors"):

        return state

    discussion = state["output"].get("discussion", "")

    history = state.get("history", [])

    summary = summarize_interaction(
        discussion,
        history
    )

    state["output"]["summary"] = summary

    return state


# =====================================================
# FOLLOWUP NODE
# =====================================================

def followup_node(state: AgentState):

    if state.get("errors"):

        return state

    discussion = state["output"].get("discussion", "")

    history = state.get("history", [])

    followup = suggest_followup(
        discussion,
        history
    )

    state["output"]["follow_up"] = followup

    return state


# =====================================================
# LOG NODE
# =====================================================

def log_node(state: AgentState):

    if state.get("errors"):

        return state

    result = log_interaction(state["output"])

    state["output"]["database"] = result

    return state


# =====================================================
# EDIT NODE
# =====================================================

def edit_node(state: AgentState):

    data = state["input"]

    result = edit_interaction(
        data.get("interaction_id"),
        data.get("updates", {})
    )

    state["output"] = result

    return state


# =====================================================
# SEARCH NODE
# =====================================================

def search_node(state: AgentState):

    doctor = state["input"].get("hcp_name", "")

    results = search_hcp(doctor)

    state["output"] = {
        "results": results
    }

    return state


# =====================================================
# CHAT NODE
# =====================================================

def chat_node(state: AgentState):

    query = state["input"].get("query", "")

    response = chat_assistant(query)

    state["output"] = {
        "response": response
    }

    return state
# =====================================================
# BUILD GRAPH
# =====================================================

builder = StateGraph(AgentState)

# Core Nodes
builder.add_node("extract", extract_node)
builder.add_node("validate", validate_node)
builder.add_node("history", history_node)
builder.add_node("summary", summary_node)
builder.add_node("followup", followup_node)
builder.add_node("log", log_node)

# Utility Nodes
builder.add_node("edit", edit_node)
builder.add_node("search", search_node)
builder.add_node("chat", chat_node)


# =====================================================
# ENTRY ROUTING
# =====================================================

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
# MAIN CRM AI FLOW
# =====================================================

builder.add_edge("extract", "validate")
builder.add_edge("validate", "history")
builder.add_edge("history", "summary")
builder.add_edge("summary", "followup")
builder.add_edge("followup", "log")
builder.add_edge("log", END)


# =====================================================
# OTHER FLOWS
# =====================================================

builder.add_edge("edit", END)
builder.add_edge("search", END)
builder.add_edge("chat", END)


# =====================================================
# COMPILE GRAPH
# =====================================================

graph = builder.compile()