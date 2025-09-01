export default function Metric({ label, value, hint }:{label:string,value:string|number,hint?:string}) {
  return (
    <div style={{ padding: 16, border: "1px solid #eee", borderRadius: 12 }}>
      <div style={{ fontSize: 12, opacity: .7 }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 700 }}>{value}</div>
      {hint && <div style={{ fontSize: 12, opacity: .6 }}>{hint}</div>}
    </div>
  );
}
