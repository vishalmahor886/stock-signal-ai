# app.py

import streamlit as st
import pandas as pd
import requests

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="AI Trading Dashboard",
    page_icon="📈",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📊 Stock Analysis")

symbol = st.sidebar.text_input(
    "Enter Symbol",
    value="reliance"
).lower()

refresh = st.sidebar.button("🔄 Refresh")

# =====================================================
# API
# =====================================================

@st.cache_data(ttl=60)
def load_data(symbol):

    try:

        api_url = f"http://127.0.0.1:8000/api/signals/{symbol}"

        response = requests.get(
            api_url,
            timeout=120
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        st.error(f"API Error: {e}")
        return {}

if refresh:
    st.cache_data.clear()

data = load_data(symbol)

if not data:
    st.stop()

# =====================================================
# RESPONSE PARSING
# =====================================================

result = data.get("data", data)

technical = result.get("technical_signal", {})
indicator = result.get("indicator_summary", {})
ratios = result.get("financial_ratio", {})
financials = result.get("financial_statement", {})
news = result.get("news_sentiment", {})
ai = result.get("ai_respones", {})

# =====================================================
# HEADER
# =====================================================

st.title("📈 AI Trading Analysis Dashboard")

st.subheader(
    f"Stock : {data.get('symbol', symbol).upper()}"
)

# =====================================================
# AI RECOMMENDATION
# =====================================================

st.markdown("---")
st.header("🤖 AI Recommendation")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Decision",
    ai.get("decision", "NA")
)

c2.metric(
    "Confidence",
    f"{ai.get('confidence',0)}%"
)

c3.metric(
    "Score",
    ai.get("score", 0)
)

c4.metric(
    "Risk Reward",
    ai.get("risk_reward", 0)
)

st.markdown("### Trade Setup")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Entry",
    ai.get("entry_price", 0)
)

c2.metric(
    "Stop Loss",
    ai.get("stop_loss", 0)
)

c3.metric(
    "Target",
    ai.get("target_price", 0)
)

c4.metric(
    "Holding Days",
    ai.get("holding_days", 0)
)

st.info(
    ai.get(
        "reasoning",
        "No reasoning available"
    )
)

# =====================================================
# TECHNICAL SIGNAL
# =====================================================

st.markdown("---")
st.header("📊 Technical Signal")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Signal",
    technical.get("signal", "NA")
)

c2.metric(
    "Score",
    technical.get(
        "composite_score",
        0
    )
)

c3.metric(
    "Confidence",
    technical.get(
        "confidence",
        0
    )
)

reasoning = technical.get("reasoning", [])

if reasoning:

    st.subheader("Technical Reasoning")

    for item in reasoning:
        st.success(item)

# =====================================================
# PRICE
# =====================================================

st.markdown("---")
st.header("💹 Price Overview")

price = indicator.get("price", {})

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Open",
    price.get("open", 0)
)

c2.metric(
    "High",
    price.get("high", 0)
)

c3.metric(
    "Low",
    price.get("low", 0)
)

c4.metric(
    "Close",
    price.get("close", 0)
)

# =====================================================
# TREND
# =====================================================

st.markdown("---")
st.header("📈 Trend Indicators")

trend = indicator.get("trend", {})

if trend:

    trend_df = pd.DataFrame(
        list(trend.items()),
        columns=["Indicator", "Value"]
    )

    st.dataframe(
        trend_df,
        use_container_width=True
    )

# =====================================================
# MOMENTUM
# =====================================================

st.markdown("---")
st.header("⚡ Momentum Indicators")

momentum = indicator.get(
    "momentum",
    {}
)

if momentum:

    momentum_df = pd.DataFrame(
        list(momentum.items()),
        columns=["Indicator", "Value"]
    )

    st.dataframe(
        momentum_df,
        use_container_width=True
    )

# =====================================================
# VOLATILITY
# =====================================================

st.markdown("---")
st.header("🌊 Volatility")

volatility = indicator.get(
    "volatility",
    {}
)

if volatility:

    vol_df = pd.DataFrame(
        list(volatility.items()),
        columns=["Indicator", "Value"]
    )

    st.dataframe(
        vol_df,
        use_container_width=True
    )

# =====================================================
# VOLUME
# =====================================================

st.markdown("---")
st.header("📦 Volume Indicators")

volume = indicator.get(
    "volume",
    {}
)

if volume:

    volume_df = pd.DataFrame(
        list(volume.items()),
        columns=["Indicator", "Value"]
    )

    st.dataframe(
        volume_df,
        use_container_width=True
    )

# =====================================================
# SUPPORT RESISTANCE
# =====================================================

st.markdown("---")
st.header("🎯 Support & Resistance")

levels = indicator.get(
    "levels",
    {}
)

if levels:

    level_df = pd.DataFrame(
        list(levels.items()),
        columns=["Level", "Value"]
    )

    st.dataframe(
        level_df,
        use_container_width=True
    )

# =====================================================
# FINANCIAL RATIOS
# =====================================================

st.markdown("---")
st.header("🏦 Financial Ratios")

if ratios:

    ratio_df = pd.DataFrame(
        list(ratios.items()),
        columns=["Ratio", "Value"]
    )

    st.dataframe(
        ratio_df,
        use_container_width=True,
        height=450
    )

# =====================================================
# FINANCIAL STATEMENTS
# =====================================================

st.markdown("---")
st.header("📑 Financial Statements")

if financials:

    if isinstance(financials, dict):

        financial_df = pd.DataFrame(
            list(financials.items()),
            columns=[
                "Metric",
                "Value"
            ]
        )

        st.dataframe(
            financial_df,
            use_container_width=True,
            height=500
        )

# =====================================================
# NEWS SENTIMENT
# =====================================================

st.markdown("---")
st.header("📰 News Sentiment")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Overall Sentiment",
    news.get(
        "overall_sentiment",
        "NA"
    )
)

c2.metric(
    "Score",
    news.get(
        "sentiment_score",
        0
    )
)

c3.metric(
    "Confidence",
    news.get(
        "confidence",
        0
    )
)

summary = news.get("summary")

if summary:
    st.write(summary)

news_list = news.get(
    "news",
    []
)

if news_list:

    st.subheader("Latest News")

    for item in news_list:

        title = item.get(
            "title",
            "News"
        )

        with st.expander(title):

            st.write(
                "**Source:**",
                item.get(
                    "source",
                    "Unknown"
                )
            )

            st.write(
                "**Sentiment:**",
                item.get(
                    "sentiment",
                    "Neutral"
                )
            )

            st.write(
                item.get(
                    "summary",
                    ""
                )
            )

            url = item.get("url")

            if url:
                st.link_button(
                    "Open Article",
                    url
                )

# =====================================================
# RAW JSON
# =====================================================

st.markdown("---")

with st.expander("🔍 Raw API Response"):
    st.json(data)