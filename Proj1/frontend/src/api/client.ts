

export interface Cluster {
  sector: string;
  ret_short: number;
  rel_strength: number;
  volatility: number;
  performance: string;
  cluster: number;
}

export const fetchClusters = async (): Promise<Cluster[]> => {
  try {
    const res = await fetch("http://127.0.0.1:8000/clusters"); // adjust if your backend URL is different
    if (!res.ok) {
      throw new Error(`Failed to fetch clusters: ${res.statusText}`);
    }
    const data: Cluster[] = await res.json();
    return data;
  } catch (err) {
    console.error("Error fetching clusters:", err);
    return [];
  }
};

// frontend/src/api/client.ts
export interface RotationFlow {
  source: string;
  target: string;
  weight: number;
}

export async function fetchRotationFlows(): Promise<RotationFlow[]> {
  try {
    const res = await fetch("http://127.0.0.1:8000/rotation");
    if (!res.ok) throw new Error(res.statusText);
    return await res.json();
  } catch (err) {
    console.error("Error fetching rotation flows:", err);
    return [];
  }
}