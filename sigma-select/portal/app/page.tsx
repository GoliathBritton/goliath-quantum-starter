"use client";

import { useEffect, useState } from "react";
import Metric from "./components/Metric";

export default function Dashboard() {
  const [health, setHealth] = useState<any>(null);
  const api = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080";

  useEffect(() => {
    fetch(`${api}/health`).then(r => r.json()).then(setHealth).catch(()=>{});
  }, []);

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>Unified Quantum Dashboard</h1>
      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))" }}>
        <Metric label="Quantum Backend" value={health?.quantum_backend ?? "—"} hint="Dynex preferred" />
        <Metric label="NVIDIA Acceleration" value={String(!!health?.nvidia_accel)} />
        <Metric label="Performance Multiplier" value={`${health?.multiplier ?? "—"}x`} hint="Dynex + NVIDIA" />
        <Metric label="API" value={health ? "Online" : "—"} />
      </div>
    </div>
  );
}
