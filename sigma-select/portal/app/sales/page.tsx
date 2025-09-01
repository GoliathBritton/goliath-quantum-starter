"use client";
import { useState } from "react";
export default function Sales() {
  const api = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080/api";
  const [resp, setResp] = useState<any>(null);
  const run = async () => {
    const r = await fetch(`${api}/sales/automation?deal_id=DEAL-42`, { method: "POST" });
    setResp(await r.json());
  };
  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>Sales Automation</h1>
      <button onClick={run}>Schedule Follow-ups</button>
      <pre style={{ background: "#fafafa", padding: 16, borderRadius: 12 }}>{JSON.stringify(resp, null, 2)}</pre>
    </div>
  );
}
