ANALYSIS_PROMPT = """You are an expert Indian stock market swing trader and technical analyst.
Analyze the following data for {symbol} and provide a trading decision.

## Current Price Data
- Open: ₹{open}
- High: ₹{high}
- Low: ₹{low}
- Close: ₹{close}
- Volume: {volume}

## Technical Indicators

### Trend
- SMA 20: ₹{sma_20} | SMA 50: ₹{sma_50} | SMA 200: ₹{sma_200}
- EMA 12: ₹{ema_12} | EMA 26: ₹{ema_26}
- MACD Line: {macd_line} | Signal: {macd_signal} | Histogram: {macd_histogram}
- Supertrend Direction: {supertrend_direction}

### Momentum
- RSI (14): {rsi}
- Stochastic RSI K: {stoch_rsi_k} | D: {stoch_rsi_d}
- Williams %R: {williams_r}

### Volatility
- Bollinger Upper: ₹{bb_upper} | Middle: ₹{bb_middle} | Lower: ₹{bb_lower}
- BB Width: {bb_width} | BB %B: {bb_percent}
- ATR (14): ₹{atr}

### Volume
- OBV: {obv}
- VWAP: ₹{vwap}

### Support / Resistance
- Pivot: ₹{pivot}
- R1: ₹{r1} | R2: ₹{r2} | R3: ₹{r3}
- S1: ₹{s1} | S2: ₹{s2} | S3: ₹{s3}

## Technical Signal (Rule-based)
- Signal: {tech_signal}
- Composite Score: {tech_score}
- Confidence: {tech_confidence}
- Reasoning: {tech_reasoning}

## Recent Price Action (Last 10 candles)
{recent_candles}

## Your Task
Analyze all the above data and decide whether to BUY, SELL, or HOLD this stock for a swing trade (holding period: 3-15 trading days).

Consider:
1. Trend direction and strength
2. Momentum confirmation
3. Volatility and risk
4. Volume confirmation
5. Key support/resistance levels
6. Risk-reward ratio (minimum 1:2)

## Response Format
Respond ONLY with a valid JSON object (no markdown, no code blocks, no explanation outside JSON):
{{
    "decision": "BUY" or "SELL" or "HOLD",
    "confidence": 0.0 to 1.0,
    "entry_price": suggested entry price,
    "stop_loss": stop loss price,
    "target_price": target price,
    "holding_days": estimated holding period in days,
    "reasoning": "detailed explanation of your analysis and decision"
}}
"""