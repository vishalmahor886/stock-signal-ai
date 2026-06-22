from typing import TypedDict

class TradingState(TypedDict):
    symbol: str
    tech_signal: dict
    indicator_summary: dict
    news_sentiment: dict
    financial_ratio: dict
    financial_statement: dict
    ai_response:dict
    


    