"use client";
import { useState } from "react";

export default function Leads() {
  const api = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080/api";
  const [resp, setResp] = useState<any>(null);

  const score = async () => {
    const body = { company: "Acme Corp", industry: "Software", signals: { intent: 3.2, hiring: 1.1, techfit: 2.4 } };
    const r = await fetch(`${api}/leads/quantum-scoring`, { method: "POST", body: JSON.stringify(body), headers: { "Content-Type": "application/json" }});
    setResp(await r.json());
  };

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>Lead Generation (Quantum Scoring)</h1>
      <button onClick={score}>Score Example Lead</button>
      <pre style={{ background: "#fafafa", padding: 16, borderRadius: 12, overflow: "auto" }}>
        {JSON.stringify(resp, null, 2)}
      </pre>
    </div>
  );
}
