from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
from backend.builder.builder_graph import graph
router = APIRouter()

@router.get("/{symbol}")
async def get_news(symbol: str, limit: int = 10):
    """
    Fetch latest news for a given symbol
    """
    try:

        result = graph.invoke({
            "symbol":symbol
        })

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "symbol": symbol,
                "status": status.HTTP_200_OK,
                "data": {
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





    
        