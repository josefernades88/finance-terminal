import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Wealth Terminal", layout="wide")

# ---------------- HEADER ----------------
st.title("💼 Personal Wealth Terminal")

# ---------------- DATA ----------------
positions = [
    {"ticker": "BTC-USD", "name": "Bitcoin", "units": 3, "avg": 35},
    {"ticker": "WULF", "name": "Terawulf", "units": 3, "avg": 4},
    {"ticker": "AAPL", "name": "Apple", "units": 2, "avg": 150},
]

plans = {
    "Satélite": [
        {"ticker": "IUSN.DE", "units": 1, "avg": 25},
        {"ticker": "QDV5.DE", "units": 1, "avg": 25},
    ],
    "Core": [
        {"ticker": "SXR8.DE", "units": 1, "avg": 300},
    ]
}

# ---------------- SAFE PRICE ----------------
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

    st.write(
        f"**{p['name']} ({p['ticker']})** → "
        f"{value:.2f} EUR | P&L: {pnl:.2f} EUR ({pnl_pct:.2f}%)"
    )

# ---------------- PLANS ----------------
st.markdown("---")
st.markdown("### 📦 Investment Plans")

for name, assets in plans.items():
    plan_value = 0
    plan_cost = 0

    st.markdown(f"#### {name}")

    for a in assets:
        price = get_price(a["ticker"])
        if price is None:
            continue

        value = price * a["units"]
        cost = a["avg"] * a["units"]

        plan_value += value
        plan_cost += cost

    pnl = plan_value - plan_cost
    pnl_pct = (pnl / plan_cost) * 100 if plan_cost else 0

    total_value += plan_value
    total_cost += plan_cost

    st.info(f"{name}: {plan_value:.2f} EUR | {pnl_pct:.2f}%")

# ---------------- TOTAL ----------------
st.markdown("---")

total_pnl = total_value - total_cost
total_pct = (total_pnl / total_cost) * 100 if total_cost else 0

st.metric("Portfolio Value", f"{total_value:.2f} EUR")
st.metric("Invested", f"{total_cost:.2f} EUR")
st.metric("Total P&L", f"{total_pnl:.2f} EUR", f"{total_pct:.2f}%")
