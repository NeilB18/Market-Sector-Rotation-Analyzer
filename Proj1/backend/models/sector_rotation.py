import pandas as pd
from typing import Dict, List
from models.kmeans import SectorKMeans
from features.feature_engineering import build_feature_matrix


class SectorRotationModel:
    def __init__(self, window_size=30, n_clusters=3):
        self.window_size = window_size
        self.n_clusters = n_clusters
        self.kmeans = SectorKMeans(n_clusters=n_clusters)

        # date -> {sector -> performance_label}
        self.cluster_history: Dict[str, Dict[str, str]] = {}

        # List of detected rotations
        self.rotations: List[dict] = []

    def run(self, sector_prices: pd.DataFrame, market_prices: pd.DataFrame):
        """
        Main pipeline: builds rolling windows, clusters each window,
        stores history, and detects rotations.
        """

        dates = sector_prices.index

        for i in range(self.window_size, len(dates)):
            end_date = dates[i]
            window_data = sector_prices.iloc[i - self.window_size:i]

            # 1. Build features for this window
            features = build_feature_matrix(window_data, market_prices.loc[window_data.index])

            # 2. Cluster
            clustered_df = self.kmeans.get_clustered_dataframe(features)
            clustered_df = self.kmeans.label_clusters_by_performance(clustered_df)

            # 3. Store snapshot
            snapshot = clustered_df["performance"].to_dict()
            self.cluster_history[str(end_date.date())] = snapshot

        # 4. Detect rotations after building history
        self._detect_rotations()

        return self.cluster_history, self.rotations

    def _detect_rotations(self):
        """
        Compare consecutive snapshots to detect sector movement
        """
        dates = list(self.cluster_history.keys())

        for i in range(1, len(dates)):
            prev_date = dates[i - 1]
            curr_date = dates[i]

            prev_snapshot = self.cluster_history[prev_date]
            curr_snapshot = self.cluster_history[curr_date]

            for sector in curr_snapshot:
                prev_label = prev_snapshot.get(sector)
                curr_label = curr_snapshot.get(sector)

                if prev_label != curr_label:
                    rotation = {
                        "date": curr_date,
                        "sector": sector,
                        "from": prev_label,
                        "to": curr_label,
                        "direction": self._classify_direction(prev_label, curr_label)
                    }
                    self.rotations.append(rotation)

    def _classify_direction(self, from_label: str, to_label: str) -> str:
        """
        Classify rotation direction: IN / OUT / NEUTRAL
        """
        order = {
            "Underperforming": 0,
            "Neutral": 1,
            "Outperforming": 2
        }

        if from_label is None or to_label is None:
            return "Unknown"

        if order[to_label] > order[from_label]:
            return "Rotation IN"
        elif order[to_label] < order[from_label]:
            return "Rotation OUT"
        else:
            return "No Change"