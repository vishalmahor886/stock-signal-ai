from langgraph.graph import StateGraph, START, END
from backend.builder.state import TradingState
from backend.builder.nodes.technical_analysis_node import technical_analysis_node
from backend.builder.nodes.ai_response_node import ai_response_node
from backend.builder.nodes.news_sentiment_node import news_sentiment_node

builder = StateGraph(TradingState)

builder.add_node("technical_analysis",technical_analysis_node)
builder.add_node("ai_response",ai_response_node)
builder.add_node("news_sentiment",news_sentiment_node)

builder.add_edge(START, "technical_analysis")
builder.add_edge("technical_analysis", "ai_response")
builder.add_edge("ai_response", "news_sentiment")
builder.add_edge("news_sentiment", END)

graph = builder.compile()
