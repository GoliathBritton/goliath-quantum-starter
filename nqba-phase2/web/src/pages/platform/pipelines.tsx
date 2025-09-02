import Link from "next/link";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

export default function PlatformPipelines() {
  const pipelines = [
    {
      id: "PIPELINE_001",
      name: "Customer Onboarding",
      type: "Business Process",
      status: "running",
      steps: 8,
      currentStep: 5,
      efficiency: "67%",
      lastExecuted: "2 minutes ago",
      nextRun: "5 minutes",
      agents: ["Customer Service Agent", "Finance Agent", "Compliance Agent"]
    },
    {
      id: "PIPELINE_002",
      name: "Financial Risk Assessment",
      type: "Risk Management",
      status: "completed",
      steps: 12,
      currentStep: 12,
      efficiency: "89%",
      lastExecuted: "1 hour ago",
      nextRun: "24 hours",
      agents: ["Risk Analysis Agent", "Market Data Agent", "Regulatory Agent"]
    },
    {
      id: "PIPELINE_003",
      name: "Quality Control Process",
      type: "Manufacturing",
      status: "scheduled",
      steps: 6,
      currentStep: 0,
      efficiency: "92%",
      lastExecuted: "6 hours ago",
      nextRun: "2 hours",
      agents: ["QA Agent", "Production Agent", "Logistics Agent"]
    },
    {
      id: "PIPELINE_004",
      name: "Data Processing Workflow",
      type: "Data Analytics",
      status: "error",
      steps: 10,
      currentStep: 7,
      efficiency: "78%",
      lastExecuted: "30 minutes ago",
      nextRun: "Retry in 15 min",
      agents: ["Data Processing Agent", "Analytics Agent", "Storage Agent"]
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "running": return "bg-blue-100 text-blue-800";
      case "completed": return "bg-green-100 text-green-800";
      case "scheduled": return "bg-yellow-100 text-yellow-800";
      case "error": return "bg-red-100 text-red-800";
      case "paused": return "bg-gray-100 text-gray-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "running": return "🔄";
      case "completed": return "✅";
      case "scheduled": return "⏰";
      case "error": return "❌";
      case "paused": return "⏸️";
      default: return "❓";
    }
  };

  const getProgressColor = (efficiency: string) => {
    const num = parseInt(efficiency);
    if (num >= 90) return "bg-green-500";
    if (num >= 70) return "bg-blue-500";
    if (num >= 50) return "bg-yellow-500";
    return "bg-red-500";
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
            Business Process Automation
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl leading-relaxed">
            Design, deploy, and monitor intelligent business pipelines that orchestrate AI agents 
            to automate complex workflows with unprecedented efficiency.
          </p>
        </div>
      </section>

      {/* Pipeline Creation */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 border border-purple-200">
            <h2 className="text-3xl font-bold text-gray-900 mb-6">Create New Pipeline</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pipeline Name
                </label>
                <input
                  type="text"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                  placeholder="e.g., Customer Support Workflow"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Pipeline Type
                </label>
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                  <option>Business Process</option>
                  <option>Data Processing</option>
                  <option>Risk Management</option>
                  <option>Customer Service</option>
                  <option>Financial Operations</option>
                  <option>Custom Workflow</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Execution Frequency
                </label>
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent">
                  <option>On Demand</option>
                  <option>Every Hour</option>
                  <option>Daily</option>
                  <option>Weekly</option>
                  <option>Monthly</option>
                  <option>Custom Schedule</option>
                </select>
              </div>
            </div>
            
            <div className="mt-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Describe the pipeline purpose and expected outcomes..."
              ></textarea>
            </div>
            
            <div className="mt-6">
              <button className="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105">
                🔌 Create Pipeline
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Pipeline List */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900">Active Pipelines</h2>
            <div className="flex space-x-2">
              <button className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50">
                Refresh
              </button>
              <button className="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700">
                Deploy All
              </button>
            </div>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {pipelines.map((pipeline) => (
              <div key={pipeline.id} className="bg-white rounded-2xl shadow-xl p-6 border border-gray-200 hover:shadow-2xl transition-all">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{pipeline.name}</h3>
                    <p className="text-sm text-gray-500">{pipeline.type}</p>
                  </div>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(pipeline.status)}`}>
                    {getStatusIcon(pipeline.status)} {pipeline.status}
                  </span>
                </div>
                
                <div className="space-y-3 mb-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Progress</span>
                    <span className="text-sm font-semibold text-gray-900">
                      {pipeline.currentStep}/{pipeline.steps}
                    </span>
                  </div>
                  
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(pipeline.efficiency)}`}
                      style={{ width: `${(pipeline.currentStep / pipeline.steps) * 100}%` }}
                    ></div>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Efficiency</span>
                    <span className="text-sm font-semibold text-green-600">{pipeline.efficiency}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Last Executed</span>
                    <span className="text-sm text-gray-500">{pipeline.lastExecuted}</span>
                  </div>
                  
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Next Run</span>
                    <span className="text-sm text-gray-500">{pipeline.nextRun}</span>
                  </div>
                </div>
                
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Involved Agents</h4>
                  <div className="flex flex-wrap gap-2">
                    {pipeline.agents.map((agent, index) => (
                      <span key={index} className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-700">
                        {agent}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  <button className="flex-1 bg-gradient-to-r from-purple-500 to-pink-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:from-purple-600 hover:to-pink-700 transition-all">
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

      {/* Pipeline Performance Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Pipeline Performance Overview</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200 text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">4</div>
              <div className="text-sm text-gray-600">Active Pipelines</div>
            </div>
            
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200 text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">81.5%</div>
              <div className="text-sm text-gray-600">Average Efficiency</div>
            </div>
            
            <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl p-6 border border-green-200 text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">36</div>
              <div className="text-sm text-gray-600">Total Steps</div>
            </div>
            
            <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-6 border border-orange-200 text-center">
              <div className="text-3xl font-bold text-orange-600 mb-2">24/7</div>
              <div className="text-sm text-gray-600">Automation</div>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
