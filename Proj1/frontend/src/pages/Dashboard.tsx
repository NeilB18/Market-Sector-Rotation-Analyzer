import React, { useEffect, useState } from "react";
import ClusterPlot from "../components/ClusterPlot";
import SankeyPlot from "../components/SankeyPlot";
import { type Cluster, type RotationFlow, fetchClusters, fetchRotationFlows } from "../api/client";

const Dashboard: React.FC = () => {
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [flows, setFlows] = useState<RotationFlow[]>([]);

  useEffect(() => {
    fetchClusters().then(setClusters);
    fetchRotationFlows().then(setFlows);
  }, []);

  return (
    <div style={{ padding: "20px", backgroundColor: "#222", minHeight: "100vh" , width: "100%", textAlign: "center", display: "flex", flexDirection: "column", alignItems: "center"}}>
      <h1 style={{ color: "white", marginBottom: "20px" }}>Sector Dashboard</h1>

      <section style={{ marginBottom: "60px" }}>
        <h2 style={{ color: "white" }}>Sector Clusters</h2>
        <ClusterPlot clusters={clusters} />
      </section>

      <section>
        <h2 style={{ color: "white" }}>Sector Rotation</h2>
        <SankeyPlot flows={flows} />
      </section>
    </div>
  );
};

export default Dashboard;