import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI FUND v6", layout="wide")

st.title("📊 AI FUND AUTOPILOT v6")

stocks = {
    "NVIDIA": "NVDA",
    "AMD": "AMD",
    "TSMC": "TSM",
    "ASML": "ASML",
    "Broadcom": "AVGO",
    "Marvell": "MRVL",
    "SMCI": "SMCI",
    "Palantir": "PLTR",
    "Micron": "MU",
    "ARM": "ARM"
}

@st.cache_data
def momentum(ticker):
    df = yf.download(ticker, period="6mo")
    return (df["Close"].iloc[-1] - df["Close"].iloc[-60]) / df["Close"].iloc[-60]

data = {}

for name, ticker in stocks.items():
    try:
        data[name] = momentum(ticker)
    except:
        data[name] = 0

df = pd.DataFrame(list(data.items()), columns=["Stock", "Momentum"])
df = df.sort_values("Momentum", ascending=False)

ai_score = df["Momentum"].mean()

top = df.head(5)["Momentum"].mean()
bubble = top - ai_score

def regime(x):
    if x > 0.15:
        return "🟢 BULL"
    elif x > 0.05:
        return "🟡 NORMAL"
    elif x > 0:
        return "🔴 LATE"
    else:
        return "🚨 CRASH"

def allocation(x):
    if x > 0.15:
        return 600
    elif x > 0.05:
        return 300
    elif x > 0:
        return 150
    else:
        return 0

col1, col2, col3 = st.columns(3)

col1.metric("AI SCORE", round(ai_score, 3))
col2.subheader(regime(ai_score))
col3.metric("DCA (€)", allocation(ai_score))

st.metric("⚠️ BUBBLE RISK", round(bubble, 3))

st.subheader("🏆 TOP AI STOCKS")
st.dataframe(df.head(10))

fig = px.bar(df.head(10), x="Stock", y="Momentum")
st.plotly_chart(fig, use_container_width=True)
