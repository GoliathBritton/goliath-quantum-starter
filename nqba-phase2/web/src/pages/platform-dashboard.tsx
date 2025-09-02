import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function PlatformDashboard() {
  const [dashboardData, setDashboardData] = useState({
    systemStatus: {
      overall: "operational",
      flyfox: "operational",
      goliath: "operational",
      sigma: "operational",
      quantum: "operational",
      ai: "operational"
    },
    performance: {
      cpu: 45,
      memory: 62,
      storage: 38,
      network: 78
    },
    security: {
      threats: 0,
      vulnerabilities: 2,
      lastScan: "2 hours ago",
      compliance: "98%"
    },
    businessMetrics: {
      activeUsers: 1247,
      transactions: 8942,
      revenue: "$2.4M",
      growth: "+12.5%"
    }
  });

  const [activeTab, setActiveTab] = useState("overview");
  const [refreshInterval, setRefreshInterval] = useState(30);

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      setDashboardData(prev => ({
        ...prev,
        performance: {
          cpu: Math.max(20, Math.min(80, prev.performance.cpu + (Math.random() - 0.5) * 10)),
          memory: Math.max(30, Math.min(85, prev.performance.memory + (Math.random() - 0.5) * 8)),
          storage: Math.max(25, Math.min(60, prev.performance.storage + (Math.random() - 0.5) * 5)),
          network: Math.max(60, Math.min(95, prev.performance.network + (Math.random() - 0.5) * 12))
        },
        businessMetrics: {
          ...prev.businessMetrics,
          activeUsers: prev.businessMetrics.activeUsers + Math.floor(Math.random() * 10) - 5,
          transactions: prev.businessMetrics.transactions + Math.floor(Math.random() * 50) - 25
        }
      }));
    }, refreshInterval * 1000);

    return () => clearInterval(interval);
  }, [refreshInterval]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "operational": return "text-green-600 bg-green-100";
      case "degraded": return "text-yellow-600 bg-yellow-100";
      case "down": return "text-red-600 bg-red-100";
      default: return "text-gray-600 bg-gray-100";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "operational": return "🟢";
      case "degraded": return "🟡";
      case "down": return "🔴";
      default: return "⚪";
    }
  };

  const tabs = [
    { id: "overview", name: "Overview", icon: "📊" },
    { id: "systems", name: "Systems", icon: "🔧" },
    { id: "security", name: "Security", icon: "🔒" },
    { id: "performance", name: "Performance", icon: "⚡" },
    { id: "business", name: "Business", icon: "💼" }
  ];

  return (
    <>
      <Header />

      {/* Dashboard Header */}
      <section className="bg-gradient-to-r from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h1 className="text-4xl md:text-5xl font-bold mb-4">NQBA Platform Dashboard</h1>
              <p className="text-xl text-gray-300">
                Unified monitoring and control center for the entire NQBA ecosystem
              </p>
            </div>
            <div className="mt-6 lg:mt-0 flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <span className="text-sm">Refresh:</span>
                <select
                  value={refreshInterval}
                  onChange={(e) => setRefreshInterval(Number(e.target.value))}
                  className="bg-white/20 text-white border border-white/30 rounded-lg px-3 py-2 text-sm"
                >
                  <option value={15}>15s</option>
                  <option value={30}>30s</option>
                  <option value={60}>1m</option>
                  <option value={300}>5m</option>
                </select>
              </div>
              <div className={`px-4 py-2 rounded-full text-sm font-semibold ${getStatusColor(dashboardData.systemStatus.overall)}`}>
                {getStatusIcon(dashboardData.systemStatus.overall)} System {dashboardData.systemStatus.overall}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Navigation Tabs */}
      <section className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? "border-flyfox-950 text-flyfox-950"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.name}</span>
              </button>
            ))}
          </nav>
        </div>
      </section>

      {/* Dashboard Content */}
      <section className="py-8 bg-gray-50 min-h-screen">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Overview Tab */}
          {activeTab === "overview" && (
            <div className="space-y-8">
              {/* System Status Grid */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">System Status Overview</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Object.entries(dashboardData.systemStatus).map(([system, status]) => (
                    <div key={system} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900 capitalize">
                          {system === "overall" ? "Overall System" : system}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(status)}`}>
                          {getStatusIcon(status)} {status}
                        </span>
                      </div>
                      <div className="space-y-3">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Uptime</span>
                          <span className="font-medium">99.9%</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Response Time</span>
                          <span className="font-medium">45ms</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Last Check</span>
                          <span className="font-medium">2 min ago</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Performance Metrics */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Performance Metrics</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {Object.entries(dashboardData.performance).map(([metric, value]) => (
                    <div key={metric} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-semibold text-gray-900 capitalize">{metric}</h3>
                        <span className="text-2xl font-bold text-sigma-600">{value}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full transition-all duration-300 ${
                            value > 80 ? "bg-red-500" : value > 60 ? "bg-yellow-500" : "bg-green-500"
                          }`}
                          style={{ width: `${value}%` }}
                        ></div>
                      </div>
                      <p className="text-sm text-gray-600 mt-2">
                        {value > 80 ? "High" : value > 60 ? "Moderate" : "Normal"} usage
                      </p>
                    </div>
                  ))}
                </div>
              </div>

              {/* Quick Actions */}
              <div>
                <h2 className="text-2xl font-bold text-gray-900 mb-6">Quick Actions</h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <Link href="/setup_auth" className="bg-gradient-to-r from-flyfox-950 to-flyfoxSilver-800 text-white p-6 rounded-xl shadow-sm hover:from-flyfox-900 hover:to-flyfoxSilver-700 transition-all">
                    <div className="text-3xl mb-4">🔐</div>
                    <h3 className="text-xl font-semibold mb-2">Configure Authentication</h3>
                    <p className="text-flyfoxSilver-100">Set up unified access control</p>
                  </Link>
                  <Link href="/setup" className="bg-gradient-to-r from-goliathMaize-500 to-goliathMaize-600 text-white p-6 rounded-xl shadow-sm hover:from-goliathMaize-600 hover:to-goliathMaize-700 transition-all">
                    <div className="text-3xl mb-4">⚙️</div>
                    <h3 className="text-xl font-semibold mb-2">System Setup</h3>
                    <p className="text-goliathMaize-100">Configure business units and services</p>
                  </Link>
                  <Link href="/monitoring" className="bg-gradient-to-r from-goliathNavy-600 to-goliathNavy-700 text-white p-6 rounded-xl shadow-sm hover:from-goliathNavy-700 hover:to-goliathNavy-800 transition-all">
                    <div className="text-3xl mb-4">📊</div>
                    <h3 className="text-xl font-semibold mb-2">Advanced Monitoring</h3>
                    <p className="text-goliathNavy-100">Detailed analytics and reporting</p>
                  </Link>
                </div>
              </div>
            </div>
          )}

          {/* Systems Tab */}
          {activeTab === "systems" && (
            <div className="space-y-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">System Management</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Business Units */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Business Units</h3>
                  <div className="space-y-4">
                    {Object.entries(dashboardData.systemStatus).filter(([key]) => 
                      ["flyfox", "goliath", "sigma"].includes(key)
                    ).map(([unit, status]) => (
                      <div key={unit} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">
                            {unit === "flyfox" ? "🦊" : unit === "goliath" ? "🏗️" : "Σ"}
                          </span>
                          <div>
                            <h4 className="font-medium text-gray-900 capitalize">{unit}</h4>
                            <p className="text-sm text-gray-600">Business Unit</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(status)}`}>
                            {getStatusIcon(status)} {status}
                          </span>
                          <button className="text-flyfox-950 hover:text-flyfox-900 text-sm font-medium">
                            Manage
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Core Systems */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Core Systems</h3>
                  <div className="space-y-4">
                    {Object.entries(dashboardData.systemStatus).filter(([key]) => 
                      ["quantum", "ai"].includes(key)
                    ).map(([system, status]) => (
                      <div key={system} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <span className="text-2xl">
                            {system === "quantum" ? "⚛️" : "🤖"}
                          </span>
                          <div>
                            <h4 className="font-medium text-gray-900 capitalize">{system}</h4>
                            <p className="text-sm text-gray-600">Core Technology</p>
                          </div>
                        </div>
                        <div className="flex items-center space-x-3">
                          <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(status)}`}>
                            {getStatusIcon(status)} {status}
                          </span>
                          <button className="text-flyfox-950 hover:text-flyfox-900 text-sm font-medium">
                            Configure
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Security Tab */}
          {activeTab === "security" && (
            <div className="space-y-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Security Overview</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Security Status */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Security Status</h3>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                      <span className="text-green-800 font-medium">Threats Detected</span>
                      <span className="text-2xl font-bold text-green-600">{dashboardData.security.threats}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-yellow-50 rounded-lg">
                      <span className="text-yellow-800 font-medium">Vulnerabilities</span>
                      <span className="text-2xl font-bold text-yellow-600">{dashboardData.security.vulnerabilities}</span>
                    </div>
                    <div className="flex justify-between items-center p-4 bg-blue-50 rounded-lg">
                      <span className="text-blue-800 font-medium">Compliance Score</span>
                      <span className="text-2xl font-bold text-blue-600">{dashboardData.security.compliance}</span>
                    </div>
                  </div>
                </div>

                {/* Security Actions */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Security Actions</h3>
                  <div className="space-y-3">
                    <button className="w-full bg-red-600 text-white px-4 py-3 rounded-lg hover:bg-red-700 transition-colors">
                      🚨 Emergency Lockdown
                    </button>
                    <button className="w-full bg-yellow-600 text-white px-4 py-3 rounded-lg hover:bg-yellow-700 transition-colors">
                      🔍 Security Scan
                    </button>
                    <button className="w-full bg-blue-600 text-white px-4 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                      📋 Compliance Report
                    </button>
                    <button className="w-full bg-green-600 text-white px-4 py-3 rounded-lg hover:bg-green-700 transition-colors">
                      ✅ Update Security Policies
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Performance Tab */}
          {activeTab === "performance" && (
            <div className="space-y-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Performance Analytics</h2>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Real-time Metrics */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Real-time Performance</h3>
                  <div className="space-y-6">
                    {Object.entries(dashboardData.performance).map(([metric, value]) => (
                      <div key={metric}>
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm font-medium text-gray-700 capitalize">{metric}</span>
                          <span className="text-sm font-bold text-gray-900">{value}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-3">
                          <div
                            className={`h-3 rounded-full transition-all duration-500 ${
                              value > 80 ? "bg-red-500" : value > 60 ? "bg-yellow-500" : "bg-green-500"
                            }`}
                            style={{ width: `${value}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Performance History */}
                <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">Performance History</h3>
                  <div className="space-y-4">
                    <div className="text-center py-8">
                      <div className="text-4xl text-gray-400 mb-2">📈</div>
                      <p className="text-gray-600">Performance charts and historical data will be displayed here</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Business Tab */}
          {activeTab === "business" && (
            <div className="space-y-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Business Metrics</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {Object.entries(dashboardData.businessMetrics).map(([metric, value]) => (
                  <div key={metric} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                    <div className="text-center">
                      <div className="text-3xl mb-4">
                        {metric === "activeUsers" ? "👥" : 
                         metric === "transactions" ? "💳" : 
                         metric === "revenue" ? "💰" : "📈"}
                      </div>
                      <h3 className="text-lg font-semibold text-gray-900 mb-2 capitalize">
                        {metric.replace(/([A-Z])/g, ' $1').trim()}
                      </h3>
                      <div className="text-3xl font-bold text-sigma-600 mb-2">{value}</div>
                      {metric === "growth" && (
                        <span className="text-sm text-green-600 bg-green-100 px-2 py-1 rounded-full">
                          {value}
                        </span>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              {/* Business Insights */}
              <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Business Insights</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center p-4 bg-blue-50 rounded-lg">
                    <div className="text-2xl mb-2">🎯</div>
                    <h4 className="font-medium text-gray-900 mb-1">Target Achievement</h4>
                    <p className="text-2xl font-bold text-blue-600">87%</p>
                  </div>
                  <div className="text-center p-4 bg-green-50 rounded-lg">
                    <div className="text-2xl mb-2">🚀</div>
                    <h4 className="font-medium text-gray-900 mb-1">Growth Rate</h4>
                    <p className="text-2xl font-bold text-green-600">+12.5%</p>
                  </div>
                  <div className="text-center p-4 bg-purple-50 rounded-lg">
                    <div className="text-2xl mb-2">⭐</div>
                    <h4 className="font-medium text-gray-900 mb-1">Customer Satisfaction</h4>
                    <p className="text-2xl font-bold text-purple-600">94%</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>

      <Footer />
    </>
  );
}
