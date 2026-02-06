import pandas as pd
import yfinance as yf
SECTORS = {
    "Technology": "XLK",
    "Financials": "XLF",
    "Energy": "XLE",
    "Healthcare": "XLV",
    "ConsumerDiscretionary": "XLY",
    "ConsumerStaples": "XLP",
    "Industrials": "XLI",
    "Materials": "XLB",
    "Utilities": "XLU",
    "RealEstate": "XLRE"
}

MARKET_TICKER = "SPY"

def get_sector_prices(period="6mo"):
    data = {}

    for sector, ticker in SECTORS.items():
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)

        # Safety check
        if df.empty:
            print(f"⚠️ No data for {sector} ({ticker}), skipping.")
            continue

        if "Close" in df.columns:
            series = df["Close"]
        # FORCE single-level columns
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        series = df["Close"].dropna()
        data[sector] = series

    sector_prices = pd.concat(data, axis=1)
    sector_prices.index.name = "Date"

    return sector_prices

def get_market_prices(period="6mo"):
    df = yf.download(MARKET_TICKER, period=period, progress=False, auto_adjust=True)

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    prices = df["Close"].dropna()
    prices.index.name = "Date"

    return prices