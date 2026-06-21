from langgraph.graph import StateGraph, START, END
from backend.builder.state import TradingState
from backend.builder.nodes.technical_analysis_node import technical_analysis_node
from backend.builder.nodes.ai_response_node import ai_response_node

builder = StateGraph(TradingState)

builder.add_node("technical_analysis",technical_analysis_node)
builder.add_node("ai_response",ai_response_node)

builder.add_edge(START, "technical_analysis")
builder.add_edge("technical_analysis","ai_response")
builder.add_edge("ai_response",END)

graph = builder.compile()
