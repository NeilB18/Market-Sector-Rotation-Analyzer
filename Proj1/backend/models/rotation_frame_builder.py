import pandas as pd
from features.feature_engineering import build_feature_matrix
from models.kmeans import SectorKMeans

def build_rotation_frames(sector_prices, market_prices, window_size=30):
    kmeans = SectorKMeans(n_clusters=3)
    frames = []

    dates = sector_prices.index

    for i in range(window_size, len(dates)):
        end_date = dates[i]
        window_data = sector_prices.iloc[i - window_size:i]

        features = build_feature_matrix(window_data, market_prices.loc[window_data.index])
        clustered_df = kmeans.get_clustered_dataframe(features)
        clustered_df = kmeans.label_clusters_by_performance(clustered_df)

        # --- SCALE ret_medium for bubble size (CRITICAL FIX) ---
        min_size = 6
        max_size = 40

        ret_med = clustered_df["ret_medium"]
        size_scaled = (ret_med - ret_med.min()) / (ret_med.max() - ret_med.min())
        clustered_df["size"] = size_scaled * (max_size - min_size) + min_size

        clustered_df["date"] = str(end_date.date())
        clustered_df["sector"] = clustered_df.index

        frames.append(clustered_df.reset_index(drop=True))

    rotation_frames_df = pd.concat(frames, ignore_index=True)
    return rotation_frames_df