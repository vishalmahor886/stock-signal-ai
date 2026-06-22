from backend.builder.state import TradingState
import yfinance as yf
from backend.services.financial_statement_service import get_financial_statement_for_symbol


def financial_statement_agent(state:TradingState):
    try:
        symbol=state["symbol"]
        financial_statement=get_financial_statement_for_symbol(symbol)
        state["financial_statement"]=financial_statement
        return {"financial_statement":financial_statement}
    except Exception as e:
        return {
            "financial_statement": {
                "decision": "NA",
                "confidence": 0,
                "entry_price": 0,
                "stop_loss": 0,
                "target_price": 0,
                "holding_days": 0,
                "reasoning": f"Failed to generate financial statement {e}"
            }
        }