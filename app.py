import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Finance Terminal", layout="wide")

st.title("📈 Finance Terminal Simples")

st.header("📊 Mercado")

assets = {
    "S&P 500": "^GSPC",
    "Nasdaq": "^NDX",
    "Bitcoin": "BTC-USD",
    "DXY": "DX-Y.NYB"
}

for name, ticker in assets.items():
    data = yf.Ticker(ticker).history(period="2d")

    if len(data) >= 2:
        last = data["Close"].iloc[-1]
        prev = data["Close"].iloc[-2]
        change = ((last - prev) / prev) * 100

        st.write(f"{name}: {last:.2f} ({change:.2f}%)")
    else:
        st.write(f"{name}: sem dados")
