[23:11, 20.06.2026] A.: import streamlit as st
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
[23:11, 20.06.2026] Roamic: Widzę, że udostępniasz kod w języku Python. Jako specjalista ds. wsparcia technicznego Roamic, zajmuję się wyłącznie pomocą w zakresie kart eSIM, zamówień i łączności. Nie mogę pomóc w programowaniu ani tworzeniu oprogramowania.

Jeśli potrzebujesz pomocy z Twoją kartą eSIM lub chcesz sprawdzić status zamówienia, proszę podaj adres e-mail użyty przy zakupie.
[23:16, 20.06.2026] A.: import streamlit as st
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

@st.cache_data(ttl=3600)
def momentum(ticker):
    try:
        df = yf.download(
            ticker,
            period="6mo",
            progress=False,
            threads=True,
            auto_adjust=True,
            prepost=False
        )
        
        # Bardzo bezpieczne sprawdzanie
        if df is None or df.empty:
            return 0.0
        
        close = df["Close"].dropna()
        
        if len(close) < 20:          # za mało danych
            return 0.0
        
        current = float(close.iloc[-1])
        lookback = min(60, len(close) - 1)
        past = float(close.iloc[-lookback])
        
        if past <= 0:
            return 0.0
            
        return (current - past) / past   # zwraca zwykły float Pythona
        
    except Exception as e:
        # st.warning(f"Problem z {ticker}: {str(e)[:100]}")  # możesz odkomentować do debugu
        return 0.0


# ==================== GŁÓWNA LOGIKA ====================
data = {}
for name, ticker in stocks.items():
    data[name] = momentum(ticker)

df = pd.DataFrame(list(data.items()), columns=["Stock", "Momentum"])

df = df.reset_index(drop=True)
df["Momentum"] = pd.to_numeric(df["Momentum"], errors="coerce").fillna(0.0)

df = df.sort_values("Momentum", ascending=False, ignore_index=True)

# Obliczenia
ai_score = float(df["Momentum"].mean())
top5_mean = float(df.head(5)["Momentum"].mean())
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

# ==================== UI ====================
col1, col2, col3 = st.columns(3)

col1.metric("AI SCORE", f"{ai_score:.3f}")
col2.subheader(regime(ai_score))
col3.metric("DCA (€)", allocation(ai_score))

st.metric("⚠️ BUBBLE RISK", f"{bubble:.3f}", delta="Top5 vs średnia")

st.subheader("🏆 TOP AI STOCKS")
st.dataframe(
    df.head(10).style.format({"Momentum": "{:.1%}"}),
    use_container_width=True,
    hide_index=True
)

fig = px.bar(
    df.head(10),
    x="Stock",
    y="Momentum",
    text_auto='.1%',
    title="Momentum AI Stocks (6 miesięcy)"
)
fig.update_layout(yaxis_tickformat='.0%')
st.plotly_chart(fig, use_container_width=True)

with st.expander("Wszystkie akcje"):
    st.dataframe(
        df.style.format({"Momentum": "{:.1%}"}),
        hide_index=True,
        use_container_width=True
    )
