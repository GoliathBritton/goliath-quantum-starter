import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function FlyfoxAI() {
  const [activeClients, setActiveClients] = useState(47);
  const [platformRevenue, setPlatformRevenue] = useState(1200000);
  const [quantumJobs, setQuantumJobs] = useState(89);
  const [aiAgents, setAiAgents] = useState(247);

  useEffect(() => {
    // Simulate real-time platform updates
    const interval = setInterval(() => {
      setActiveClients(prev => prev + Math.floor(Math.random() * 2));
      setPlatformRevenue(prev => prev + Math.floor(Math.random() * 50000));
      setQuantumJobs(prev => prev + Math.floor(Math.random() * 3));
      setAiAgents(prev => prev + Math.floor(Math.random() * 2));
    }, 6000);

    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const platformModules = [
    { name: "Quantum Computing Hub", status: "Active", efficiency: "99.9%", color: "from-purple-500 to-pink-500", icon: "⚛️" },
    { name: "AI Agent Management", status: "Active", efficiency: "99.7%", color: "from-blue-500 to-cyan-500", icon: "🤖" },
    { name: "Business Automation", status: "Active", efficiency: "98.8%", color: "from-green-500 to-emerald-500", icon: "⚡" },
    { name: "Advanced Analytics", status: "Active", efficiency: "99.2%", color: "from-orange-500 to-red-500", icon: "📊" }
  ];

  const clientIndustries = [
    { name: "Financial Services", clients: 18, revenue: "$450K", color: "from-green-500 to-emerald-500", icon: "💳" },
    { name: "Technology", clients: 15, revenue: "$380K", color: "from-blue-500 to-cyan-500", icon: "💻" },
    { name: "Healthcare", clients: 8, revenue: "$220K", color: "from-purple-500 to-pink-500", icon: "🏥" },
    { name: "Energy", clients: 6, revenue: "$150K", color: "from-orange-500 to-red-500", icon: "⚡" }
  ];

  const aiCapabilities = [
    { name: "Natural Language Processing", accuracy: "99.3%", icon: "💬", description: "Advanced language understanding and generation" },
    { name: "Computer Vision", accuracy: "98.7%", icon: "👁️", description: "Image and video analysis capabilities" },
    { name: "Predictive Modeling", accuracy: "99.1%", icon: "🔮", description: "Forecast future trends and outcomes" },
    { name: "Autonomous Decision Making", accuracy: "97.9%", icon: "🧠", description: "Self-learning decision systems" }
  ];

  return (
    <>
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-orange-900 via-red-800 to-pink-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="text-6xl md:text-7xl mb-6">🦊</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              FLYFOX AI
            </h1>
            <p className="text-xl md:text-2xl text-orange-200 max-w-4xl mx-auto leading-relaxed">
              Quantum-powered AI platform and business automation.
              The world's first intelligence economy platform with 410x performance boost.
            </p>
            
            {/* Status Badges */}
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <div className="flex items-center space-x-2 bg-orange-500/20 backdrop-blur-sm border border-orange-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-orange-400 rounded-full animate-pulse"></div>
                <span>Active Clients: {activeClients}</span>
              </div>
              <div className="flex items-center space-x-2 bg-red-500/20 backdrop-blur-sm border border-red-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-red-400 rounded-full animate-pulse"></div>
                <span>Revenue: {formatCurrency(platformRevenue)}</span>
              </div>
              <div className="flex items-center space-x-2 bg-pink-500/20 backdrop-blur-sm border border-pink-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-pink-400 rounded-full animate-pulse"></div>
                <span>AI Agents: {aiAgents}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-orange-600 mb-2">{activeClients}</div>
              <p className="text-gray-600">Active Clients</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-red-600 mb-2">{formatCurrency(platformRevenue)}</div>
              <p className="text-gray-600">Platform Revenue</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-pink-600 mb-2">{quantumJobs}</div>
              <p className="text-gray-600">Quantum Jobs</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">{aiAgents}</div>
              <p className="text-gray-600">AI Agents</p>
            </div>
          </div>
        </div>
      </section>

      {/* Platform Overview */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Platform Overview</h2>
            <p className="text-xl text-gray-600">Comprehensive AI platform with quantum computing integration</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Platform Modules */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Platform Modules</h3>
              <div className="space-y-6">
                {platformModules.map((module, index) => (
                  <div key={index} className="flex items-center space-x-4">
                    <div className={`w-16 h-16 bg-gradient-to-br ${module.color} rounded-xl flex items-center justify-center text-white text-2xl`}>
                      {module.icon}
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-semibold text-gray-900">{module.name}</span>
                        <span className="text-lg font-bold text-gray-700">{module.efficiency}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Status</span>
                        <span className="text-sm font-semibold text-green-600">{module.status}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Client Industries */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Client Industries</h3>
              <div className="space-y-4">
                {clientIndustries.map((industry, index) => (
                  <div key={index} className="p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3 mb-2">
                      <div className={`w-12 h-12 bg-gradient-to-br ${industry.color} rounded-lg flex items-center justify-center text-white text-xl`}>
                        {industry.icon}
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">{industry.name}</p>
                        <p className="text-sm text-gray-600">{industry.clients} clients</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">{industry.revenue}</p>
                      <p className="text-xs text-gray-600">Revenue</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* AI Capabilities */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">AI Capabilities</h2>
            <p className="text-xl text-gray-600">State-of-the-art artificial intelligence powered by quantum computing</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {aiCapabilities.map((capability, index) => (
              <div key={index} className="bg-gradient-to-br from-orange-500 to-red-500 text-white p-6 rounded-xl text-center">
                <div className="text-4xl mb-4">{capability.icon}</div>
                <h3 className="text-xl font-bold mb-2">{capability.name}</h3>
                <p className="text-orange-100 mb-3 text-sm">{capability.description}</p>
                <div className="text-2xl font-bold">{capability.accuracy}</div>
              </div>
            ))}
          </div>

          {/* AI Performance Metrics */}
          <div className="bg-gradient-to-r from-gray-900 to-gray-800 text-white rounded-2xl p-8">
            <h3 className="text-2xl font-bold mb-6 text-center">AI Performance Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-orange-400 mb-2">410x</div>
                <p className="text-gray-300">Performance Boost</p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-red-400 mb-2">99.9%</div>
                <p className="text-gray-300">Uptime</p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-pink-400 mb-2">24/7</div>
                <p className="text-gray-300">Continuous Learning</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FLYFOX AI Pillars */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">FLYFOX AI Pillars</h2>
            <p className="text-xl text-gray-600">The foundation of our revolutionary platform</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🧠</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Metis AI</h3>
              <p className="text-gray-600 mb-6">
                Autonomous intelligence systems that learn and adapt without human intervention
              </p>
              <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🚀</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Hyperion Scaling</h3>
              <p className="text-gray-600 mb-6">
                Instant deployment and scaling capabilities for any business need
              </p>
              <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">⚛️</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Dynex Quantum</h3>
              <p className="text-gray-600 mb-6">
                410x performance boost through quantum computing integration
              </p>
              <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🏗️</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">NQBA Core</h3>
              <p className="text-gray-600 mb-6">
                Neuromorphic quantum business architecture for enterprise solutions
              </p>
              <div className="bg-orange-100 text-orange-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🎯</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Q-Cortex</h3>
              <p className="text-gray-600 mb-6">
                Policy-driven decision making with quantum-enhanced governance
              </p>
              <div className="bg-indigo-100 text-indigo-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🔄</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Self-Learning</h3>
              <p className="text-gray-600 mb-6">
                Continuous improvement and optimization through machine learning
              </p>
              <div className="bg-teal-100 text-teal-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Business Automation */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Business Automation</h2>
            <p className="text-xl text-gray-600">Transform your business with AI-powered automation</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white p-8 rounded-2xl">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-2xl font-bold mb-4">Sales Automation</h3>
              <p className="mb-6 text-blue-100">
                AI-powered lead generation, qualification, and follow-up systems
              </p>
              <div className="text-3xl font-bold">+247%</div>
              <p className="text-blue-200">Sales Increase</p>
            </div>

            <div className="bg-gradient-to-br from-green-500 to-emerald-500 text-white p-8 rounded-2xl">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-2xl font-bold mb-4">Analytics & Insights</h3>
              <p className="mb-6 text-green-100">
                Real-time business intelligence and predictive analytics
              </p>
              <div className="text-3xl font-bold">-68%</div>
              <p className="text-green-200">Time to Insight</p>
            </div>

            <div className="bg-gradient-to-br from-purple-500 to-pink-500 text-white p-8 rounded-2xl">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-2xl font-bold mb-4">Process Optimization</h3>
              <p className="mb-6 text-purple-100">
                Streamline operations with intelligent workflow automation
              </p>
              <div className="text-3xl font-bold">73%</div>
              <p className="text-purple-200">Efficiency Gain</p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-orange-600 to-red-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Experience the Future of AI?</h2>
          <p className="text-xl text-orange-100 mb-8 max-w-3xl mx-auto">
            Join the intelligence economy with FLYFOX AI's quantum-powered platform
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform-dashboard" className="bg-white text-orange-600 px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
              Access Platform Dashboard
            </Link>
            <Link href="/contact" className="bg-orange-700 text-white px-8 py-4 rounded-xl font-semibold hover:bg-orange-800 transition-colors">
              Schedule Platform Demo
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
