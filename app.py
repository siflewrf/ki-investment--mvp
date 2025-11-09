import streamlit as st
import pandas as pd
import requests
import plotly.express as px

st.set_page_config(page_title="KI Invest MVP", layout="wide")

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {"vs_currency": "eur", "order": "market_cap_desc", "per_page": 10, "page": 1}

def fetch_crypto_data():
    try:
        response = requests.get(COINGECKO_URL, params=PARAMS)
        data = response.json()
        df = pd.DataFrame(data)
        return df[["symbol", "current_price", "price_change_percentage_24h"]]
    except Exception as e:
        st.error(f"Fehler beim Abrufen: {e}")
        return pd.DataFrame()

st.title("KI Invest MVP – Simulation & Marktanalyse")
st.write("Einfaches FinTech-Dashboard mit Live-Daten und Rendite-Simulation.")

df = fetch_crypto_data()
if not df.empty:
    st.subheader("Live Kryptodaten")
    st.dataframe(df)
    st.subheader("Preisentwicklung (Beispiel)")
    fig = px.bar(df, x="symbol", y="current_price", color="price_change_percentage_24h")
    st.plotly_chart(fig)

st.subheader("Simulation")
betrag = st.number_input("Monatlicher Betrag (€)", min_value=10, value=300)
jahre = st.number_input("Zeitraum (Jahre)", min_value=1, value=20)
risiko = st.selectbox("Risiko", ["konservativ", "ausgewogen", "aggressiv"])
rendite = {"konservativ": 0.05, "ausgewogen": 0.08, "aggressiv": 0.12}
rate = rendite[risiko]
endwert = betrag * ((1 + rate)**jahre - 1) / rate
st.write(f"Prognose: Aus {betrag} €/Monat werden ca. {int(endwert):,} € nach {jahre} Jahren.")
