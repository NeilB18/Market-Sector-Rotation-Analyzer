import pandas as pd


def compute_returns(prices, window):
    """
    prices: DataFrame (dates x sectors)
    window: int (e.g. 30, 90)
    Returns % change over window
    """
    return prices.pct_change(window)


def compute_volatility(prices, window=30):
    """
    Rolling volatility (std dev of daily returns)
    """
    daily_returns = prices.pct_change()
    return daily_returns.rolling(window).std()


def compute_relative_strength(sector_prices, market_prices, window=30):
    sector_ret = sector_prices.pct_change(window)

    # Flatten MultiIndex columns if present
    if isinstance(sector_ret.columns, pd.MultiIndex):
        sector_ret.columns = sector_ret.columns.get_level_values(1)

    market_ret = market_prices.pct_change(window)

    # Align index
    market_ret = market_ret.reindex(sector_ret.index).ffill()

    relative_strength = sector_ret.sub(market_ret, axis=0)

    return relative_strength


def build_feature_matrix(sector_prices, market_prices):
    """
    Returns a DataFrame where:
    rows = sectors
    columns = features
    """

    # Dynamically choose windows based on available data
    max_len = len(sector_prices)

    w1 = min(30, max_len - 1)
    w2 = min(90, max_len - 1)

    ret_30 = compute_returns(sector_prices, w1).iloc[-1]
    ret_90 = compute_returns(sector_prices, w2).iloc[-1]
    vol_30 = compute_volatility(sector_prices, w1).iloc[-1]
    rel_str = compute_relative_strength(sector_prices, market_prices, w1).iloc[-1]

    features = pd.DataFrame({
        "ret_short": ret_30,
        "ret_medium": ret_90,
        "volatility": vol_30,
        "rel_strength": rel_str
    })

    # Only drop rows where ALL values are NaN
    features = features.dropna(how="all")

    return features

def standardize_features(feature_matrix):
    """
    Standardizes the feature matrix (z-score normalization)
    """
    standardized = (feature_matrix - feature_matrix.mean()) / feature_matrix.std()
    return standardized