import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Trading Dashboard",
    page_icon="📈",
    layout="wide"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.buy-box {
    background-color: #0f5132;
    padding: 20px;
    border-radius: 15px;
    color: white;
}

.sell-box {
    background-color: #842029;
    padding: 20px;
    border-radius: 15px;
    color: white;
}

.hold-box {
    background-color: #664d03;
    padding: 20px;
    border-radius: 15px;
    color: white;
}

.metric-card {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# HEADER
# ==========================

st.title("🚀 AI Trading Dashboard")
st.caption("Technical + News + AI Sentiment Analysis")

# ==========================
# SIDEBAR
# ==========================

st.sidebar.header("Stock Search")

symbol = st.sidebar.text_input(
    "Stock Symbol",
    value="RELIANCE"
)

backend_url = st.sidebar.text_input(
    "Backend URL",
    value="http://localhost:8000/api/signals"
)

analyze = st.sidebar.button("Analyze")

# ==========================
# API CALL
# ==========================

if analyze:

    with st.spinner("Running AI Analysis..."):

        try:

            response = requests.get(
                f"{backend_url}/{symbol.upper()}"
            )

            result = response.json()

            data = result["data"]

            news = data["news_sentiment"]

            # ==================================
            # TOP SUMMARY
            # ==================================

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Overall Sentiment",
                news["overall_sentiment"]
            )

            col2.metric(
                "Sentiment Score",
                round(news["sentiment_score"], 2)
            )

            col3.metric(
                "Confidence",
                f"{news['confidence']*100:.1f}%"
            )

            st.divider()

            # ==================================
            # BUY SELL HOLD
            # ==================================

            decision = news["decision"]

            if decision == "BUY":
                st.markdown(
                    f"""
                    <div class="buy-box">
                    <h1>🟢 BUY</h1>
                    <h3>Confidence: {news['confidence']*100:.1f}%</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif decision == "SELL":
                st.markdown(
                    f"""
                    <div class="sell-box">
                    <h1>🔴 SELL</h1>
                    <h3>Confidence: {news['confidence']*100:.1f}%</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    f"""
                    <div class="hold-box">
                    <h1>🟡 HOLD</h1>
                    <h3>Confidence: {news['confidence']*100:.1f}%</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.divider()

            # ==================================
            # SUMMARY
            # ==================================

            st.subheader("📰 AI News Summary")

            st.info(news["summary"])

            st.divider()

            # ==================================
            # NEWS TABLE
            # ==================================

            st.subheader("Recent News Analysis")

            rows = []

            for item in news["news"]:

                rows.append({
                    "Title": item.get("title", ""),
                    "Sentiment": item.get("sentiment", ""),
                    "Summary": item.get("summary", "")
                })

            df = pd.DataFrame(rows)

            st.dataframe(
                df,
                use_container_width=True
            )

            st.divider()

            # ==================================
            # PIE CHART
            # ==================================

            st.subheader("Sentiment Distribution")

            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Positive",
                            "Negative",
                            "Neutral"
                        ],
                        values=[
                            news["positive_news_count"],
                            news["negative_news_count"],
                            news["neutral_news_count"]
                        ]
                    )
                ]
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.divider()

            # ==================================
            # BULLISH / BEARISH
            # ==================================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("🐂 Bullish Factors")

                bullish = []

                for n in news["news"]:
                    bullish.extend(
                        n.get("bullish_factors", [])
                    )

                for b in bullish:
                    st.success(b)

            with col2:

                st.subheader("🐻 Bearish Factors")

                bearish = []

                for n in news["news"]:
                    bearish.extend(
                        n.get("bearish_factors", [])
                    )

                for b in bearish:
                    st.error(b)

        except Exception as e:

            st.error(str(e))