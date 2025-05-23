#!/bin/bash

# --- USER CONFIGURATION ---
GITHUB_USERNAME="your-github-username"
REPO_NAME="etf-tracker"
ACCESS_TOKEN="ghp_your_github_token_here"

# --- SETUP PROJECT DIRECTORY ---
mkdir etf_tracker_app && cd etf_tracker_app

# Create the Streamlit app
cat <<EOF > app.py
import streamlit as st
import yfinance as yf

st.set_page_config(page_title=\"Satrix S&P 500 Tracker\", layout=\"centered\")
st.title(\"📈 Satrix S&P 500 ETF Tracker\")

ticker = yf.Ticker(\"IVV\")
data = ticker.history(period=\"1d\", interval=\"5m\")

st.subheader(\"Today's Price Movement\")
st.line_chart(data[\"Close\"])

st.subheader(\"What’s happening?\")
if data[\"Close\"][-1] > data[\"Close\"][0]:
    st.success(\"✅ ETF is trending up. Likely due to market optimism or strong earnings.\")
else:
    st.warning(\"⚠️ ETF is down today. Could be due to market uncertainty or negative news.\")

st.subheader(\"💰 Profit Estimator\")
amount = st.number_input(\"How much did you invest (R)?\", value=500.0)
buy_price = st.number_input(\"Price you bought at (R)?\", value=90.0)
current_price = data[\"Close\"][-1]
units = amount / buy_price
value_now = units * current_price
profit = value_now - amount

st.metric(\"Current ETF Price\", f\"R{current_price:.2f}\")
st.metric(\"Your Investment Value\", f\"R{value_now:.2f}\", delta=f\"R{profit:.2f}\")

st.info(\"Tip: Use trends to decide when to add more (buy dips) or sell (take profit).\")
EOF

# Create requirements.txt
echo -e "streamlit\nyfinance" > requirements.txt

# --- INITIALIZE GIT REPO ---
git init
git config user.name "$GITHUB_USERNAME"
git config user.email "${GITHUB_USERNAME}@users.noreply.github.com"
git add .
git commit -m "Initial commit for ETF tracker app"

# --- CREATE GITHUB REPO VIA API ---
curl -u "$GITHUB_USERNAME:$ACCESS_TOKEN" https://api.github.com/user/repos -d "{\"name\":\"$REPO_NAME\"}"

# --- PUSH TO GITHUB ---
git branch -M main
git remote add origin https://$ACCESS_TOKEN@github.com/$GITHUB_USERNAME/$REPO_NAME.git
git push -u origin main

# --- FINAL MESSAGE ---
echo "✅ App pushed to GitHub!"
echo "👉 Visit https://streamlit.io/cloud to deploy your app"
