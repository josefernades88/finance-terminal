import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Personal Wealth Terminal", layout="wide")

# ---------------- HEADER ----------------
st.title("💼 Personal Wealth Terminal")
st.caption("Visão pessoal de investimentos e património")

st.markdown("---")

# ---------------- PORTFOLIO (EDITÁVEL NO CÓDIGO) ----------------
portfolio = {
    "AAPL": {"shares": 5, "avg": 150},
    "NVDA": {"shares": 2, "avg": 400},
    "BTC-USD": {"shares": 0.1, "avg": 30000}
}

# ---------------- CALCULATIONS ----------------
total_value = 0
total_cost = 0

rows = []

for ticker, pos in portfolio.items():
    data = yf.Ticker(ticker).history(period="1d")

    if not data.empty:
        price = data["Close"].iloc[-1]

        value = price * pos["shares"]
        cost = pos["avg"] * pos["shares"]
        pnl = value - cost
        pnl_pct = (pnl / cost) * 100 if cost != 0 else 0

        total_value += value
        total_cost += cost

        rows.append({
            "ticker": ticker,
            "value": value,
            "cost": cost,
            "pnl": pnl,
            "pnl_pct": pnl_pct
        })

# ---------------- DASHBOARD ----------------
st.subheader("🏠 Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Portfolio Value", f"{total_value:,.2f}")

with col2:
    st.metric("Invested", f"{total_cost:,.2f}")

with col3:
    st.metric("Total P&L", f"{total_value - total_cost:,.2f}")

st.markdown("---")

# ---------------- POSITIONS ----------------
st.subheader("💼 Positions")

for r in rows:
    st.write(
        f"**{r['ticker']}** → "
        f"Value: {r['value']:,.2f} | "
        f"P&L: {r['pnl']:,.2f} ({r['pnl_pct']:.2f}%)"
    )

st.markdown("---")

# ---------------- MARKET CONTEXT ----------------
st.subheader("📊 Market Context")

assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^NDX",
    "BTC": "BTC-USD",
    "Gold": "GC=F",
    "Oil": "CL=F"
}

cols = st.columns(len(assets))

for i, (name, ticker) in enumerate(assets.items()):
    data = yf.Ticker(ticker).history(period="2d")

    if len(data) >= 2:
        last = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2]
        change = ((last - prev) / prev) * 100

        cols[i].metric(name, f"{last:,.2f}", f"{change:.2f}%")
