from backend.services.news_service import get_news_sentiment_for_symbol
from backend.ai_models.hf_ai_model import agentic_llm
from backend.prompts.news_prompt import NEWS_PROMPT
import json

def news_sentiment_node(state:dict):
    news_sentiment={}
    try:
        symbol = state.get("symbol")
        if not symbol:
            return {"news_sentiment": news_sentiment}

        news = get_news_sentiment_for_symbol(symbol, max_result=5)
        if not news:
            return {"news_sentiment": []}

        llm_model= agentic_llm()

        prompts=NEWS_PROMPT.format(
            symbol=symbol,
            article=news
        )

        response=llm_model.invoke(prompts)

        content = response.content if hasattr(response, "content") else str(response)

        content = content.replace("```json", "").replace("```", "").strip()
        news_sentiment = json.loads(content)
        return {"news_sentiment": news_sentiment}

    except Exception as e:
        return {"news_sentiment": news_sentiment, "error":str(e)}