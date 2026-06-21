from typing import TypedDict

class TradingState(TypedDict):
    symbol: str
    tech_signal: dict
    indicator_summary: dict
    ai_response: dict


    