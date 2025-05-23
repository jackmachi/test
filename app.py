import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Satrix S&P 500 Tracker", layout="centered")
st.title("📈 Satrix S&P 500 ETF Tracker")

# Use IVV as a proxy for the Satrix S&P 500 ETF (IVV is an iShares S&P 500 ETF)
ticker = yf.Ticker("IVV")
data = ticker.history(period="1d", interval="5m")

st.subheader("Today's Price Movement")
st.line_chart(data["Close"])

st.subheader("What’s happening?")
if data["Close"].iloc[-1] > data["Close"].iloc[0]:
    st.success("✅ ETF is trending up. Likely due to market optimism or strong earnings.")
else:
    st.warning("⚠️ ETF is down today. Could be due to market uncertainty or negative news.")

st.subheader("💰 Profit Estimator")
amount = st.number_input("How much did you invest (R)?", value=500.0)
buy_price = st.number_input("Price you bought at (R)?", value=90.0)
current_price = data["Close"].iloc[-1]
units = amount / buy_price
value_now = units * current_price
profit = value_now - amount

st.metric("Current ETF Price", f"R{current_price:.2f}")
st.metric("Your Investment Value", f"R{value_now:.2f}", delta=f"R{profit:.2f}")

st.info("Tip: Use trends to decide when to add more (buy dips) or sell (take profit).")
