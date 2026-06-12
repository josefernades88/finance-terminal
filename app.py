import streamlit as st
import yfinance as yf
import json
import os
import pandas as pd
from datetime import date

# ===================== CONFIG =====================
st.set_page_config(page_title="Wealth Terminal PRO", layout="wide")

st.markdown("""
<style>
body {
    background-color:#0b0f14;
    color:#e6e6e6;
    font-family: Arial;
}

.block-container {
    padding-top: 1.5rem;
}

h1, h2, h3 {
    color:#ffffff;
}

hr {
    border-color:#1f2a36;
}

div[data-testid="metric-container"] {
    background:#0f141b;
    border:1px solid #1f2a36;
    padding:10px;
    border-radius:6px;
}

section[data-testid="stSidebar"] {
    background:#0f141b;
}
</style>
""", unsafe_allow_html=True)

# ===================== FILES =====================
PORTFOLIO_FILE = "portfolio.json"
WATCHLIST_FILE = "watchlist.json"
HISTORY_FILE = "history.csv"

# ===================== DEFAULTS =====================
if not os.path.exists(PORTFOLIO_FILE):
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump([
            {"ticker":"BTC-USD","name":"Bitcoin","units":3,"avg":35},
            {"ticker":"AAPL","name":"Apple","units":2,"avg":150},
            {"ticker":"NVDA","name":"Nvidia","units":1,"avg":400}
        ], f)

if not os.path.exists(WATCHLIST_FILE):
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(["^GSPC","^NDX","BTC-USD","GC=F","CL=F","VIX"], f)

# ===================== LOAD =====================
def load_json(file):
    with open(file,"r") as f:
        return json.load(f)

def save_json(file,data):
    with open(file,"w") as f:
        json.dump(data,f,indent=2)

portfolio = load_json(PORTFOLIO_FILE)
watchlist = load_json(WATCHLIST_FILE)

# ===================== PRICE =====================
def price(t):
    try:
        return yf.Ticker(t).history(period="5d")["Close"].dropna().iloc[-1]
    except:
        return None

# ===================== NAV =====================
page = st.sidebar.radio("Terminal",["Dashboard","Portfolio","Markets","Watchlist"])

# ===================================================
# DASHBOARD
# ===================================================
if page == "Dashboard":

    st.title("MARKET OVERVIEW")

    total_value = 0
    total_cost = 0

    for p in portfolio:
        px = price(p["ticker"])
        if not px:
            continue

        value = px * p["units"]
        cost = p["avg"] * p["units"]

        pnl = value - cost
        pct = (pnl/cost)*100 if cost else 0

        total_value += value
        total_cost += cost

        color = "#00ff88" if pnl >= 0 else "#ff4d4d"

        st.markdown(f"""
        <div style="
            display:flex;
            justify-content:space-between;
            padding:5px 0;
            border-bottom:1px solid #1f2a36;
            font-size:13px;
        ">
            <div><b>{p['ticker']}</b> {p['name']}</div>
            <div style="color:{color};">
                {pct:.2f}% | {value:,.0f}€
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    c1,c2,c3 = st.columns(3)
    c1.metric("Portfolio",f"{total_value:,.0f}€")
    c2.metric("Invested",f"{total_cost:,.0f}€")
    c3.metric("P&L",f"{total_value-total_cost:,.0f}€")

    # ---- HISTORY ----
    os.makedirs("data",exist_ok=True)
    today = str(date.today())

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            if today not in f.read():
                with open(HISTORY_FILE,"a") as f2:
                    f2.write(f"{today},{total_value}\n")
    else:
        with open(HISTORY_FILE,"w") as f:
            f.write(f"{today},{total_value}\n")

    st.markdown("---")
    st.subheader("Equity Curve")

    df = pd.read_csv(HISTORY_FILE,names=["Date","Value"])
    df["Date"] = pd.to_datetime(df["Date"])
    st.line_chart(df.set_index("Date"))

# ===================================================
# PORTFOLIO
# ===================================================
elif page == "Portfolio":

    st.title("PORTFOLIO CONTROL ROOM")

    st.markdown("---")

    with st.form("add"):
        c1,c2,c3,c4 = st.columns(4)

        ticker = c1.text_input("Ticker")
        name = c2.text_input("Name")
        units = c3.number_input("Units",0.0)
        avg = c4.number_input("Avg",0.0)

        if st.form_submit_button("Add"):
            portfolio.append({
                "ticker":ticker.upper(),
                "name":name,
                "units":units,
                "avg":avg
            })
            save_json(PORTFOLIO_FILE,portfolio)
            st.rerun()

    st.markdown("---")

    for i,p in enumerate(portfolio):
        px = price(p["ticker"])
        if not px:
            continue

        value = px*p["units"]
        pnl = value - p["avg"]*p["units"]

        color = "#00ff88" if pnl>=0 else "#ff4d4d"

        col1,col2,col3 = st.columns([3,2,2])

        col1.write(f"{p['ticker']} — {p['name']}")
        col2.write(f"{value:,.0f}€")
        col3.markdown(f"<span style='color:{color}'>{pnl:,.0f}€</span>",unsafe_allow_html=True)

        if st.button("remove",key=i):
            portfolio.pop(i)
            save_json(PORTFOLIO_FILE,portfolio)
            st.rerun()

# ===================================================
# MARKETS
# ===================================================
elif page == "Markets":

    st.title("GLOBAL MARKETS SCAN")

    assets = {
        "S&P500":"^GSPC",
        "NASDAQ":"^NDX",
        "BTC":"BTC-USD",
        "GOLD":"GC=F",
        "OIL":"CL=F",
        "VIX":"^VIX"
    }

    cols = st.columns(3)

    for i,(name,t) in enumerate(assets.items()):
        data = yf.Ticker(t).history(period="2d")

        if len(data)>=2:
            last = data["Close"].iloc[-1]
            prev = data["Close"].iloc[-2]
            chg = ((last-prev)/prev)*100

            color = "#00ff88" if chg>=0 else "#ff4d4d"

            cols[i%3].markdown(f"""
            <div style="
                padding:10px;
                border:1px solid #1f2a36;
                border-radius:6px;
                margin-bottom:10px;
            ">
                <div style="font-size:11px;opacity:0.6">{name}</div>
                <div style="font-size:18px"><b>{last:,.2f}</b></div>
                <div style="color:{color}">{chg:.2f}%</div>
            </div>
            """,unsafe_allow_html=True)

# ===================================================
# WATCHLIST (NEW LEVEL)
# ===================================================
elif page == "Watchlist":

    st.title("WATCHLIST")

    new = st.text_input("Add ticker")
    if st.button("Add"):
        watchlist.append(new.upper())
        save_json(WATCHLIST_FILE,watchlist)
        st.rerun()

    st.markdown("---")

    cols = st.columns(3)

    for i,t in enumerate(watchlist):
        px = price(t)

        if not px:
            continue

        cols[i%3].metric(t,f"{px:,.2f}")
