import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Finance Terminal", layout="wide")

# -----------------------
# HEADER
# -----------------------
st.title("📈 Finance Terminal")

st.caption("Mercado + Portefólio pessoal em tempo real")

st.markdown("---")

# -----------------------
# MERCADO (CORE)
# -----------------------
st.subheader("📊 Mercado")

assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^NDX",
    "Dow Jones": "^DJI",
    "VIX": "^VIX",
    "Bitcoin": "BTC-USD",
    "Ouro": "GC=F",
    "Petróleo": "CL=F",
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

# -----------------------
# PORTFÓLIO SIMPLES (FAKE POR AGORA)
# -----------------------
st.subheader("💼 Portefólio")

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

        st.write(f"**{ticker}** → Valor: {value:,.2f} | Investido: {cost:,.2f}")

profit = total_value - total_cost

st.markdown("---")

st.subheader(f"Resultado total: {profit:,.2f}")
