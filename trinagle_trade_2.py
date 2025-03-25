import streamlit as st
import yfinance as yf
import pandas as pd

def get_latest_price(ticker):
    """
    Downloads the most recent 1-day data with 1-minute intervals and returns the last closing price.
    """
    data = yf.download(ticker, period="1d", interval="1m")
    # Ensure data is not empty
    if data.empty:
        raise ValueError(f"No data returned for {ticker}.")
    return data['Close'].iloc[-1].item()  # Ensure to return a scalar value

def get_rate(from_currency, to_currency):
    """
    Try to get the direct exchange rate for from_currency -> to_currency.
    If not available, try to get the inverse rate.
    """
    ticker = f"{from_currency}{to_currency}=X"
    try:
        rate = get_latest_price(ticker)
    except ValueError:
        rate = None

    if rate is None or pd.isna(rate):  # check for NaN
        # Try the inverse ticker and take reciprocal
        inv_ticker = f"{to_currency}{from_currency}=X"
        try:
            inv_rate = get_latest_price(inv_ticker)
        except ValueError:
            inv_rate = None

        if inv_rate is None or pd.isna(inv_rate):
            return None
        return 1 / inv_rate
    return rate

st.title("Triangle Arbitrage Calculator")

# Define a list of currencies available for selection.
currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD"]

st.write("Select three currencies to form a triangle arbitrage cycle: A → B → C → A.")

col1, col2, col3 = st.columns(3)
with col1:
    currency_A = st.selectbox("Currency A (start/end)", currencies, index=0)
with col2:
    currency_B = st.selectbox("Currency B (middle)", currencies, index=1)
with col3:
    currency_C = st.selectbox("Currency C (middle)", currencies, index=2)

if currency_A == currency_B or currency_B == currency_C or currency_C == currency_A:
    st.error("Please select three different currencies.")
else:
    st.write(f"You selected the triangle: {currency_A} → {currency_B} → {currency_C} → {currency_A}")

    # Retrieve the exchange rates for each leg of the cycle.
    rate_AB = get_rate(currency_A, currency_B)
    rate_BC = get_rate(currency_B, currency_C)
    rate_CA = get_rate(currency_C, currency_A)

    if rate_AB is None or rate_BC is None or rate_CA is None:
        st.error("Could not retrieve one or more exchange rates. Try different currency selections.")
    else:
        st.write(f"Exchange rate {currency_A} → {currency_B}: {rate_AB}")
        st.write(f"Exchange rate {currency_B} → {currency_C}: {rate_BC}")
        st.write(f"Exchange rate {currency_C} → {currency_A}: {rate_CA}")

        # Compute the triangle arbitrage product.
        triangle_product = rate_AB * rate_BC * rate_CA
        st.write(f"Triangle arbitrage product: {triangle_product}")

        # Allow the user to set the threshold for detecting an arbitrage opportunity.
      