import yfinance as yf

def get_latest_price(ticker):
    """
    Downloads the most recent 1-day data with 1-minute intervals and returns the last closing price.
    """
    data = yf.download(ticker, period="1d", interval="1m")
    # Ensure data is not empty
    if data.empty:
        raise ValueError(f"No data returned for {ticker}.")
    return data['Close'].iloc[-1].item()  # Ensure to return a scalar value

# Define tickers for the three currency pairs
eur_usd_ticker = "EURUSD=X"  # EUR to USD
gbp_usd_ticker = "GBPUSD=X"  # GBP to USD
eur_gbp_ticker = "EURGBP=X"  # EUR to GBP

# Fetch the latest closing prices
eur_usd = get_latest_price(eur_usd_ticker)
gbp_usd = get_latest_price(gbp_usd_ticker)
eur_gbp = get_latest_price(eur_gbp_ticker)

# Check for NaN values
if any(map(lambda x: x != x, [eur_usd, gbp_usd, eur_gbp])):
    raise ValueError("One of the fetched prices is NaN.")

print(f"EUR/USD: {eur_usd}")
print(f"GBP/USD: {gbp_usd}")
print(f"EUR/GBP: {eur_gbp}")

# Calculate the implied GBP/USD rate from EUR/USD and EUR/GBP
implied_gbp_usd = eur_usd / eur_gbp
print(f"\nMarket GBP/USD: {gbp_usd}")
print(f"Implied GBP/USD (EUR/USD divided by EUR/GBP): {implied_gbp_usd}")

# Compute the mispricing (difference between actual and implied GBP/USD)
mispricing = gbp_usd - implied_gbp_usd
print(f"Mispricing (GBP/USD - Implied GBP/USD): {mispricing}")

# Alternatively, calculate the triangle arbitrage product:
# Starting with 1 USD -> convert to EUR -> then to GBP -> then back to USD should yield ~1 if no arbitrage exists.
# For USD -> EUR: 1 / (EUR/USD)
# For EUR -> GBP: multiply by (EUR/GBP)
# For GBP -> USD: multiply by (GBP/USD)
triangle_value = (gbp_usd * eur_gbp) / eur_usd
print(f"\nTriangle arbitrage product: {triangle_value}")

# Define a threshold for detecting significant mispricing (this value can be adjusted)
