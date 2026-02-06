from fastapi import FastAPI
from data.dataGetter import get_sector_prices, get_market_prices
from features.feature_engineering import build_feature_matrix
from models.kmeans import SectorKMeans
from models.rotation_flow import compute_rotation_flow, compute_relative_strength, compute_rolling_strength, compute_sector_returns
import pandas as pd 

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # adjust port if different
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/clusters")
def get_clusters():
    # sector_prices = get_sector_prices()
    # market_prices = get_market_prices()
    # feature_df = build_feature_matrix(sector_prices, market_prices)  # DataFrame with features
    # kmeans = SectorKMeans()
    # clustered_df = kmeans.label_clusters_by_performance(
    #     kmeans.get_clustered_dataframe(feature_df)
    # )
    # return clustered_df.reset_index().to_dict(orient="records")
        # Get prices
    sector_prices = get_sector_prices()
    market_prices = get_market_prices()

    # Build feature matrix
    feature_df = pd.DataFrame({
        "ret_short": sector_prices.pct_change(30).iloc[-1],  # 30-day return
        "rel_strength": sector_prices.pct_change(30).iloc[-1] - market_prices.pct_change(30).iloc[-1],
        "volatility": sector_prices.pct_change().rolling(30).std().iloc[-1],
    })

    # K-Means
    km = SectorKMeans(n_clusters=3)
    clustered_df = km.get_clustered_dataframe(feature_df)
    clustered_df = km.label_clusters_by_performance(clustered_df)

    # Prepare JSON
    data = []
    for idx, row in clustered_df.iterrows():
        data.append({
            "sector": idx,
            "ret_short": float(row["ret_short"]),
            "rel_strength": float(row["rel_strength"]),
            "volatility": float(row["volatility"]),
            "performance": row["performance"],
            "cluster": int(row["cluster"]),
        })

    return data

@app.get("/rotation")
def get_rotation():
    # Get prices
    sector_prices = get_sector_prices()
    market_prices = get_market_prices()

    # Compute returns
    sector_returns = compute_sector_returns(sector_prices)
    market_returns = market_prices.pct_change().dropna()

    # Compute relative strength (sector vs market)
    rel_strength = compute_relative_strength(sector_returns, market_returns)

    # Compute rolling strength
    rolling_strength = compute_rolling_strength(rel_strength, window=20)

    # Compute rotation flows
    flows = compute_rotation_flow(rolling_strength)

    # Prepare JSON response
    data = []
    for f in flows:
        data.append({
            "source": f["source"],
            "target": f["target"],
            "weight": f["weight"]
        })

    return data
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)