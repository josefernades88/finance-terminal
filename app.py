import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Terminal", layout="wide")

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style="
        font-size:28px;
        font-weight:700;
        margin-bottom:0px;">
        📈 Market Terminal
    </div>
    <div style="
        font-size:13px;
        opacity:0.6;
        margin-bottom:15px;">
        Personal finance • Markets • Portfolio
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- MARKET ----------------
st.subheader("📊 Markets")

assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^NDX",
    "Dow": "^DJI",
    "VIX": "^VIX",
    "BTC": "BTC-USD",
    "Gold": "GC=F",
    "Oil": "CL=F",
    "DXY": "DX-Y.NYB"
}

cols = st.columns(4)

for i, (name, ticker) in enumerate(assets.items()):
    data = yf.Ticker(ticker).history(period="2d")

    if len(data) >= 2:
        last = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2]
        change = ((last - prev) / prev) * 100

        cols[i % 4].markdown(
            f"""
            <div style="
                padding:10px;
                border:1px solid #222;
                border-radius:8px;
                margin-bottom:8px;">
                <div style="font-size:12px; opacity:0.7;">{name}</div>
                <div style="font-size:18px; font-weight:600;">
                    {last:,.2f}
                </div>
                <div style="font-size:12px; color:{'lime' if change >= 0 else 'red'};">
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

        st.markdown(
            f"**{ticker}** → Value: {value:,.0f} | Cost: {cost:,.0f}"
        )

profit = total_value - total_cost

st.markdown("---")

st.metric("Total P&L", f"{profit:,.2f}")
