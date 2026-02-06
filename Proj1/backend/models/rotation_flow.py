import pandas as pd
import plotly.graph_objects as go
from data.dataGetter import get_sector_prices, get_market_prices
# -----------------------------
# Core Calculations
# -----------------------------

def compute_sector_returns(sector_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily returns for each sector.
    """
    returns = sector_prices.pct_change().dropna()
    return returns

def compute_relative_strength(sector_returns: pd.DataFrame, market_returns: pd.Series) -> pd.DataFrame:
    """
    Relative strength = sector return minus market return.
    """
    aligned_market = market_returns.reindex(sector_returns.index)
    rel_strength = sector_returns.sub(aligned_market, axis=0)
    return rel_strength

def compute_rolling_strength(rel_strength: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    """
    Compute rolling mean of relative strength.
    Reduced default window to 5 for more responsiveness.
    """
    rolling = rel_strength.rolling(window=window).mean().dropna()
    return rolling

def compute_rotation_flow(rolling_strength: pd.DataFrame) -> pd.DataFrame:
    """
    Detect capital rotation between consecutive rolling windows using rank changes.
    
    Returns a DataFrame with columns: source, target, weight
    """
    flows = []

    dates = rolling_strength.index
    sectors = rolling_strength.columns

    for i in range(1, len(dates)):
        prev = rolling_strength.iloc[i - 1]
        curr = rolling_strength.iloc[i]

        # Rank sectors by relative strength
        prev_rank = prev.rank(ascending=False)
        curr_rank = curr.rank(ascending=False)

        # Compute rank change (positive = improved, negative = declined)
        rank_change = curr_rank - prev_rank

        # Sectors that gained relative strength
        gaining = rank_change[rank_change < 0].sort_values()  # rank decreased → moved up
        # Sectors that lost relative strength
        losing = rank_change[rank_change > 0].sort_values(ascending=False)  # rank increased → moved down

        # Pair losing → gaining sectors
        for loser in losing.index:
            for gainer in gaining.index:
                weight = min(losing[loser], -gaining[gainer])  # use magnitude of rank change
                if weight > 0:
                    flows.append({
                        "source": loser,
                        "target": gainer,
                        "weight": float(weight)
                    })

    flow_df = pd.DataFrame(flows)
    if flow_df.empty:
        return pd.DataFrame(columns=["source", "target", "weight"])
    
    # Aggregate duplicate flows
    flow_df = flow_df.groupby(["source", "target"], as_index=False)["weight"].sum()

    return flow_df

# -----------------------------
# Visualization
# -----------------------------

def plot_sector_to_sector_sankey(flow_df: pd.DataFrame):
    """
    Plot a Sankey diagram from a rotation flow DataFrame.
    """
    sector_returns = compute_sector_returns(get_sector_prices())
    market_returns = get_market_prices().pct_change().dropna()
    rel_strength = compute_relative_strength(sector_returns, market_returns)
    flows = []
    rolling_strength = compute_rolling_strength(rel_strength, window=5)

    for i in range(1, len(rolling_strength)):
        prev = rolling_strength.iloc[i-1]
        curr = rolling_strength.iloc[i]

        # Rank sectors
        prev_rank = prev.rank(ascending=False)
        curr_rank = curr.rank(ascending=False)

        # Rank changes
        rank_change = prev_rank - curr_rank  # positive = gained
        gained = rank_change[rank_change > 0]
        lost = rank_change[rank_change < 0]

        for src in lost.index:
            for tgt in gained.index:
                weight = abs(rank_change[src]) + rank_change[tgt]  # sum of magnitude
                flows.append({"source": src, "target": tgt, "weight": float(weight)})

    flow_df = pd.DataFrame(flows)
    flow_df = flow_df.groupby(["source", "target"], as_index=False).sum()
    return flow_df