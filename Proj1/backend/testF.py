from data.dataGetter import get_sector_prices, get_market_prices
from features.feature_engineering import build_feature_matrix
from models.kmeans import SectorKMeans


sector_prices = get_sector_prices()
market_prices = get_market_prices()

features = build_feature_matrix(sector_prices, market_prices)

kmeans = SectorKMeans(n_clusters=3)
clustered_df = kmeans.get_clustered_dataframe(features)
clustered_df = kmeans.label_clusters_by_performance(clustered_df)

kmeans.plot_clusters(clustered_df)

from data.dataGetter import get_sector_prices, get_market_prices
from models.rotation_frame_builder import build_rotation_frames
from visualization.rotation_animation import animate_sector_rotation

sector_prices = get_sector_prices()
market_prices = get_market_prices()

rotation_frames_df = build_rotation_frames(sector_prices, market_prices, window_size=30)

animate_sector_rotation(rotation_frames_df)