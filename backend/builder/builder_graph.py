from langgraph.graph import StateGraph, START, END
from backend.builder.state import TradingState
from backend.agents.technical_analysis_agent import technical_analysis_agent
from backend.agents.ai_response_agent import ai_response_agent
from backend.agents.news_sentiment_agent import news_sentiment_agent
from backend.agents.financial_statement_agent import financial_statement_agent
from backend.agents.financial_ratio_agent import financial_ratio_agent

builder = StateGraph(TradingState)

builder.add_node("technical_analysis",technical_analysis_agent)
builder.add_node("news_sentiment",news_sentiment_agent)
builder.add_node("financial_analysis", financial_statement_agent)
builder.add_node("financial_ratio", financial_ratio_agent)
builder.add_node("ai_response", ai_response_agent)


builder.add_edge(START, "technical_analysis")
builder.add_edge(START, "news_sentiment")
builder.add_edge(START, "financial_analysis")
builder.add_edge(START, "financial_ratio")

builder.add_edge("technical_analysis", "ai_response")
builder.add_edge("news_sentiment", "ai_response")
builder.add_edge("financial_analysis", "ai_response")
builder.add_edge("financial_ratio", "ai_response")

builder.add_edge("ai_response", END)
graph = builder.compile()
