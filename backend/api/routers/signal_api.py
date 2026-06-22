from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

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
        news_sentiment=graph_result.get("news_sentiment")
        financial_statement=graph_result.get("financial_statement")
        financial_ratio=graph_result.get("financial_ratio")
        ai_response = graph_result.get("ai_response")

        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content= {
                "symbol": symbol,
                "status": status.HTTP_200_OK,
                "data": {
                    "technical_signal": tech_signal,
                    "indicator_summary": indicator_summary,
                    "financial_ratio": financial_ratio,
                    "financial_statement": financial_statement,
                    "news_sentiment": news_sentiment,
                    "ai_respones": ai_response
                    
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