import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Monitoring() {
  const systemMetrics = [
    {
      name: "Quantum Backend",
      status: "healthy",
      uptime: "99.97%",
      performance: "410x",
      lastCheck: "2 seconds ago",
      responseTime: "45ms"
    },
    {
      name: "AI Agent Cluster",
      status: "healthy",
      uptime: "99.94%",
      performance: "24x",
      lastCheck: "5 seconds ago",
      responseTime: "120ms"
    },
    {
      name: "NQBA Core",
      status: "warning",
      uptime: "99.89%",
      performance: "18x",
      lastCheck: "1 minute ago",
      responseTime: "280ms"
    },
    {
      name: "MCP Integration",
      status: "healthy",
      uptime: "99.99%",
      performance: "12x",
      lastCheck: "10 seconds ago",
      responseTime: "85ms"
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "healthy": return "bg-green-100 text-green-800";
      case "warning": return "bg-yellow-100 text-yellow-800";
      case "critical": return "bg-red-100 text-red-800";
      case "offline": return "bg-gray-100 text-gray-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "healthy": return "🟢";
      case "warning": return "🟡";
      case "critical": return "🔴";
      case "offline": return "⚫";
      default: return "❓";
    }
  };

  const alerts = [
    {
      id: "ALT_001",
      severity: "warning",
      message: "NQBA Core response time increased by 15%",
      timestamp: "2 minutes ago",
      system: "NQBA Core"
    },
    {
      id: "ALT_002",
      severity: "info",
      message: "New quantum job submitted successfully",
      timestamp: "5 minutes ago",
      system: "Quantum Backend"
    },
    {
      id: "ALT_003",
      severity: "info",
      message: "AI Agent performance optimization completed",
      timestamp: "12 minutes ago",
      system: "AI Agent Cluster"
    }
  ];

  const getAlertColor = (severity: string) => {
    switch (severity) {
      case "critical": return "border-red-500 bg-red-50";
      case "warning": return "border-yellow-500 bg-yellow-50";
      case "info": return "border-blue-500 bg-blue-50";
      default: return "border-gray-500 bg-gray-50";
    }
  };

  const getAlertIcon = (severity: string) => {
    switch (severity) {
      case "critical": return "🔴";
      case "warning": return "🟡";
      case "info": return "🔵";
      default: return "⚪";
    }
  };

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-4 mb-6">
            <Link href="/platform-dashboard" className="text-flyfoxSilver-300 hover:text-white transition-colors">
              ← Back to Dashboard
            </Link>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            System Monitoring
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl leading-relaxed">
            Real-time monitoring of FLYFOX AI platform health, performance metrics, and system alerts. 
            Proactive monitoring ensures optimal operation and quantum advantage.
          </p>
        </div>
      </section>

      {/* System Health Overview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">System Health Overview</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {systemMetrics.map((metric, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 hover:shadow-2xl transition-all">
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-lg font-bold text-gray-900">{metric.name}</h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(metric.status)}`}>
                    {getStatusIcon(metric.status)} {metric.status}
                  </span>
                </div>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Uptime</span>
                    <span className="text-sm font-semibold text-green-600">{metric.uptime}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Performance</span>
                    <span className="text-sm font-semibold text-cyan-600">{metric.performance}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Response Time</span>
                    <span className="text-sm font-semibold text-gray-900">{metric.responseTime}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Last Check</span>
                    <span className="text-sm text-gray-500">{metric.lastCheck}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Real-time Metrics */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Real-time Performance Metrics</h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Quantum Performance */}
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Quantum Computing Performance</h3>
              
              <div className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Current Performance Multiplier</span>
                    <span className="text-2xl font-bold text-cyan-600">410x</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-gradient-to-r from-cyan-500 to-purple-600 h-3 rounded-full" style={{ width: '100%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Jobs in Queue</span>
                    <span className="text-lg font-semibold text-purple-600">12</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-purple-500 h-3 rounded-full" style={{ width: '60%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Average Job Time</span>
                    <span className="text-lg font-semibold text-green-600">2.3s</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-green-500 h-3 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>
              </div>
            </div>
            
            {/* AI Agent Performance */}
            <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">AI Agent Performance</h3>
              
              <div className="space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Active Agents</span>
                    <span className="text-2xl font-bold text-green-600">24</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-green-500 h-3 rounded-full" style={{ width: '80%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Average Efficiency</span>
                    <span className="text-lg font-semibold text-blue-600">43x</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-blue-500 h-3 rounded-full" style={{ width: '72%' }}></div>
                  </div>
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Learning Progress</span>
                    <span className="text-lg font-semibold text-orange-600">78%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <div className="bg-orange-500 h-3 rounded-full" style={{ width: '78%' }}></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* System Alerts */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">System Alerts</h2>
            <div className="flex space-x-2">
              <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                Clear All
              </button>
              <button className="px-4 py-2 text-sm font-medium text-white bg-cyan-600 rounded-lg hover:bg-cyan-700">
                View History
              </button>
            </div>
          </div>
          
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div key={alert.id} className={`border-l-4 p-4 rounded-lg ${getAlertColor(alert.severity)}`}>
                <div className="flex items-start space-x-3">
                  <span className="text-lg">{getAlertIcon(alert.severity)}</span>
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{alert.message}</p>
                    <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                      <span>{alert.timestamp}</span>
                      <span>•</span>
                      <span>{alert.system}</span>
                    </div>
                  </div>
                  <button className="text-gray-400 hover:text-gray-600">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* System Resources */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">System Resources</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">87%</div>
              <div className="text-sm text-gray-600">CPU Usage</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div className="bg-green-500 h-2 rounded-full" style={{ width: '87%' }}></div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">64%</div>
              <div className="text-sm text-gray-600">Memory Usage</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '64%' }}></div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">92%</div>
              <div className="text-sm text-gray-600">GPU Usage</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div className="bg-purple-500 h-2 rounded-full" style={{ width: '92%' }}></div>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 text-center">
              <div className="text-3xl font-bold text-orange-600 mb-2">78%</div>
              <div className="text-sm text-gray-600">Storage Usage</div>
              <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                <div className="bg-orange-500 h-2 rounded-full" style={{ width: '78%' }}></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
