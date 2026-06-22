from backend.builder.state import TradingState
from backend.services.financial_ratio_service import get_financial_ratio_for_symbol

def financial_ratio_agent(state:TradingState):
    try:
        symbol=state["symbol"]
        financial_ratio=get_financial_ratio_for_symbol(symbol)
        state["financial_ratio"]=financial_ratio
        return {"financial_ratio":financial_ratio}
    except Exception as e:
        return {
            "financial_ratio": {},
            "error": str(e)
        }