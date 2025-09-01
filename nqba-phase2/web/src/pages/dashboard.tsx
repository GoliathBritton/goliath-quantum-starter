"use client";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";

interface KPIMetric {
  name: string;
  value: number;
  unit: string;
  trend: string;
  change_percent: number;
}

interface DashboardData {
  kpis: Record<string, KPIMetric>;
  quantum_jobs_running: number;
  last_updated: string;
}

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch('http://localhost:8000/v2/dashboard/overview');
      const data = await response.json();
      setDashboardData(data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <>
        <Header />
        <main className="max-w-6xl mx-auto p-8">
          <div className="text-center">Loading dashboard...</div>
        </main>
        <Footer />
      </>
    );
  }

  return (
    <>
      <Header />
      <main className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Unified Dashboard</h1>
          <p className="text-gray-600">Cross-pillar KPIs and real-time analytics</p>
        </div>

        {dashboardData && (
          <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {Object.entries(dashboardData.kpis).map(([key, kpi]) => (
                <div key={key} className="bg-white p-6 rounded-lg shadow border">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-gray-600">{kpi.name}</p>
                      <p className="text-2xl font-bold">
                        {kpi.value.toLocaleString()}{kpi.unit !== 'count' && kpi.unit !== 'x' && kpi.unit !== '%' ? ` ${kpi.unit}` : kpi.unit === 'x' ? 'x' : kpi.unit === '%' ? '%' : ''}
                      </p>
                    </div>
                    <div className={`text-sm ${kpi.trend === 'up' ? 'text-green-600' : kpi.trend === 'down' ? 'text-red-600' : 'text-gray-600'}`}>
                      {kpi.trend === 'up' ? '↗' : kpi.trend === 'down' ? '↘' : '→'} {kpi.change_percent}%
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Quantum Performance */}
            <div className="bg-white p-6 rounded-lg shadow border mb-8">
              <h2 className="text-xl font-semibold mb-4">Quantum Performance</h2>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">410x</div>
                  <div className="text-sm text-gray-600">Performance Multiplier</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-green-600">{dashboardData.quantum_jobs_running}</div>
                  <div className="text-sm text-gray-600">Active Jobs</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-purple-600">Dynex</div>
                  <div className="text-sm text-gray-600">Quantum Backend</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">99.9%</div>
                  <div className="text-sm text-gray-600">Uptime</div>
                </div>
              </div>
            </div>

            {/* Pillar Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-lg font-semibold mb-4">Goliath Financial</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Total Assets</span>
                    <span className="font-medium">$12.5M</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Active Loans</span>
                    <span className="font-medium">47</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Default Rate</span>
                    <span className="font-medium">2.1%</span>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-lg font-semibold mb-4">FLYFOX AI</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Agents Deployed</span>
                    <span className="font-medium">156</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Optimizations</span>
                    <span className="font-medium">89</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Decisions</span>
                    <span className="font-medium">1,247</span>
                  </div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow border">
                <h3 className="text-lg font-semibold mb-4">Sigma Select</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Leads Scored</span>
                    <span className="font-medium">892</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">QEI Score</span>
                    <span className="font-medium">0.87</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-gray-600">Revenue</span>
                    <span className="font-medium">$187.5K</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="text-sm text-gray-500 text-center">
              Last updated: {new Date(dashboardData.last_updated).toLocaleString()}
            </div>
          </>
        )}
      </main>
      <Footer />
    </>
  );
}
