"""
Technical Indicator Engine
Computes all major technical indicators on OHLCV DataFrames.
"""

import pandas as pd
import numpy as np


# =====================================================
# TREND INDICATORS
# =====================================================

def sma(df: pd.DataFrame, column: str = "Close", periods: list[int] = None) -> pd.DataFrame:
    """Simple Moving Averages."""
    if periods is None:
        periods = [20, 50, 200]
    for p in periods:
        df[f"SMA_{p}"] = df[column].rolling(window=p).mean()
    return df


def ema(df: pd.DataFrame, column: str = "Close", periods: list[int] = None) -> pd.DataFrame:
    """Exponential Moving Averages."""
    if periods is None:
        periods = [12, 26]
    for p in periods:
        df[f"EMA_{p}"] = df[column].ewm(span=p, adjust=False).mean()
    return df


def macd(
    df: pd.DataFrame,
    column: str = "Close",
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> pd.DataFrame:
    """MACD: line, signal line, and histogram."""
    ema_fast = df[column].ewm(span=fast, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow, adjust=False).mean()
    df["MACD_Line"] = ema_fast - ema_slow
    df["MACD_Signal"] = df["MACD_Line"].ewm(span=signal, adjust=False).mean()
    df["MACD_Histogram"] = df["MACD_Line"] - df["MACD_Signal"]
    return df


def supertrend(
    df: pd.DataFrame, period: int = 10, multiplier: float = 3.0
) -> pd.DataFrame:
    """Supertrend indicator for trend direction."""
    hl2 = (df["High"] + df["Low"]) / 2
    atr_val = atr(df.copy(), period=period)["ATR"]

    upper_band = hl2 + (multiplier * atr_val)
    lower_band = hl2 - (multiplier * atr_val)

    supertrend_vals = pd.Series(np.nan, index=df.index)
    direction = pd.Series(1, index=df.index)  # 1 = up, -1 = down

    for i in range(1, len(df)):
        if df["Close"].iloc[i] > upper_band.iloc[i - 1]:
            direction.iloc[i] = 1
        elif df["Close"].iloc[i] < lower_band.iloc[i - 1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i - 1]

        if direction.iloc[i] == 1:
            lower_band.iloc[i] = max(lower_band.iloc[i], lower_band.iloc[i - 1])
            supertrend_vals.iloc[i] = lower_band.iloc[i]
        else:
            upper_band.iloc[i] = min(upper_band.iloc[i], upper_band.iloc[i - 1])
            supertrend_vals.iloc[i] = upper_band.iloc[i]

    df["Supertrend"] = supertrend_vals
    df["Supertrend_Direction"] = direction
    return df


# =====================================================
# MOMENTUM INDICATORS
# =====================================================

def rsi(df: pd.DataFrame, column: str = "Close", period: int = 14) -> pd.DataFrame:
    """Relative Strength Index."""
    delta = df[column].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100.0 - (100.0 / (1.0 + rs))
    return df


def stochastic_rsi(
    df: pd.DataFrame, rsi_period: int = 14, stoch_period: int = 14
) -> pd.DataFrame:
    """Stochastic RSI."""
    if "RSI" not in df.columns:
        df = rsi(df, period=rsi_period)

    rsi_vals = df["RSI"]
    rsi_min = rsi_vals.rolling(window=stoch_period).min()
    rsi_max = rsi_vals.rolling(window=stoch_period).max()

    df["StochRSI"] = (rsi_vals - rsi_min) / (rsi_max - rsi_min)
    df["StochRSI_K"] = df["StochRSI"].rolling(window=3).mean()
    df["StochRSI_D"] = df["StochRSI_K"].rolling(window=3).mean()
    return df


def williams_r(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Williams %R."""
    highest_high = df["High"].rolling(window=period).max()
    lowest_low = df["Low"].rolling(window=period).min()
    df["Williams_R"] = -100 * (highest_high - df["Close"]) / (highest_high - lowest_low)
    return df


# =====================================================
# VOLATILITY INDICATORS
# =====================================================

def bollinger_bands(
    df: pd.DataFrame, column: str = "Close", period: int = 20, std_dev: float = 2.0
) -> pd.DataFrame:
    """Bollinger Bands: upper, middle, lower."""
    sma_val = df[column].rolling(window=period).mean()
    rolling_std = df[column].rolling(window=period).std()

    df["BB_Upper"] = sma_val + (std_dev * rolling_std)
    df["BB_Middle"] = sma_val
    df["BB_Lower"] = sma_val - (std_dev * rolling_std)
    df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / df["BB_Middle"]
    df["BB_Percent"] = (df[column] - df["BB_Lower"]) / (df["BB_Upper"] - df["BB_Lower"])
    return df


def atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Average True Range."""
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()

    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["ATR"] = true_range.ewm(span=period, adjust=False).mean()
    return df


# =====================================================
# VOLUME INDICATORS
# =====================================================

def obv(df: pd.DataFrame) -> pd.DataFrame:
    """On-Balance Volume."""
    obv_vals = [0]
    for i in range(1, len(df)):
        if df["Close"].iloc[i] > df["Close"].iloc[i - 1]:
            obv_vals.append(obv_vals[-1] + df["Volume"].iloc[i])
        elif df["Close"].iloc[i] < df["Close"].iloc[i - 1]:
            obv_vals.append(obv_vals[-1] - df["Volume"].iloc[i])
        else:
            obv_vals.append(obv_vals[-1])
    df["OBV"] = obv_vals
    return df


def vwap(df: pd.DataFrame) -> pd.DataFrame:
    """Volume Weighted Average Price (intraday approximation)."""
    typical_price = (df["High"] + df["Low"] + df["Close"]) / 3
    cumulative_tp_vol = (typical_price * df["Volume"]).cumsum()
    cumulative_vol = df["Volume"].cumsum()
    df["VWAP"] = cumulative_tp_vol / cumulative_vol
    return df


# =====================================================
# SUPPORT / RESISTANCE
# =====================================================

def pivot_points(df: pd.DataFrame) -> pd.DataFrame:
    """Standard pivot points from previous day's OHLC."""
    prev_high = df["High"].shift(1)
    prev_low = df["Low"].shift(1)
    prev_close = df["Close"].shift(1)

    pivot = (prev_high + prev_low + prev_close) / 3

    df["Pivot"] = pivot
    df["R1"] = (2 * pivot) - prev_low
    df["S1"] = (2 * pivot) - prev_high
    df["R2"] = pivot + (prev_high - prev_low)
    df["S2"] = pivot - (prev_high - prev_low)
    df["R3"] = prev_high + 2 * (pivot - prev_low)
    df["S3"] = prev_low - 2 * (prev_high - pivot)
    return df


# =====================================================
# COMPOSITE: COMPUTE ALL
# =====================================================

def compute_all(df: pd.DataFrame) -> pd.DataFrame:
    """Compute all indicators on a DataFrame with OHLCV columns."""
    df = df.copy()

    # Trend
    df = sma(df)
    df = ema(df)
    df = macd(df)
    df = supertrend(df)

    # Momentum
    df = rsi(df)
    df = stochastic_rsi(df)
    df = williams_r(df)

    # Volatility
    df = bollinger_bands(df)
    df = atr(df)

    # Volume
    df = obv(df)
    df = vwap(df)

    # Support/Resistance
    df = pivot_points(df)

    return df


def get_latest_summary(df: pd.DataFrame) -> dict:
    """
    Get the latest indicator values as a dictionary.
    Useful for passing to the AI agent for analysis.
    """
    df = compute_all(df)
    latest = df.iloc[-1]

    summary = {
        "price": {
            "open": round(float(latest["Open"]), 2),
            "high": round(float(latest["High"]), 2),
            "low": round(float(latest["Low"]), 2),
            "close": round(float(latest["Close"]), 2),
            "volume": int(latest["Volume"]),
        },
        "trend": {
            "sma_20": round(float(latest.get("SMA_20", 0)), 2),
            "sma_50": round(float(latest.get("SMA_50", 0)), 2),
            "sma_200": round(float(latest.get("SMA_200", 0)), 2),
            "ema_12": round(float(latest.get("EMA_12", 0)), 2),
            "ema_26": round(float(latest.get("EMA_26", 0)), 2),
            "macd_line": round(float(latest.get("MACD_Line", 0)), 4),
            "macd_signal": round(float(latest.get("MACD_Signal", 0)), 4),
            "macd_histogram": round(float(latest.get("MACD_Histogram", 0)), 4),
            "supertrend": round(float(latest.get("Supertrend", 0)), 2),
            "supertrend_direction": int(latest.get("Supertrend_Direction", 0)),
        },
        "momentum": {
            "rsi": round(float(latest.get("RSI", 0)), 2),
            "stoch_rsi_k": round(float(latest.get("StochRSI_K", 0)), 4),
            "stoch_rsi_d": round(float(latest.get("StochRSI_D", 0)), 4),
            "williams_r": round(float(latest.get("Williams_R", 0)), 2),
        },
        "volatility": {
            "bb_upper": round(float(latest.get("BB_Upper", 0)), 2),
            "bb_middle": round(float(latest.get("BB_Middle", 0)), 2),
            "bb_lower": round(float(latest.get("BB_Lower", 0)), 2),
            "bb_width": round(float(latest.get("BB_Width", 0)), 4),
            "bb_percent": round(float(latest.get("BB_Percent", 0)), 4),
            "atr": round(float(latest.get("ATR", 0)), 2),
        },
        "volume": {
            "obv": int(latest.get("OBV", 0)),
            "vwap": round(float(latest.get("VWAP", 0)), 2),
        },
        "levels": {
            "pivot": round(float(latest.get("Pivot", 0)), 2),
            "r1": round(float(latest.get("R1", 0)), 2),
            "r2": round(float(latest.get("R2", 0)), 2),
            "r3": round(float(latest.get("R3", 0)), 2),
            "s1": round(float(latest.get("S1", 0)), 2),
            "s2": round(float(latest.get("S2", 0)), 2),
            "s3": round(float(latest.get("S3", 0)), 2),
        },
        "recent_candles": [],
    }

    # Add last 10 candles for price action context
    for i in range(-10, 0):
        if abs(i) <= len(df):
            row = df.iloc[i]
            summary["recent_candles"].append({
                "open": round(float(row["Open"]), 2),
                "high": round(float(row["High"]), 2),
                "low": round(float(row["Low"]), 2),
                "close": round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            })

    return summary
