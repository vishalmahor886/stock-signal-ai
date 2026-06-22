import yfinance as yf
import json
def get_financial_ratio_for_symbol(symbol:str):
    try:
        yf_symbol = symbol.upper()
        if "." not in yf_symbol:
            yf_symbol = f"{yf_symbol}.NS"

        info = yf.Ticker(yf_symbol).info
        if not info:
            return {"success": False, "message": "No data found"}

        ratios = {
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "current_ratio": info.get("currentRatio"),
            "debt_to_equity": info.get("debtToEquity"),
            "profit_margin": info.get("profitMargins"),
            "operating_margin": info.get("operatingMargins"),
            "peg_ratio": info.get("pegRatio"),
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "price_to_book": info.get("priceToBook")
        }

        return ratios
    except Exception as e:
        return {
            "error": str(e)
        }