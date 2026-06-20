import streamlit as st
import yfinance as yf
import pandas as pd
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

@st.cache_data(ttl=3600)  # cache na 1 godzinę
def momentum(ticker):
    try:
        df = yf.download(ticker, period="6mo", progress=False, threads=True)
        
        if df.empty or len(df) < 20:  # minimum rozsądna liczba dni
            return 0.0
            
        # Bezpieczne pobieranie cen (ostatnia i sprzed ~60 dni handlowych)
        close = df["Close"]
        current = close.iloc[-1]
        
        # Bierzemy cenę sprzed ok. 60 sesji lub tyle ile jest (minimum 20)
        lookback = min(60, len(close) - 1)
        past = close.iloc[-lookback]
        
        if past == 0:
            return 0.0
            
        return (current - past) / past
    except Exception as e:
        st.warning(f"Problem z {ticker}: {e}")
        return 0.0


# Pobieranie danych
data = {}
for name, ticker in stocks.items():
    data[name] = momentum(ticker)

# Tworzenie DataFrame
df = pd.DataFrame(list(data.items()), columns=["Stock", "Momentum"])

# === KLUCZOWE POPRAWKI ===
df = df.reset_index(drop=True)                    # zapobiega błędowi indeksów
df["Momentum"] = pd.to_numeric(df["Momentum"], errors='coerce')  # wymusza float
df = df.sort_values("Momentum", ascending=False, ignore_index=True)

# Obliczenia
ai_score = df["Momentum"].mean()
top5_mean = df.head(5)["Momentum"].mean()
bubble = top5_mean - ai_score

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

# Dashboard
col1, col2, col3 = st.columns(3)

col1.metric("AI SCORE", f"{ai_score:.3f}")
col2.subheader(regime(ai_score))
col3.metric("DCA (€)", allocation(ai_score))

st.metric("⚠️ BUBBLE RISK", f"{bubble:.3f}", 
          delta=f"Top5 vs średnia")

st.subheader("🏆 TOP AI STOCKS")
st.dataframe(
    df.head(10).style.format({"Momentum": "{:.1%}"}),
    use_container_width=True,
    hide_index=True
)

# Wykres
fig = px.bar(
    df.head(10), 
    x="Stock", 
    y="Momentum",
    text="Momentum",
    title="Momentum AI Stocks (6M)"
)
fig.update_traces(texttemplate='%{y:.1%}', textposition='outside')
fig.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig, use_container_width=True)

# Opcjonalnie pełna tabela
with st.expander("Wszystkie akcje"):
    st.dataframe(df.style.format({"Momentum": "{:.1%}"}), hide_index=True)
