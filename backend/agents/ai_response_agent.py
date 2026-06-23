from backend.builder.state import TradingState
from backend.prompts.ai_analysis_prompt import ANALYSIS_PROMPT
from backend.ai_models.hf_ai_model import agentic_llm
import json
import re


def extract_json(content: str):
    """
    Safely extract JSON from LLM output
    """
    if not content:
        raise ValueError("Empty LLM response")

    # Remove markdown fences first
    content = content.replace("```json", "").replace("```", "").strip()

    # Try direct parse
    try:
        return json.loads(content)
    except:
        pass

    # Extract JSON block using regex
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON found in response: {content}")

    return json.loads(match.group(0))


def ai_response_agent(state: TradingState):
    try:
        tech_signal = state.get("tech_signal", {})
        indicator_summary = state.get("indicator_summary", {})
        news_sentiment = state.get("news_sentiment", {})
        financial_statement = state.get("financial_statement", {})
        financial_ratio = state.get("financial_ratio", {})
        symbol = state.get("symbol")

        if not tech_signal or not indicator_summary:
            return {"ai_response": f"Insufficient data for {symbol}"}

        # Format indicators
        signal_text = "\n".join([f"- {k}: {v}" for k, v in tech_signal.items()])

        news_text = json.dumps(news_sentiment, indent=2, default=str)
        financial_text = json.dumps(financial_statement, indent=2, default=str)
        ratio_text = json.dumps(financial_ratio, indent=2, default=str)

        prompt = ANALYSIS_PROMPT.format(
            symbol=symbol,

            open=tech_signal.get("current_price", "Unknown"),
            high=tech_signal.get("high_52w", "Unknown"),
            low=tech_signal.get("low_52w", "Unknown"),
            close=tech_signal.get("close", "Unknown"),
            volume=tech_signal.get("volume", "Unknown"),

            sma_20=indicator_summary.get("trend", {}).get("sma_20", "-"),
            sma_50=indicator_summary.get("trend", {}).get("sma_50", "-"),
            sma_200=indicator_summary.get("trend", {}).get("sma_200", "-"),

            ema_12=indicator_summary.get("trend", {}).get("ema_12", "-"),
            ema_26=indicator_summary.get("trend", {}).get("ema_26", "-"),

            macd_line=indicator_summary.get("trend", {}).get("macd_line", "-"),
            macd_signal=indicator_summary.get("trend", {}).get("macd_signal", "-"),
            macd_histogram=indicator_summary.get("trend", {}).get("macd_histogram", "-"),

            supertrend_direction=indicator_summary.get("trend", {}).get("supertrend_direction", "-"),

            rsi=indicator_summary.get("momentum", {}).get("rsi_14", "-"),
            stoch_rsi_k=indicator_summary.get("momentum", {}).get("stoch_rsi_k", "-"),
            stoch_rsi_d=indicator_summary.get("momentum", {}).get("stoch_rsi_d", "-"),
            williams_r=indicator_summary.get("momentum", {}).get("williams_r", "-"),

            bb_upper=indicator_summary.get("volatility", {}).get("bb_upper", "-"),
            bb_middle=indicator_summary.get("volatility", {}).get("bb_middle", "-"),
            bb_lower=indicator_summary.get("volatility", {}).get("bb_lower", "-"),

            bb_width=indicator_summary.get("volatility", {}).get("bb_width", "-"),
            bb_percent=indicator_summary.get("volatility", {}).get("bb_percent", "-"),

            atr=indicator_summary.get("volatility", {}).get("atr_14", "-"),

            obv=indicator_summary.get("volume", {}).get("obv", "-"),
            vwap=indicator_summary.get("volume", {}).get("vwap", "-"),

            pivot=indicator_summary.get("levels", {}).get("pivot", "-"),
            r1=indicator_summary.get("levels", {}).get("r1", "-"),
            r2=indicator_summary.get("levels", {}).get("r2", "-"),
            r3=indicator_summary.get("levels", {}).get("r3", "-"),
            s1=indicator_summary.get("levels", {}).get("s1", "-"),
            s2=indicator_summary.get("levels", {}).get("s2", "-"),
            s3=indicator_summary.get("levels", {}).get("s3", "-"),

            tech_signal=signal_text,
            tech_score=tech_signal.get("composite_score", "-"),
            tech_confidence=tech_signal.get("confidence", "-"),
            tech_reasoning=tech_signal.get("reasoning", "-"),

            recent_candles="No recent candle data available",

            news_text=news_text,
            financial_text=financial_text,
            ratio_text=ratio_text
        )

        llm = agentic_llm()
        ai_signal = llm.invoke(prompt)

        print("RAW LLM OUTPUT:\n", ai_signal.content)

        ai_response = extract_json(ai_signal.content)

        return {"ai_response": ai_response}

    except Exception as e:
        return {
            "ai_response": {
                "decision": "NA",
                "confidence": 0,
                "score": 0,
                "entry_price": 0,
                "stop_loss": 0,
                "target_price": 0,
                "risk_reward": 0,
                "holding_days": 0,
                "technical_score": 0,
                "fundamental_score": 0,
                "sentiment_score": 0,
                "reasoning": f"Failed: {str(e)}"
            }
        }