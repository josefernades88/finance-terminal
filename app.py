import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Wealth Terminal", layout="wide")

st.title("💼 Personal Wealth Terminal")
st.caption("Portefólio pessoal com estrutura por planos e ativos")

st.markdown("---")

# -----------------------------
# POSIÇÕES INDIVIDUAIS
# -----------------------------
positions = {
    "BTC-USD": {"name": "Bitcoin Trust (CFD)", "units": 3, "avg": 40},
    "TERA": {"name": "Terawulf (Ação)", "units": 3, "avg": 4},
}

# -----------------------------
# PLANOS DE INVESTIMENTO
# -----------------------------
plans = {
    "Satélite": {
        "MSCI WORLD SMALL CAP ETF": {"units": 1, "avg": 25},
        "MSCI INDIA ETF": {"units": 1, "avg": 25},
    },
    "Core": {
        "S&P 500 ETF": {"units": 1, "avg": 300},
    }
}

# -----------------------------
# FUNÇÃO BASE
# -----------------------------
def get_value(ticker, units):
    data = yf.Ticker(ticker).history(period="1d")
    if data.empty:
        return None
    price = data["Close"].iloc[-1]
    return price * units, price

# -----------------------------
# CALCULAR POSIÇÕES
# -----------------------------
total_value = 0
total_cost = 0

st.subheader("📊 Overview")

# POSITIONS
st.markdown("### 🧾 Positions")

for ticker, data_dict in positions.items():
    result = get_value(ticker, data_dict["units"])
    if result:
        value, price = result
        cost = data_dict["avg"] * data_dict["units"]

        pnl = value - cost
        pnl_pct = (pnl / cost) * 100

        total_value += value
        total_cost += cost

        st.write(
            f"**{data_dict['name']}** → "
            f"{value:.2f} | P&L: {pnl:.2f} ({pnl_pct:.2f}%)"
        )

st.markdown("---")

# PLANS
st.markdown("### 📦 Investment Plans")

for plan_name, assets in plans.items():

    plan_value = 0
    plan_cost = 0

    st.markdown(f"#### {plan_name}")

    for ticker, d in assets.items():
        result = get_value(ticker, d["units"])
        if result:
            value, price = result
            cost = d["avg"] * d["units"]

            plan_value += value
            plan_cost += cost

            st.write(f"- {ticker}: {value:.2f}")

    plan_pnl = plan_value - plan_cost
    plan_pct = (plan_pnl / plan_cost) * 100 if plan_cost else 0

    st.info(f"{plan_name} Total → {plan_value:.2f} | P&L: {plan_pct:.2f}%")

    total_value += plan_value
    total_cost += plan_cost

st.markdown("---")

# -----------------------------
# TOTAL
# -----------------------------
total_pnl = total_value - total_cost
total_pct = (total_pnl / total_cost) * 100 if total_cost else 0

st.subheader("🏁 Total Portfolio")

st.metric("Value", f"{total_value:.2f}")
st.metric("Invested", f"{total_cost:.2f}")
st.metric("P&L", f"{total_pnl:.2f}", f"{total_pct:.2f}%")
