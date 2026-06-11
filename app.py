import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Wealth Terminal", layout="wide")

# ---------------- SIDEBAR (BLOOMBERG FEEL) ----------------
st.sidebar.title("📊 Terminal")
page = st.sidebar.radio("Navigation", ["Dashboard"])

# ---------------- HEADER ----------------
st.title("💼 Personal Wealth Terminal")
st.caption("Portfolio • Markets • Performance")

st.markdown("---")

# ---------------- DATA ----------------
positions = [
    {"ticker": "BTC-USD", "name": "Bitcoin", "units": 3, "avg": 35},
    {"ticker": "WULF", "name": "Terawulf", "units": 3, "avg": 4},
    {"ticker": "AAPL", "name": "Apple", "units": 2, "avg": 150},
]

# ---------------- SAFE PRICE ----------------
def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if data.empty:
            return None
        return data["Close"].dropna().iloc[-1]
    except:
        return None

# ---------------- PORTFOLIO CALC ----------------
total_value = 0
total_cost = 0

st.subheader("🏠 Overview")

cols = st.columns(3)

# ---------------- POSITIONS ----------------
st.markdown("### 🧾 Positions")

for p in positions:
    price = get_price(p["ticker"])

    if price is None:
        continue

    value = price * p["units"]
    cost = p["avg"] * p["units"]
    pnl = value - cost
    pnl_pct = (pnl / cost) * 100 if cost else 0

    total_value += value
    total_cost += cost

    st.write(
        f"**{p['name']} ({p['ticker']})** → "
        f"{value:.2f} EUR | P&L: {pnl:.2f} ({pnl_pct:.2f}%)"
    )

st.markdown("---")

# ---------------- TOTAL METRICS ----------------
total_pnl = total_value - total_cost
total_pct = (total_pnl / total_cost) * 100 if total_cost else 0

cols[0].metric("Portfolio Value", f"{total_value:.2f} EUR")
cols[1].metric("Invested", f"{total_cost:.2f} EUR")
cols[2].metric("Total P&L", f"{total_pnl:.2f} EUR", f"{total_pct:.2f}%")

st.markdown("---")

# ---------------- PERFORMANCE CHART (C FEATURE) ----------------
st.subheader("📈 Portfolio Performance (simulado)")

# histórico simples baseado em variação de preço dos ativos
dates = pd.date_range(end=datetime.date.today(), periods=30)

portfolio_values = []

for i in range(30):
    daily_value = 0

    for p in positions:
        data = yf.Ticker(p["ticker"]).history(period="30d")

        if not data.empty:
            try:
                price = data["Close"].iloc[i]
                daily_value += price * p["units"]
            except:
                pass

    portfolio_values.append(daily_value)

df = pd.DataFrame({
    "Date": dates,
    "Portfolio": portfolio_values
})

st.line_chart(df.set_index("Date"))
