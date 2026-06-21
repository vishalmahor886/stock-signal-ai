"""
Signal Generator
Produces BUY / SELL / HOLD signals from technical indicator values
using a weighted multi-indicator scoring system.
"""

from __future__ import annotations

import pandas as pd
from backend.services.indicators import compute_all


# =====================================================
# INDICATOR SCORING FUNCTIONS
# Each returns a score from -1.0 (strong sell) to +1.0 (strong buy)
# =====================================================

def _score_rsi(rsi_val: float) -> float:
    """RSI scoring: oversold = buy, overbought = sell."""
    if pd.isna(rsi_val):
        return 0.0
    if rsi_val < 30:
        return 1.0  # Oversold — strong buy
    elif rsi_val < 40:
        return 0.5
    elif rsi_val > 70:
        return -1.0  # Overbought — strong sell
    elif rsi_val > 60:
        return -0.5
    return 0.0


def _score_macd(macd_line: float, macd_signal: float, macd_hist: float) -> float:
    """MACD scoring: bullish crossover = buy, bearish = sell."""
    if pd.isna(macd_line) or pd.isna(macd_signal):
        return 0.0

    score = 0.0
    # Line above signal = bullish
    if macd_line > macd_signal:
        score += 0.5
    else:
        score -= 0.5

    # Histogram direction (momentum)
    if not pd.isna(macd_hist):
        if macd_hist > 0:
            score += 0.3
        else:
            score -= 0.3

    return max(-1.0, min(1.0, score))


def _score_moving_averages(
    close: float, sma_20: float, sma_50: float, sma_200: float
) -> float:
    """MA scoring: price above MAs = bullish, golden/death cross."""
    if any(pd.isna(v) for v in [close, sma_20, sma_50, sma_200]):
        return 0.0

    score = 0.0
    # Price above key MAs
    if close > sma_20:
        score += 0.2
    else:
        score -= 0.2

    if close > sma_50:
        score += 0.2
    else:
        score -= 0.2

    if close > sma_200:
        score += 0.2
    else:
        score -= 0.2

    # Golden cross (SMA 50 > SMA 200) / Death cross
    if sma_50 > sma_200:
        score += 0.4
    else:
        score -= 0.4

    return max(-1.0, min(1.0, score))


def _score_bollinger(close: float, bb_upper: float, bb_lower: float, bb_percent: float) -> float:
    """Bollinger Bands scoring: near lower = buy, near upper = sell."""
    if any(pd.isna(v) for v in [close, bb_upper, bb_lower, bb_percent]):
        return 0.0

    if bb_percent < 0.0:
        return 1.0  # Below lower band — oversold
    elif bb_percent < 0.2:
        return 0.6
    elif bb_percent > 1.0:
        return -1.0  # Above upper band — overbought
    elif bb_percent > 0.8:
        return -0.6
    return 0.0


def _score_supertrend(direction: int) -> float:
    """Supertrend direction: 1 = uptrend (buy), -1 = downtrend (sell)."""
    if pd.isna(direction):
        return 0.0
    return 1.0 if direction == 1 else -1.0


def _score_stochastic_rsi(stoch_k: float, stoch_d: float) -> float:
    """Stochastic RSI scoring."""
    if pd.isna(stoch_k) or pd.isna(stoch_d):
        return 0.0

    score = 0.0
    if stoch_k < 0.2:
        score += 0.7  # Oversold
    elif stoch_k > 0.8:
        score -= 0.7  # Overbought

    # Crossover
    if stoch_k > stoch_d:
        score += 0.3
    else:
        score -= 0.3

    return max(-1.0, min(1.0, score))


def _score_williams_r(wr: float) -> float:
    """Williams %R scoring."""
    if pd.isna(wr):
        return 0.0
    if wr < -80:
        return 0.8  # Oversold
    elif wr > -20:
        return -0.8  # Overbought
    return 0.0


def _score_volume(obv_series: pd.Series) -> float:
    """Volume confirmation via OBV trend (last 5 values)."""
    recent = obv_series.dropna().tail(5)
    if len(recent) < 3:
        return 0.0

    # Check if OBV is trending up or down
    slope = (recent.iloc[-1] - recent.iloc[0]) / len(recent)
    if slope > 0:
        return 0.5  # Volume confirming uptrend
    elif slope < 0:
        return -0.5
    return 0.0


# =====================================================
# INDICATOR WEIGHTS
# =====================================================

INDICATOR_WEIGHTS = {
    "rsi": 0.15,
    "macd": 0.15,
    "moving_averages": 0.15,
    "bollinger": 0.10,
    "supertrend": 0.15,
    "stochastic_rsi": 0.10,
    "williams_r": 0.05,
    "volume": 0.15,
}


# =====================================================
# MAIN SIGNAL GENERATION
# =====================================================

def generate_signal(df: pd.DataFrame) -> dict:
    """
    Generate a trading signal from OHLCV data.

    Returns:
        dict with keys:
            - signal: 'BUY' | 'SELL' | 'HOLD'
            - composite_score: float (-1 to +1)
            - confidence: float (0 to 1)
            - indicator_scores: dict of individual scores
            - reasoning: list of human-readable reasons
    """
    # Compute all indicators
    df = compute_all(df)
    latest = df.iloc[-1]

    # Compute individual scores
    scores = {}
    reasoning = []

    # RSI
    scores["rsi"] = _score_rsi(latest.get("RSI", float("nan")))
    if scores["rsi"] > 0.5:
        reasoning.append(f"RSI ({latest.get('RSI', 0):.1f}) indicates oversold conditions")
    elif scores["rsi"] < -0.5:
        reasoning.append(f"RSI ({latest.get('RSI', 0):.1f}) indicates overbought conditions")

    # MACD
    scores["macd"] = _score_macd(
        latest.get("MACD_Line", float("nan")),
        latest.get("MACD_Signal", float("nan")),
        latest.get("MACD_Histogram", float("nan")),
    )
    if scores["macd"] > 0.3:
        reasoning.append("MACD shows bullish momentum")
    elif scores["macd"] < -0.3:
        reasoning.append("MACD shows bearish momentum")

    # Moving Averages
    scores["moving_averages"] = _score_moving_averages(
        latest["Close"],
        latest.get("SMA_20", float("nan")),
        latest.get("SMA_50", float("nan")),
        latest.get("SMA_200", float("nan")),
    )
    if scores["moving_averages"] > 0.5:
        reasoning.append("Price is above key moving averages (bullish trend)")
    elif scores["moving_averages"] < -0.5:
        reasoning.append("Price is below key moving averages (bearish trend)")

    # Bollinger Bands
    scores["bollinger"] = _score_bollinger(
        latest["Close"],
        latest.get("BB_Upper", float("nan")),
        latest.get("BB_Lower", float("nan")),
        latest.get("BB_Percent", float("nan")),
    )
    if scores["bollinger"] > 0.5:
        reasoning.append("Price near Bollinger Band lower — potential bounce")
    elif scores["bollinger"] < -0.5:
        reasoning.append("Price near Bollinger Band upper — potential pullback")

    # Supertrend
    scores["supertrend"] = _score_supertrend(
        latest.get("Supertrend_Direction", float("nan"))
    )
    if scores["supertrend"] > 0:
        reasoning.append("Supertrend confirms uptrend")
    elif scores["supertrend"] < 0:
        reasoning.append("Supertrend confirms downtrend")

    # Stochastic RSI
    scores["stochastic_rsi"] = _score_stochastic_rsi(
        latest.get("StochRSI_K", float("nan")),
        latest.get("StochRSI_D", float("nan")),
    )

    # Williams %R
    scores["williams_r"] = _score_williams_r(
        latest.get("Williams_R", float("nan"))
    )

    # Volume (OBV)
    scores["volume"] = _score_volume(df["OBV"])
    if scores["volume"] > 0.3:
        reasoning.append("Volume confirms buying pressure (OBV rising)")
    elif scores["volume"] < -0.3:
        reasoning.append("Volume confirms selling pressure (OBV falling)")

    # Weighted composite score
    composite_score = sum(
        scores[ind] * INDICATOR_WEIGHTS[ind] for ind in INDICATOR_WEIGHTS
    )

    # Determine signal and confidence
    confidence = abs(composite_score)

    if composite_score >= 0.35:
        signal = "BUY"
    elif composite_score <= -0.35:
        signal = "SELL"
    else:
        signal = "HOLD"
        if not reasoning:
            reasoning.append("Indicators are mixed — no clear directional bias")

    return {
        "signal": signal,
        "composite_score": round(composite_score, 4),
        "confidence": round(min(confidence, 1.0), 4),
        "indicator_scores": {k: round(v, 4) for k, v in scores.items()},
        "reasoning": reasoning,
    }


def generate_signal_for_symbol(symbol: str, df: pd.DataFrame) -> dict:
    """Convenience wrapper that includes the symbol in the result."""
    result = generate_signal(df)
    result["symbol"] = symbol
    return result
