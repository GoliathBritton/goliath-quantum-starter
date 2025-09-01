"use client";
import { useState } from "react";
export default function Revenue() {
  const api = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8080/api";
  const [resp, setResp] = useState<any>(null);
  const optimize = async () => {
    const r = await fetch(`${api}/revenue/optimization?product_id=SKU-999`, { method: "POST" });
    setResp(await r.json());
  };
  return (
    <div style={{ display: "grid", gap: 16 }}>
      <h1>Revenue Optimization</h1>
      <button onClick={optimize}>Optimize Pricing</button>
      <pre style={{ background: "#fafafa", padding: 16, borderRadius: 12 }}>{JSON.stringify(resp, null, 2)}</pre>
    </div>
  );
}
