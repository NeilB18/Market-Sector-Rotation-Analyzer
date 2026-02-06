import plotly.express as px

def animate_sector_rotation(rotation_frames_df):
    """
    rotation_frames_df columns:
    ['date', 'sector', 'ret_short', 'rel_strength', 'volatility',
     'ret_medium', 'performance']
    """

    fig = px.scatter_3d(
        rotation_frames_df,
        x="ret_short",
        y="rel_strength",
        z="volatility",
        animation_frame="date",
        animation_group="sector",
        color="performance",
        size="size",
        text="sector",
        color_discrete_map={
            "Outperforming": "green",
            "Neutral": "gray",
            "Underperforming": "red"
        },
        title="Sector Rotation Over Time (Money Flow)",
        labels={
            "ret_short": "Short-Term Return",
            "rel_strength": "Relative Strength",
            "volatility": "Volatility",
            "performance": "Performance"
        },
        hover_data={"sector": True, "ret_medium": True}
    )

    fig.update_traces(marker=dict(opacity=0.85))
    fig.update_layout(
        width=1200,
        height=1000,
        template="plotly_dark",
        legend_title="Cluster Performance"
    )

    fig.show()