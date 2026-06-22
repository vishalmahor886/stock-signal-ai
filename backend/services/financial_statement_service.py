import yfinance as yf
import pandas as pd
import numpy as np
import json

def get_financial_statement_for_symbol(symbol: str):
    try:
        yf_symbol = symbol.upper()
        if "." not in yf_symbol:
            yf_symbol = f"{yf_symbol}.NS"

        df = yf.Ticker(yf_symbol).financials

        if df.empty:
            return {"success": False, "message": "No data found"}

        df = (df / 1e7).round(2)

        # Convert column names to strings
        df.columns = [str(col.date()) for col in df.columns]

        # Replace NaN, inf, -inf
        df = df.replace([np.inf, -np.inf], np.nan)

        # Convert through JSON to remove all NaN safely
        financial_statement = json.loads(
            df.to_json(orient="index")
        )

        return financial_statement
    except Exception as e:
        return {
            "error": str(e)
        }