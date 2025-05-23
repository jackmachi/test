import streamlit as st
import yfinance as yf
from datetime import datetime
import requests

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

# Chatbot Assistant
st.subheader("💬 Ask the Market Assistant")
user_question = st.chat_input("Ask something about the ETF or market today...")

# Function to fetch recent market news headlines from a free open-source API (Finviz RSS)
def fetch_market_news():
    try:
        url = "https://finviz.com/feed.ashx"
        res = requests.get(url)
        if res.status_code == 200:
            from xml.etree import ElementTree as ET
            root = ET.fromstring(res.content)
            return [item.find("title").text for item in root.findall("channel/item")[:3]]
    except:
        return []

if user_question:
    first_price = data["Close"].iloc[0]
    latest_price = data["Close"].iloc[-1]
    price_change = latest_price - first_price
    percent_change = (price_change / first_price) * 100
    time_now = datetime.now().strftime("%H:%M")
    news = fetch_market_news()

    if "buy" in user_question.lower():
        response = "📊 The ETF is " + ("up" if price_change > 0 else "down") + f" {percent_change:.2f}% today. Buying now depends on your goals. Cost averaging is often a good long-term strategy."
    elif "why" in user_question.lower() and "down" in user_question.lower():
        reason = "Could be due to weak earnings or macroeconomic concerns."
        response = f"📉 The ETF is down {percent_change:.2f}% today. {reason}"
    elif "why" in user_question.lower() and "up" in user_question.lower():
        reason = "Likely due to investor optimism or strong economic indicators."
        response = f"📈 The ETF is up {percent_change:.2f}% today. {reason}"
    else:
        response = f"As of {time_now}, the ETF is trading at R{latest_price:.2f} ({percent_change:.2f}% change today)."

    if news:
        response += "\n\n🗞️ Top News Headlines:\n- " + "\n- ".join(news)

    st.chat_message("assistant").write(response)
