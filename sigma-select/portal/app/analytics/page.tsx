"use client";
import { useState } from "react";
export default function Analytics() {
  const api = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080/api";
  const [resp, setResp] = useState<any>(null);
  const getForecast = async () => {
    const r = await fetch(`${api}/analytics/predictive?horizon_days=30`);
    setResp(await r.json());
  };
  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>Predictive Analytics</h1>
      <button onClick={getForecast}>Get 30-Day Forecast</button>
      <pre style={{ background: "#fafafa", padding: 16, borderRadius: 12 }}>{JSON.stringify(resp, null, 2)}</pre>
    </div>
  );
}
