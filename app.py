import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Personal Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
    <style>
        .main-title {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .sub-title {
            font-size: 14px;
            opacity: 0.7;
            margin-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📈 Personal Finance Terminal</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Markets • Portfolio • Crypto • Macro</div>', unsafe_allow_html=True)

st.markdown("---")

# ----------------------------
# MARKET OVERVIEW
# ----------------------------
st.subheader("📊 Market Overview")

assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^NDX",
    "Dow Jones": "^DJI",
    "VIX": "^VIX",
    "Bitcoin": "BTC-USD",
    "Gold": "GC=F",
    "Oil": "CL=F",
    "DXY": "DX-Y.NYB"
}

cols = st.columns(4)

i = 0

for name, ticker in assets.items():
    data = yf.Ticker(ticker).history(period="2d")

    if len(data) >= 2:
        last = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2]
        change = ((last - prev) / prev) * 100

        with cols[i % 4]:
            st.metric(
                label=name,
                value=f"{last:,.2f}",
                delta=f"{change:.2f}%"
            )
    else:
        with cols[i % 4]:
            st.metric(name, "N/A", "N/A")

    i += 1

st.markdown("---")

# ----------------------------
# PORTFOLIO (SIMPLE)
# ----------------------------
st.subheader("💼 Portfolio Snapshot")

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

        st.write(f"**{ticker}** → Value: {value:,.2f} | Invested: {cost:,.2f}")

profit = total_value - total_cost

st.markdown("---")

st.metric("Total P&L", f"{profit:,.2f}")
