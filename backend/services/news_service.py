from ddgs import DDGS
from backend.services.remove_duplicate_articles import remove_duplicates


def get_news_sentiment_for_symbol(symbol:str, max_result:int = 5):
    query=f"{symbol} stock news"
    articles=[]

    with DDGS() as ddgs:
        results = ddgs.news(query=query,max_results=max_result)
    
    for item in results:
        articles.append({
            "title": item.get("title"),
            "summary": item.get("summary"),
            "url":item.get("url"),
            "date":item.get("date"),
            "source":item.get("source")
        })
    return remove_duplicates(articles)
