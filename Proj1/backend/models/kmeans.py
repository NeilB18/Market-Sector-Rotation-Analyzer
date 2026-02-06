import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
class SectorKMeans:
    def __init__(self, n_clusters=3, random_state=42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)

    def fit(self, feature_df: pd.DataFrame):
        """
        feature_df: rows = sectors, columns = features
        """

        # 1. Standardize features (Z-score)
        scaled_features = self.scaler.fit_transform(feature_df)

        # 2. Fit K-Means
        self.model.fit(scaled_features)

        return self

    def predict(self, feature_df: pd.DataFrame):
        """
        Returns cluster labels for each sector
        """

        scaled_features = self.scaler.transform(feature_df)
        labels = self.model.predict(scaled_features)

        return labels

    def fit_predict(self, feature_df: pd.DataFrame):
        """
        Convenience method: fit + predict
        """

        scaled_features = self.scaler.fit_transform(feature_df)
        labels = self.model.fit_predict(scaled_features)

        return labels

    def get_clustered_dataframe(self, feature_df: pd.DataFrame):
        """
        Returns feature_df with an added 'cluster' column
        """

        labels = self.fit_predict(feature_df)

        clustered_df = feature_df.copy()
        clustered_df["cluster"] = labels

        return clustered_df

    def get_cluster_centers(self, feature_df: pd.DataFrame):
        """
        Returns cluster centers in original feature scale
        """

        scaled_centers = self.model.cluster_centers_
        centers = self.scaler.inverse_transform(scaled_centers)

        centers_df = pd.DataFrame(
            centers,
            columns=feature_df.columns,
            index=[f"Cluster_{i}" for i in range(self.n_clusters)]
        )

        return centers_df

    def label_clusters_by_performance(self,clustered_df):
        """
        Adds a 'performance' column based on mean short-term return per cluster
        """
        cluster_means = clustered_df.groupby("cluster")["ret_short"].mean()
        sorted_clusters = cluster_means.sort_values(ascending=False).index.tolist()
        performance_map = {
            sorted_clusters[0]: "Outperforming",
            sorted_clusters[1]: "Neutral",
            sorted_clusters[2]: "Underperforming"
        }
        clustered_df["performance"] = clustered_df["cluster"].map(performance_map)
        return clustered_df

    def plot_clusters(self, clustered_df: pd.DataFrame):
        if "performance" not in clustered_df.columns:
            clustered_df = self.label_clusters_by_performance(clustered_df)

        df = clustered_df.reset_index().rename(columns={"index": "sector"})

        # Plot 3D scatter
        fig = px.scatter_3d(
            df,
            x="ret_short",
            y="rel_strength",
            z="volatility",
            color="performance",       # use human-readable labels
            text="sector",             # sector names on points
            title="Sector Clusters Labeled by Performance",
            color_discrete_map={
                "Outperforming": "green",
                "Neutral": "yellow",
                "Underperforming": "red"
            },
            labels={
                "ret_short": "Short-Term Return",
                "rel_strength": "Relative Strength",
                "volatility": "Volatility",
                "performance": "Cluster Performance"
            },
            hover_data={"cluster": True, "ret_medium": True}  # optional extra info
        )

        fig.update_traces(marker=dict(size=8), textposition="top center")
        fig.update_layout(
            width=1000,
            height=800,
            template="plotly_dark",
            legend_title="Performance"
        )

        fig.show()
        fig.update_layout(template="plotly_dark")