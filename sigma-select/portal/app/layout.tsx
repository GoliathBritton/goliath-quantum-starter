export const metadata = {
  title: "FLYFOX AI — Sigma Select",
  description: "Quantum-accelerated revenue engine by FLYFOX AI (Dynex-first)"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "ui-sans-serif, system-ui" }}>
        <header style={{ padding: "16px 24px", borderBottom: "1px solid #eee", display: "flex", gap: 16, alignItems: "center" }}>
          <strong>FLYFOX AI</strong>
          <nav style={{ display: "flex", gap: 12 }}>
            <a href="/">Dashboard</a>
            <a href="/sigmaeq">SigmaEQ</a>
            <a href="/leads">Leads</a>
            <a href="/sales">Sales</a>
            <a href="/revenue">Revenue</a>
            <a href="/analytics">Analytics</a>
          </nav>
          <div style={{ marginLeft: "auto", opacity: .7, fontSize: 12 }}>Dynex-first • + NVIDIA Accel</div>
        </header>
        <main style={{ padding: 24 }}>{children}</main>
      </body>
    </html>
  );
}
