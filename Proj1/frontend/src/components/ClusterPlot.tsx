import React from "react";
import Plot from "react-plotly.js";
import { type Cluster } from "../api/client";

interface ClusterPlotProps {
  clusters: Cluster[];
}

const ClusterPlot: React.FC<ClusterPlotProps> = ({ clusters }) => {
  if (!clusters || clusters.length === 0)
    return <p style={{ color: "white" }}>No cluster data available</p>;

  const x = clusters.map((c) => c.ret_short);
  const y = clusters.map((c) => c.rel_strength);
  const z = clusters.map((c) => c.volatility);
  const color = clusters.map((c) =>
    c.performance === "Outperforming"
      ? "green"
      : c.performance === "Underperforming"
      ? "red"
      : "gray"
  );
  const text = clusters.map((c) => c.sector);

  return (
    <Plot
      data={[
        {
          x,
          y,
          z,
          text,
          type: "scatter3d",
          mode: "markers+text",
          marker: {
            size: 8,
            color,
          },
        },
      ]}
      layout={{
        title: "Sector Clusters (K-Means)",
        scene: {
          xaxis: { title: "Short-Term Return" },
          yaxis: { title: "Relative Strength" },
          zaxis: { title: "Volatility" },
        },
        font: { color: "white" },
        paper_bgcolor: "#222",
        plot_bgcolor: "#222",
      }}
      style={{ width: "100vh", height: "100vh"}}
    />
  );
};

export default ClusterPlot;