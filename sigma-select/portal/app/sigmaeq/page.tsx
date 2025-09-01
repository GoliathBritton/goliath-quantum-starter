"use client";
import { useState } from "react";
import Metric from "../components/Metric";

export default function SigmaEQ() {
  const api = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080/api";
  const [qei, setQei] = useState<any>(null);
  const [momentum, setMomentum] = useState<any>(null);

  const runQEI = async () => {
    const body = { inputs: { cycle_time: 42, win_rate: 31, acv: 85, cac: 23, ltv: 420 }, window: "7d" };
    const r = await fetch(`${api}/sigmaeq/qei-calculation`, { method: "POST", body: JSON.stringify(body), headers: { "Content-Type": "application/json" }});
    setQei(await r.json());
  };

  const runMomentum = async () => {
    const body = { metrics: { daily_wins: 12, avg_deal_size: 8700, velocity: 2.3 }, window: "7d" };
    const r = await fetch(`${api}/sigmaeq/momentum-tracking`, { method: "POST", body: JSON.stringify(body), headers: { "Content-Type": "application/json" }});
    setMomentum(await r.json());
  };

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>SigmaEQ Revenue Engine</h1>
      <div style={{ display: "flex", gap: 12 }}>
        <button onClick={runQEI}>Run QEI</button>
        <button onClick={runMomentum}>Run Momentum</button>
      </div>
      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))" }}>
        <Metric label="QEI Score" value={qei?.qei_score ?? "—"} hint={qei ? `backend=${qei.quantum_backend} • x${qei.multiplier}` : ""}/>
        <Metric label="Momentum" value={momentum?.momentum ?? "—"} />
      </div>
      <pre style={{ background: "#fafafa", padding: 16, borderRadius: 12, overflow: "auto" }}>
        {JSON.stringify({ qei, momentum }, null, 2)}
      </pre>
    </div>
  );
}
