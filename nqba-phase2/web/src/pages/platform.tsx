import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";
import MCPComponent from "../components/MCPComponent";
import FLYFOXProcessIntelligence from "../components/FLYFOXProcessIntelligence";

export default function Platform() {
  const platformFeatures = [
    {
      title: "Compute Jobs",
      description: "Quantum-neuromorphic compute via NQBA (Dynex-preferred)",
      icon: "⚛️",
      color: "from-accent-500 to-accent-600",
      features: [
        "410x performance multiplier",
        "QUBO optimization",
        "NVIDIA acceleration",
        "Real-time job monitoring",
        "Cost optimization"
      ],
      link: "/platform/jobs",
      cta: "Run Quantum Job"
    },
    {
      title: "Agent Pods",
      description: "Metis pods with Hyperion scaling for autonomous intelligence",
      icon: "🤖",
      color: "from-goliathMaize-500 to-goliathMaize-600",
      features: [
        "Self-learning agents",
        "Instant deployment",
        "Auto-scaling infrastructure",
        "Performance monitoring",
        "Agent evolution"
      ],
      link: "/platform/agents",
      cta: "Deploy Agents"
    },
    {
      title: "Pipelines",
      description: "UiPath, n8n, Mendix, Prismatic integration and automation",
      icon: "🔌",
      color: "from-sigma-500 to-sigma-600",
      features: [
        "Universal API mesh",
        "Enterprise connectors",
        "Drag-and-drop recipes",
        "1-click deployment",
        "Real-time monitoring"
      ],
      link: "/platform/pipelines",
      cta: "Build Pipeline"
    },
    {
      title: "Model Context Protocol",
      description: "Unified AI model management and context orchestration",
      icon: "🔗",
      color: "from-purple-500 to-purple-600",
      features: [
        "Multi-provider integration",
        "Context-aware routing",
        "Performance optimization",
        "Cost management",
        "Seamless context sharing"
      ],
      link: "#mcp",
      cta: "Explore MCP"
    },
    {
      title: "Process Mining",
              description: "FLYFOX-powered process intelligence and automation discovery",
      icon: "🔍",
      color: "from-indigo-500 to-indigo-600",
      features: [
        "Process discovery & mapping",
        "Automation opportunity identification",
        "Performance optimization",
        "Compliance assurance",
        "Cost reduction analytics"
      ],
              link: "#process-intelligence",
      cta: "Explore Processes"
    }
  ];

  const integrationStatus = [
    { name: "UiPath", status: "connected", icon: "🤖", description: "RPA & Process Automation" },
    { name: "n8n", status: "connected", icon: "⚡", description: "Workflow Automation" },
    { name: "Mendix", status: "connected", icon: "🏗️", description: "Low-Code Development" },
    { name: "Prismatic", status: "connected", icon: "🔌", description: "Integration Platform" },
    { name: "Chetu", status: "available", icon: "🛠️", description: "Custom Development Services" },
         { name: "FLYFOX Process Intelligence", status: "connected", icon: "🔍", description: "Process Mining & Intelligence" }
  ];

  const platformMetrics = [
    { label: "Active Jobs", value: "247", change: "+12%", color: "text-blue-600" },
    { label: "Running Agents", value: "89", change: "+8%", color: "text-green-600" },
    { label: "Pipeline Executions", value: "1,247", change: "+23%", color: "text-purple-600" },
    { label: "Performance Boost", value: "410x", change: "Quantum", color: "text-orange-600" }
  ];

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            FLYFOX AI Platform
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            Dynex-powered intelligent economy platform with OpenAI linguistic intelligence, 
                         NQBA backbone, MCP integration, FLYFOX process intelligence, and comprehensive business automation across all verticals.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform/jobs" className="bg-gradient-to-r from-flyfoxSilver-600 to-goliathNavy-600 hover:from-flyfoxSilver-700 hover:to-goliathNavy-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🚀 Launch Platform
            </Link>
            <Link href="/ecosystem" className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🔍 Explore Ecosystem
            </Link>
          </div>
          <div className="mt-6 text-sm text-gray-400">
                         Dynex-preferred backend • NVIDIA acceleration • OpenAI dialogue layer • MCP integration • FLYFOX process intelligence
          </div>
        </div>
      </section>

      {/* Platform Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {platformMetrics.map((metric, index) => (
              <div key={index} className="bg-gray-50 rounded-2xl p-6 text-center">
                <div className={`text-3xl font-bold mb-2 ${metric.color}`}>
                  {metric.value}
                </div>
                <div className="text-gray-600 mb-2">{metric.label}</div>
                <div className="text-sm text-green-600 font-medium">{metric.change}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Platform Features */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Platform Capabilities
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From quantum computing to autonomous agents, experience the future of business automation
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-5 gap-8">
            {platformFeatures.map((feature, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
                <div className={`w-20 h-20 bg-gradient-to-br ${feature.color} rounded-2xl flex items-center justify-center text-3xl text-white mx-auto mb-6`}>
                  {feature.icon}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">{feature.title}</h3>
                <p className="text-gray-600 mb-6 text-center leading-relaxed">{feature.description}</p>
                
                <ul className="space-y-3 mb-8">
                  {feature.features.map((feat, idx) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <span className="text-green-500 mt-1">•</span>
                      <span className="text-gray-700">{feat}</span>
                    </li>
                  ))}
                </ul>
                
                {feature.link.startsWith('#') ? (
                  <button 
                    onClick={() => document.getElementById(feature.link.substring(1))?.scrollIntoView({ behavior: 'smooth' })}
                    className={`block w-full py-4 px-6 rounded-xl font-semibold text-lg text-center transition-all bg-gradient-to-r ${feature.color} text-white hover:shadow-lg`}
                  >
                    {feature.cta}
                  </button>
                ) : (
                  <Link 
                    href={feature.link}
                    className={`block w-full py-4 px-6 rounded-xl font-semibold text-lg text-center transition-all bg-gradient-to-r ${feature.color} text-white hover:shadow-lg`}
                  >
                    {feature.cta}
                  </Link>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* MCP Component Section */}
      <section id="mcp" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Model Context Protocol (MCP)
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience unified AI model management and context orchestration across the entire platform
            </p>
          </div>
          
          <MCPComponent />
        </div>
      </section>

             {/* FLYFOX Process Intelligence Section */}
       <section id="process-intelligence" className="py-20 bg-gray-50">
         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
           <div className="text-center mb-16">
             <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
               Process Mining & Intelligence
             </h2>
             <p className="text-xl text-gray-600 max-w-3xl mx-auto">
               FLYFOX-powered process discovery, automation opportunities, and performance optimization across all business units
             </p>
           </div>
           
           <FLYFOXProcessIntelligence />
         </div>
       </section>

      {/* Integration Status */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Integration Ecosystem
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Universal API mesh that natively integrates enterprise connectors and automation platforms
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {integrationStatus.map((integration, index) => (
              <div key={index} className="bg-gray-50 rounded-2xl p-6 border border-gray-200">
                <div className="flex items-center space-x-4 mb-4">
                  <div className="text-3xl">{integration.icon}</div>
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{integration.name}</h3>
                    <p className="text-gray-600 text-sm">{integration.description}</p>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                    integration.status === 'connected' 
                      ? 'bg-green-100 text-green-800' 
                      : 'bg-blue-100 text-blue-800'
                  }`}>
                    {integration.status === 'connected' ? '🟢 Connected' : '🔵 Available'}
                  </span>
                  
                  <button className="text-sigma-600 hover:text-sigma-700 font-medium text-sm">
                    {integration.status === 'connected' ? 'Manage' : 'Learn More'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Actions */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Quick Actions
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Get started immediately with our most popular platform features
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-8">
            <Link href="/platform/jobs" className="bg-gradient-to-r from-flyfox-950 to-flyfoxSilver-800 text-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all group">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">⚛️</div>
              <h3 className="text-2xl font-bold mb-4">Submit Quantum Job</h3>
              <p className="text-flyfoxSilver-100 mb-6">
                Run QUBO optimization, portfolio analysis, or custom quantum algorithms on Dynex
              </p>
              <div className="flex items-center text-flyfoxSilver-200 group-hover:text-white transition-colors">
                <span>Launch Job Console</span>
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </Link>
            
            <Link href="/platform/agents" className="bg-gradient-to-r from-goliathMaize-500 to-goliathMaize-600 text-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all group">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🤖</div>
              <h3 className="text-2xl font-bold mb-4">Deploy AI Agents</h3>
              <p className="text-goliathMaize-100 mb-6">
                Spin up Quantum Digital, Calling, or Business Agents with Metis AI templates
              </p>
              <div className="flex items-center text-goliathMaize-200 group-hover:text-white transition-colors">
                <span>Agent Management</span>
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </Link>
            
            <Link href="/platform/pipelines" className="bg-gradient-to-r from-goliathNavy-600 to-goliathNavy-700 text-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all group">
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🔌</div>
              <h3 className="text-2xl font-bold mb-4">Build Automation</h3>
              <p className="text-goliathNavy-100 mb-6">
                Create workflows with UiPath, n8n, Mendix, or Prismatic integration recipes
              </p>
              <div className="flex items-center text-goliathNavy-200 group-hover:text-white transition-colors">
                <span>Pipeline Builder</span>
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </Link>

            <button 
              onClick={() => document.getElementById('mcp')?.scrollIntoView({ behavior: 'smooth' })}
              className="bg-gradient-to-r from-purple-500 to-purple-600 text-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all group"
            >
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🔗</div>
              <h3 className="text-2xl font-bold mb-4">Manage Models</h3>
              <p className="text-purple-100 mb-6">
                Orchestrate AI models, manage contexts, and optimize performance across the ecosystem
              </p>
              <div className="flex items-center text-purple-200 group-hover:text-white transition-colors">
                <span>MCP Dashboard</span>
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </button>

            <button 
                             onClick={() => document.getElementById('process-intelligence')?.scrollIntoView({ behavior: 'smooth' })}
              className="bg-gradient-to-r from-indigo-500 to-indigo-600 text-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all group"
            >
              <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🔍</div>
              <h3 className="text-2xl font-bold mb-4">Process Mining</h3>
              <p className="text-indigo-100 mb-6">
                Discover automation opportunities and optimize business processes across all units
              </p>
              <div className="flex items-center text-indigo-200 group-hover:text-white transition-colors">
                <span>Process Intelligence</span>
                <svg className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            </button>
          </div>
        </div>
      </section>

      {/* Platform Benefits */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Why Choose FLYFOX AI Platform?
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the advantages that make us the leader in intelligent business automation
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-flyfox-950 to-flyfoxSilver-800 rounded-xl flex items-center justify-center text-white font-bold flex-shrink-0">
                  1
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Quantum Advantage</h3>
                  <p className="text-gray-600">
                    410x performance multiplier with Dynex quantum computing and NVIDIA acceleration, 
                    providing computational power that classical systems cannot match.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-goliathMaize-500 to-goliathMaize-600 rounded-xl flex items-center justify-center text-white font-bold flex-shrink-0">
                  2
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Self-Learning Intelligence</h3>
                  <p className="text-gray-600">
                    Metis AI agents continuously evolve and optimize, learning from every interaction 
                    to provide increasingly intelligent automation and decision-making.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-goliathNavy-600 to-goliathNavy-700 rounded-xl flex items-center justify-center text-white font-bold flex-shrink-0">
                  3
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Universal Integration</h3>
                  <p className="text-gray-600">
                    Native integration with leading automation platforms and enterprise systems, 
                    creating a seamless ecosystem that speaks every language.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold flex-shrink-0">
                  4
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Model Context Protocol</h3>
                  <p className="text-gray-600">
                    Unified AI model management with context orchestration, ensuring optimal model 
                    selection and seamless context sharing across all systems.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold flex-shrink-0">
                  5
                </div>
                <div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">Process Intelligence</h3>
                  <p className="text-gray-600">
                                         FLYFOX-powered process mining and automation discovery, providing enterprise-grade 
                     process intelligence across all business units.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Experience the Future?
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Join the intelligent economy where quantum computing meets autonomous intelligence 
            to create unprecedented business value and performance.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform/jobs" className="bg-white text-flyfox-950 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🚀 Start with Quantum Jobs
            </Link>
            <Link href="/contact" className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              📞 Contact Sales
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
