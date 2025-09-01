import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Home() {
  return (
    <>
      <Header />
      <main className="max-w-6xl mx-auto p-8">
        <h1 className="text-4xl font-bold">FLYFOX AI — NQBA Unified Dashboard</h1>
        <p className="mt-4 text-gray-700">Phase 2: Unified Dashboard + Integrations + Quantum Security</p>

        <section className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Unified Dashboard</h3>
            <p className="text-sm text-gray-600">Cross-pillar KPIs and real-time analytics.</p>
            <Link href="/dashboard"><a className="text-indigo-600">Open Dashboard →</a></Link>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Integrations</h3>
            <p className="text-sm text-gray-600">UiPath, n8n, Mendix, Prismatic adapters & MCP plugins.</p>
            <Link href="/integrations"><a className="text-indigo-600">Manage Integrations →</a></Link>
          </div>
          <div className="p-4 border rounded">
            <h3 className="font-semibold">Quantum Security</h3>
            <p className="text-sm text-gray-600">Quantum-anchored key rotation and compliance tooling.</p>
            <Link href="/security"><a className="text-indigo-600">Security →</a></Link>
          </div>
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-bold mb-4">Performance Metrics</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="p-4 bg-blue-50 rounded">
              <div className="text-2xl font-bold text-blue-600">410x</div>
              <div className="text-sm text-gray-600">Performance Multiplier</div>
            </div>
            <div className="p-4 bg-green-50 rounded">
              <div className="text-2xl font-bold text-green-600">24.7%</div>
              <div className="text-sm text-gray-600">Conversion Rate</div>
            </div>
            <div className="p-4 bg-purple-50 rounded">
              <div className="text-2xl font-bold text-purple-600">1150%</div>
              <div className="text-sm text-gray-600">ROI</div>
            </div>
            <div className="p-4 bg-orange-50 rounded">
              <div className="text-2xl font-bold text-orange-600">99.9%</div>
              <div className="text-sm text-gray-600">Uptime</div>
            </div>
          </div>
        </section>

        <section className="mt-12">
          <h2 className="text-2xl font-bold mb-4">Core Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-6 border rounded">
              <h3 className="text-xl font-semibold mb-2">🎯 Unified Dashboard</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Cross-pillar KPIs and real-time analytics</li>
                <li>• Goliath Financial + FLYFOX AI + Sigma Select integration</li>
                <li>• Quantum-enhanced performance metrics</li>
                <li>• Real-time data visualization</li>
              </ul>
            </div>
            <div className="p-6 border rounded">
              <h3 className="text-xl font-semibold mb-2">🔌 Integrations Hub</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• UiPath: RPA orchestration for back-office automation</li>
                <li>• n8n: Low-code workflow orchestration</li>
                <li>• Mendix: Enterprise app rapid development</li>
                <li>• Prismatic: SaaS integrations platform</li>
              </ul>
            </div>
            <div className="p-6 border rounded">
              <h3 className="text-xl font-semibold mb-2">🔐 Quantum Security</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Quantum-anchored key rotation (Dynex-backed)</li>
                <li>• Envelope encryption and field-level encryption</li>
                <li>• Compliance tooling and audit logs</li>
                <li>• Role-based access control (RBAC)</li>
              </ul>
            </div>
            <div className="p-6 border rounded">
              <h3 className="text-xl font-semibold mb-2">🚀 Self-Evolving Q-Sales Division™</h3>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Agent pod orchestration and management</li>
                <li>• Self-improvement loops with Dynex QUBO optimization</li>
                <li>• Performance monitoring and evolution cycles</li>
                <li>• Hyperion scaling engine integration</li>
              </ul>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}
