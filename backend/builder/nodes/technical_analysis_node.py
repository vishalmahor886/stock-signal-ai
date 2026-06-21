from backend.builder.state import TradingState
from backend.services.signal_generator import generate_signal_for_symbol 
from backend.services.indicators import get_latest_summary
import yfinance as yf


def technical_analysis_node(state:TradingState):
    symbol=state["symbol"]
    yf_symbol = symbol if "." in symbol else f"{symbol}.NS"
    df = yf.Ticker(yf_symbol).history(period="1y")
    df.reset_index(inplace=True)
    state["tech_signal"]=generate_signal_for_symbol(symbol,df)  
    state["indicator_summary"]=get_latest_summary(df)   
    
    return {
        "tech_signal":state["tech_signal"],
        "indicator_summary":state["indicator_summary"]
    }
