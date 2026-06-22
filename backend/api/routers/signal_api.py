from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import yfinance as yf

from backend.services.indicators import get_latest_summary
from backend.services.signal_generator import generate_signal_for_symbol 
from backend.agents.financial_statement_agent import financial_statement_agent
from backend.builder.builder_graph import graph



router = APIRouter()

@router.get("/{symbol}")
def get_signal(symbol:str):
    """
    On-demand signal generation for a specific symbol.
    """

    try:
        ## Technical Signal

        graph_result=graph.invoke({"symbol":symbol})
        tech_signal=graph_result.get("tech_signal")
        indicator_summary=graph_result.get("indicator_summary")
       # technical_analysis_ai_response=graph_result.get("ai_response")
        news_sentiment=graph_result.get("news_sentiment")
        financial_statement=graph_result.get("financial_statement")

        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {
                "symbol": symbol,
                "status": status.HTTP_200_OK,
                "data": {
                    "technical_signal": tech_signal,
                    "indicator_summary": indicator_summary,
                    #"ai_response": technical_analysis_ai_response,
                    "financial_statement": financial_statement,
                    "news_sentiment": news_sentiment,
                    
                },  
            },
            media_type="application/json"
        )
    except HTTPException as e:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "symbol": symbol,
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Insufficient data for symbol",
            },
            media_type="application/json"
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "symbol": symbol,
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            },
            media_type="application/json"
        )