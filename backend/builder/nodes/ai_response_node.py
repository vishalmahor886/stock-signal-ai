from backend.builder.state import TradingState
from backend.prompts.analysis_prompt import ANALYSIS_PROMPT
from backend.ai_models.hf_ai_model import agentic_llm 
import json

def ai_response_node(state:TradingState):
    try:
        tech_signal=state.get("tech_signal",{})
        indicator_summary=state.get("indicator_summary",{})
        symbol=state["symbol"]

        #check if we have the required data
        if not tech_signal or not indicator_summary:
            return {
                "ai_response":f"Insufficient data for {symbol}"
            }
        indicators_text = ""
        for indicator, value in indicator_summary.items():
            indicators_text += f"- {indicator}: {value}\n"

        # Format technical signal
        signal_text = "\n".join([f"- {key}: {value}" for key, value in tech_signal.items()])

        # Format recent candles (optional - can be added if available)
        recent_candles = "No recent candle data available"

        open_price = tech_signal.get("current_price")
        high_price = tech_signal.get("high_52w")
        low_price = tech_signal.get("low_52w")
        close_price = tech_signal.get("close")
        volume = tech_signal.get("volume", "Unknown")

        # Construct the analysis prompt
        prompt = ANALYSIS_PROMPT.format(
            symbol=symbol,
            open=open_price if open_price is not None else "Unknown",
            high=high_price if high_price is not None else "Unknown",
            low=low_price if low_price is not None else "Unknown",
            close=close_price if close_price is not None else "Unknown",
            volume=volume,
            sma_20=indicator_summary.get("trend",{}).get("sma_20", "-"),
            sma_50=indicator_summary.get("trend",{}).get("sma_50", "-"),
            sma_200=indicator_summary.get("trend",{}).get("sma_200", "-"),
            ema_12=indicator_summary.get("trend",{}).get("ema_12", "-"),
            ema_26=indicator_summary.get("trend",{}).get("ema_26", "-"),
            macd_line=indicator_summary.get("trend",{}).get("macd_line", "-"),
            macd_signal=indicator_summary.get("trend",{}).get("macd_signal", "-"),
            macd_histogram=indicator_summary.get("trend",{}).get("macd_histogram", "-"),
            supertrend_direction=indicator_summary.get("trend",{}).get("supertrend_direction", "-"),
            rsi=indicator_summary.get("momentum",{}).get("rsi_14", "-"),
            stoch_rsi_k=indicator_summary.get("momentum",{}).get("stoch_rsi_k", "-"),
            stoch_rsi_d=indicator_summary.get("momentum",{}).get("stoch_rsi_d", "-"),
            williams_r=indicator_summary.get("momentum",{}).get("williams_r", "-"),
            bb_upper=indicator_summary.get("volatility",{}).get("bb_upper", "-"),
            bb_middle=indicator_summary.get("volatility",{}).get("bb_middle", "-"),
            bb_lower=indicator_summary.get("volatility",{}).get("bb_lower", "-"),
            bb_width=indicator_summary.get("volatility",{}).get("bb_width", "-"),
            bb_percent=indicator_summary.get("volatility",{}).get("bb_percent", "-"),
            atr=indicator_summary.get("volatility",{}).get("atr_14", "-"),
            obv=indicator_summary.get("volume",{}).get("obv", "-"),
            vwap=indicator_summary.get("volume",{}).get("vwap", "-"),
            pivot=indicator_summary.get("levels",{}).get("pivot", "-"),
            r1=indicator_summary.get("levels",{}).get("r1", "-"),
            r2=indicator_summary.get("levels",{}).get("r2", "-"),
            r3=indicator_summary.get("levels",{}).get("r3", "-"),
            s1=indicator_summary.get("levels",{}).get("s1", "-"),
            s2=indicator_summary.get("levels",{}).get("s2", "-"),
            s3=indicator_summary.get("levels",{}).get("s3", "-"),
            tech_signal=signal_text,
            tech_score=tech_signal.get("composite_score", "-"),
            tech_confidence=tech_signal.get("confidence", "-"),
            tech_reasoning=tech_signal.get("reasoning", "-"),
            recent_candles=recent_candles
        )

        llm = agentic_llm()
        ai_signal = llm.invoke(prompt)
        ai_response = json.loads(ai_signal.content.strip().replace("```json","").replace("```",""))
        return {"ai_response": ai_response}
    except Exception as e:
        return {
            "ai_response": {
                "decision": "NA",
                "confidence": 0,
                "entry_price": 0,
                "stop_loss": 0,
                "target_price": 0,
                "holding_days": 0,
                "reasoning": f"Failed to generate AI response {e}"
            }
        }