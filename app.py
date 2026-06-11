import streamlit as st
import yfinance as yf
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="Wealth Terminal", layout="wide")

# ---------------- HEADER ----------------
st.markdown(
    """
    <div style="font-size:26px;font-weight:700;letter-spacing:0.5px;">
        WEALTH TERMINAL
    </div>
    <div style="font-size:12px;opacity:0.6;margin-bottom:10px;">
        personal portfolio • markets • performance tracking
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------- DATA ----------------
positions = [
    {"ticker": "BTC-USD", "name": "Bitcoin", "units": 3, "avg": 35},
    {"ticker": "WULF", "name": "Terawulf", "units": 3, "avg": 4},
    {"ticker": "AAPL", "name": "Apple", "units": 2, "avg": 150},
]

# ---------------- HISTORY ----------------
HISTORY_FILE = "data/portfolio_history.csv"

def save_portfolio_value(total_value):
    os.makedirs("data", exist_ok=True)
    today = str(date.today())
    row = f"{today},{total_value}\n"

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            if today in f.read():
                return

    with open(HISTORY_FILE, "a") as f:
        f.write(row)

# ---------------- PRICE FUNCTION ----------------
def get_price(ticker):
    try:
        data = yf.Ticker(ticker).history(period="5d")
        if data.empty:
            return None
        return data["Close"].dropna().iloc[-1]
    except:
        return None

# ---------------- CALCULATIONS ----------------
total_value = 0
total_cost = 0

st.subheader("🏠 Overview")

# ---------------- POSITIONS ----------------
st.markdown("### 🧾 Positions")

for p in positions:
    price = get_price(p["ticker"])

    if price is None:
        st.warning(f"Sem dados: {p['ticker']}")
        continue

    value = price * p["units"]
    cost = p["avg"] * p["units"]
    pnl = value - cost
    pnl_pct = (pnl / cost) * 100 if cost else 0

    total_value += value
    total_cost += cost

    color = "#00ff88" if pnl >= 0 else "#ff4d4d"

    st.markdown(
        f"""
        <div style="
            padding:6px 0;
            border-bottom:1px solid #1f1f1f;
            font-size:13px;
        ">
            <b>{p['name']}</b> ({p['ticker']})
            <span style="float:right;color:{color};">
                {value:,.2f} EUR | {pnl_pct:.2f}%
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- TOTAL ----------------
total_pnl = total_value - total_cost
total_pct = (total_pnl / total_cost) * 100 if total_cost else 0

st.markdown("---")

col1, col2, col3 = st.columns(3)

col1.metric("Portfolio Value", f"{total_value:,.2f} EUR")
col2.metric("Invested", f"{total_cost:,.2f} EUR")
col3.metric("Total P&L", f"{total_pnl:,.2f} EUR", f"{total_pct:.2f}%")

# ---------------- SAVE HISTORY ----------------
save_portfolio_value(total_value)

st.markdown("---")

# ---------------- PERFORMANCE (REAL EQUITY CURVE) ----------------
st.subheader("📈 Real Portfolio Performance")

if os.path.exists(HISTORY_FILE):
    df = pd.read_csv(HISTORY_FILE, names=["Date", "Value"])
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")

    st.line_chart(df.set_index("Date"))
else:
    st.info("Ainda sem histórico suficiente.")
    
# ---------------- MARKET CONTEXT ----------------
st.markdown("---")
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
