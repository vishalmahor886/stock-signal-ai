from backend.builder.state import TradingState
import yfinance as yf
from backend.services.financial_statement_service import get_financial_statement_for_symbol


def financial_statement_agent(state: TradingState):
    try:
        symbol = state["symbol"]

        financial_statement = get_financial_statement_for_symbol(symbol)

        # IMPORTANT: do NOT wrap again
        return {
            "financial_statement": financial_statement
        }

    except Exception as e:
        return {
            "financial_statement": {
                "error": str(e)
            }
        }