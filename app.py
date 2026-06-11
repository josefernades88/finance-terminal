import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Finance Terminal", layout="wide")

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style="padding-bottom:10px;">
        <div style="font-size:30px; font-weight:700;">📈 Personal Finance Terminal</div>
        <div style="font-size:13px; opacity:0.6;">
            Markets • Portfolio • Crypto • Macro (personal use)
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- MARKETS ----------------
st.subheader("📊 Markets")

assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^NDX",
    "Dow": "^DJI",
    "VIX": "^VIX",
    "BTC": "BTC-USD",
    "ETH": "ETH-USD",
    "Gold": "GC=F",
    "Oil": "CL=F",
    "DXY": "DX-Y.NYB"
}

cols = st.columns(3)

for i, (name, ticker) in enumerate(assets.items()):
    data = yf.Ticker(ticker).history(period="2d")

    if len(data) >= 2:
        last = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2]
        change = ((last - prev) / prev) * 100

        color = "#00ff88" if change >= 0 else "#ff4d4d"

        cols[i % 3].markdown(
            f"""
            <div style="
                background-color:#0e1117;
                border:1px solid #1f1f1f;
                border-radius:10px;
                padding:12px;
                margin-bottom:10px;
            ">
                <div style="font-size:11px; opacity:0.6;">
                    {name}
                </div>

                <div style="font-size:22px; font-weight:700;">
                    {last:,.2f}
                </div>

                <div style="font-size:12px; color:{color};">
                    {change:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# ---------------- PORTFOLIO ----------------
st.subheader("💼 Portfolio")

portfolio = {
    "AAPL": {"shares": 5, "avg": 150},
    "NVDA": {"shares": 2, "avg": 400},
    "BTC-USD": {"shares": 0.1, "avg": 30000}
}

total_value = 0
total_cost = 0

for ticker, pos in portfolio.items():
    data = yf.Ticker(ticker).history(period="1d")

    if not data.empty:
        price = data["Close"].iloc[-1]

        value = price * pos["shares"]
        cost = pos["avg"] * pos["shares"]

        total_value += value
        total_cost += cost

        pnl = value - cost
        pnl_color = "#00ff88" if pnl >= 0 else "#ff4d4d"

        st.markdown(
            f"""
            <div style="
                padding:10px;
                border-bottom:1px solid #1f1f1f;
            ">
                <b>{ticker}</b>
                <span style="float:right; color:{pnl_color};">
                    {pnl:,.2f}
                </span>
                <br>
                <span style="opacity:0.6;">
                    Value: {value:,.2f} | Invested: {cost:,.2f}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

profit = total_value - total_cost

st.markdown("---")

st.metric("Total Portfolio P&L", f"{profit:,.2f}")
