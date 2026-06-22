from pydantic import BaseModel
from typing import TypedDict,List


class NewsArticle(BaseModel):
    title:str
    #url:str
    #date:str
    description: str
    #source: str
    


class NewsAnalysisResponse(BaseModel):
    symbol: str
    sentiment: str
    score: float
    summary: str
    bullish_factors: List[str]
    bearish_factors: List[str]
    impact: str