// frontend/src/components/SankeyPlot.tsx
import React from "react";
import Plot from "react-plotly.js";
import { type RotationFlow } from "../api/client";

interface SankeyPlotProps {
  flows: RotationFlow[];
}

const SankeyPlot: React.FC<SankeyPlotProps> = ({ flows }) => {
  if (!flows || flows.length === 0)
    return <p style={{ color: "white" }}>No rotation flow data</p>;

  const labels = Array.from(
    new Set([...flows.map((f) => f.source), ...flows.map((f) => f.target)])
  );
  const labelToIndex: Record<string, number> = {};
  labels.forEach((l, i) => (labelToIndex[l] = i));

  const data = [
    {
      type: "sankey",
      orientation: "h",
      node: {
        pad: 20,
        thickness: 25,
        line: { color: "black", width: 0.5 },
        label: labels,
      },
      link: {
        source: flows.map((f) => labelToIndex[f.source]),
        target: flows.map((f) => labelToIndex[f.target]),
        value: flows.map((f) => f.weight),
      },
    },
  ];

  return (
    <Plot
      data={data}
      layout={{
        title: "Sector Rotation – Capital Flow",
        font: { color: "white" },
        paper_bgcolor: "#222",
        plot_bgcolor: "#222",
      }}
      style={{ width: "100%", height: "600px" }}
    />
  );
};

export default SankeyPlot;