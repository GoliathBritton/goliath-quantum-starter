import Link from "next/link";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

export default function PlatformAgents() {
  const agents = [
    {
      id: "AGENT_001",
      name: "Quantum Finance Agent",
      type: "Financial Analysis",
      status: "active",
      performance: "98.7%",
      tasks: ["Portfolio optimization", "Risk assessment", "Market analysis"],
      lastActive: "2 minutes ago",
      efficiency: "24x"
    },
    {
      id: "AGENT_002",
      name: "Manufacturing QA Agent",
      type: "Quality Control",
      status: "active",
      performance: "99.2%",
      tasks: ["Defect detection", "Process optimization", "Quality metrics"],
      lastActive: "5 minutes ago",
      efficiency: "34x"
    },
    {
      id: "AGENT_003",
      name: "Healthcare Diagnostics Agent",
      type: "Medical Analysis",
      status: "training",
      performance: "94.1%",
      tasks: ["Patient diagnosis", "Treatment recommendations", "Research analysis"],
      lastActive: "1 hour ago",
      efficiency: "96x"
    },
    {
      id: "AGENT_004",
      name: "Supply Chain Agent",
      type: "Logistics",
      status: "idle",
      performance: "97.8%",
      tasks: ["Route optimization", "Inventory management", "Demand forecasting"],
      lastActive: "3 hours ago",
      efficiency: "18x"
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "active": return "bg-green-100 text-green-800";
      case "training": return "bg-blue-100 text-blue-800";
      case "idle": return "bg-yellow-100 text-yellow-800";
      case "error": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active": return "🟢";
      case "training": return "🔄";
      case "idle": return "⏸️";
      case "error": return "❌";
      default: return "❓";
    }
  };

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center space-x-4 mb-6">
            <Link href="/platform" className="text-flyfoxSilver-300 hover:text-white transition-colors">
              ← Back to Platform
            </Link>
          </div>
          
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            AI Agent Workforce
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl leading-relaxed">
            Manage autonomous AI agents that continuously learn, optimize, and execute business processes 
            with unprecedented efficiency and accuracy.
          </p>
        </div>
      </section>

      {/* Agent Creation */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl p-8 border border-green-200">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Create New AI Agent</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Agent Name
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  placeholder="e.g., Customer Service Agent"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Agent Type
                </label>
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                  <option>Customer Service</option>
                  <option>Financial Analysis</option>
                  <option>Quality Control</option>
                  <option>Data Processing</option>
                  <option>Process Automation</option>
                  <option>Custom Agent</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Initial Knowledge Base
                </label>
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent">
                  <option>General Business</option>
                  <option>Financial Services</option>
                  <option>Manufacturing</option>
                  <option>Healthcare</option>
                  <option>Retail</option>
                  <option>Custom</option>
                </select>
              </div>
            </div>
            
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Specialization Areas
              </label>
              <textarea
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                placeholder="Enter specific areas of expertise, e.g., Risk management, Customer satisfaction, Process optimization"
              ></textarea>
            </div>
            
            <div className="mt-6">
              <button className="bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105">
                🤖 Create AI Agent
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Agent List */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Active Agents</h2>
            <div className="flex space-x-2">
              <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                Refresh
              </button>
              <button className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700">
                Deploy All
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {agents.map((agent) => (
              <div key={agent.id} className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 hover:shadow-2xl transition-all">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{agent.name}</h3>
                    <p className="text-sm text-gray-500">{agent.type}</p>
                  </div>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                    {getStatusIcon(agent.status)} {agent.status}
                  </span>
                </div>
                
                <div className="space-y-3 mb-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Performance</span>
                    <span className="text-sm font-semibold text-green-600">{agent.performance}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Efficiency</span>
                    <span className="text-sm font-semibold text-blue-600">{agent.efficiency}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Last Active</span>
                    <span className="text-sm text-gray-500">{agent.lastActive}</span>
                  </div>
                </div>
                
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Capabilities</h4>
                  <div className="flex flex-wrap gap-2">
                    {agent.tasks.map((task, index) => (
                      <span key={index} className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-700">
                        {task}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <button className="flex-1 bg-gradient-to-r from-green-500 to-blue-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-green-600 hover:to-blue-700 transition-all">
                    View Details
                  </button>
                  <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all">
                    ⚙️
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Agent Performance Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Agent Performance Overview</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl p-6 border border-green-200 text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">4</div>
              <div className="text-sm text-gray-600">Active Agents</div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200 text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">97.4%</div>
              <div className="text-sm text-gray-600">Average Performance</div>
            </div>
            
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200 text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">43x</div>
              <div className="text-sm text-gray-600">Average Efficiency</div>
            </div>
            
            <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-6 border border-orange-200 text-center">
              <div className="text-3xl font-bold text-orange-600 mb-2">24/7</div>
              <div className="text-sm text-gray-600">Availability</div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
