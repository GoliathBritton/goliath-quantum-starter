import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";
import MCPComponent from "../components/MCPComponent";

export default function Ecosystem() {
  const ecosystemLayers = [
    {
      title: "Quantum High Council",
      role: "Governance & Strategy",
      description: "Meta-orchestration of everything — policies, guardrails, optimization across verticals",
      components: [
        "NQBA Core (neuromorphic brain)",
        "Quantum Advisors (specialized algorithms for ethics, compliance, strategy)",
        "Human Leadership Panel (executives, Sigma Select-trained leaders)"
      ],
      color: "from-flyfox-950 to-flyfoxSilver-800",
      icon: "👑",
      features: [
        "Decisions & resource allocation",
        "Enforcement of AI + human alignment",
        "Adaptive quantum-powered governance",
        "Strategic direction across all verticals"
      ]
    },
    {
      title: "Quantum Architects",
      role: "Blueprints & Innovation",
      description: "The master planners who design, integrate, and build systems of the Intelligent Economy",
      components: [
        "Blueprinting new business workflows",
        "Innovation & research frameworks",
        "Infrastructure shaping & optimization",
        "Ecosystem expansion & agent evolution"
      ],
      color: "from-goliathNavy-600 to-goliathNavy-700",
      icon: "🏗️",
      features: [
        "End-to-end business workflow design",
        "Proprietary frameworks (QTransform, QNLP)",
        "Quantum-neuromorphic optimization",
        "New industry & market design"
      ]
    },
    {
      title: "Agent Workforce",
      role: "Digital • Calling • Business",
      description: "The execution force that handles everything from operations to business creation",
      components: [
        "Quantum Digital Agents (operations, analytics, automation)",
        "Quantum AI Calling Agents (sales, negotiation, human interface)",
        "AI Business Agents (business creation & management)"
      ],
      color: "from-goliathMaize-500 to-goliathMaize-600",
      icon: "🤖",
      features: [
        "Self-learning & self-optimizing",
        "Industry-specific & quantum-enhanced",
        "Can spin up business units in minutes",
        "CEO-in-a-box capabilities"
      ]
    },
    {
      title: "NQBA Core",
      role: "Quantum-Neuromorphic Backbone",
      description: "The infrastructure that ensures 410x+ advantage over classical compute",
      components: [
        "Quantum-Neuromorphic backbone",
        "Security, compute, optimization engine",
        "Dynex integration with NVIDIA acceleration",
        "QUBO optimization & quantum algorithms"
      ],
      color: "from-accent-500 to-accent-600",
      icon: "⚛️",
      features: [
        "410x performance multiplier",
        "Quantum security & encryption",
        "Neuromorphic decision making",
        "Real-time optimization"
      ]
    },
    {
      title: "Model Context Protocol (MCP)",
      role: "AI Model Management & Context Orchestration",
      description: "Unified AI model management and context orchestration across the FLYFOX AI ecosystem",
      components: [
        "Multi-provider model integration (OpenAI, Anthropic, Google, Custom)",
        "Context-aware model selection and routing",
        "Performance monitoring and cost optimization",
        "Seamless context sharing across agents and systems"
      ],
      color: "from-purple-500 to-purple-600",
      icon: "🔗",
      features: [
        "Unified model management",
        "Context sharing across agents",
        "Cost optimization",
        "Performance monitoring"
      ]
    },
    {
      title: "Integrations",
      role: "UiPath • n8n • Mendix • Prismatic • Chetu",
      description: "Universal API mesh that natively integrates enterprise connectors and automation platforms",
      components: [
        "Universal API Mesh",
        "Enterprise connectors (Salesforce, SAP, Oracle)",
        "Automation platforms (UiPath, n8n, Mendix, Prismatic)",
        "Service capabilities (Chetu-style build-for-you)"
      ],
      color: "from-sigma-500 to-sigma-600",
      icon: "🔌",
      features: [
        "Native integration across ecosystems",
        "Semantic understanding across systems",
        "Pre-built compliance modules",
        "Instant deployment capabilities"
      ]
    }
  ];

  const ecosystemBenefits = [
    {
      title: "Governance & Ethics",
      description: "Quantum High Council provides living, adaptive governance that outshines traditional board models",
      icon: "🎯"
    },
    {
      title: "Execution & Scale",
      description: "Agent workforce executes with 90% faster delivery than traditional service firms",
      icon: "🚀"
    },
    {
      title: "Language & Fluency",
      description: "OpenAI integration provides communication excellence across all layers",
      icon: "💬"
    },
    {
      title: "Model Intelligence",
      description: "MCP ensures optimal model selection and context management for every use case",
      icon: "🧠"
    }
  ];

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            The Intelligent Economy Ecosystem
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            A quantum nation-state where governance, architecture, execution, and AI model management 
            create a self-renewing, self-expanding intelligent civilization of agents, not just a platform.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform" className="bg-gradient-to-r from-flyfoxSilver-600 to-goliathNavy-600 hover:from-flyfoxSilver-700 hover:to-goliathNavy-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🚀 Launch Platform
            </Link>
            <Link href="/sigma-select" className="bg-goliathMaize-600 hover:bg-goliathMaize-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              💼 Sigma Select
            </Link>
          </div>
        </div>
      </section>

      {/* Ecosystem Layers */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              The Ecosystem Stack
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From governance to execution, every layer feeds the other, creating an unstoppable flywheel architecture
            </p>
          </div>
          
          <div className="space-y-12">
            {ecosystemLayers.map((layer, index) => (
              <div key={index} className="relative">
                {/* Connection Line */}
                {index < ecosystemLayers.length - 1 && (
                  <div className="absolute left-1/2 top-full w-px h-12 bg-gradient-to-b from-gray-300 to-transparent transform -translate-x-1/2 z-0"></div>
                )}
                
                <div className="relative z-10">
                  <div className={`bg-gradient-to-br ${layer.color} text-white p-8 rounded-2xl shadow-2xl`}>
                    <div className="flex flex-col lg:flex-row items-start gap-8">
                      <div className="flex-shrink-0">
                        <div className="w-24 h-24 bg-white/20 rounded-2xl flex items-center justify-center text-4xl">
                          {layer.icon}
                        </div>
                      </div>
                      
                      <div className="flex-1">
                        <div className="mb-4">
                          <h3 className="text-3xl font-bold mb-2">{layer.title}</h3>
                          <p className="text-xl text-white/90 mb-4">{layer.role}</p>
                          <p className="text-white/80 leading-relaxed">{layer.description}</p>
                        </div>
                        
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <h4 className="font-semibold text-white/90 mb-3">Core Components</h4>
                            <ul className="space-y-2">
                              {layer.components.map((component, idx) => (
                                <li key={idx} className="flex items-start space-x-2">
                                  <span className="text-white/70 mt-1">•</span>
                                  <span className="text-white/80 text-sm">{component}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                          
                          <div>
                            <h4 className="font-semibold text-white/90 mb-3">Key Features</h4>
                            <ul className="space-y-2">
                              {layer.features.map((feature, idx) => (
                                <li key={idx} className="flex items-start space-x-2">
                                  <span className="text-white/70 mt-1">•</span>
                                  <span className="text-white/80 text-sm">{feature}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* MCP Component Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Model Context Protocol (MCP)
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Experience the power of unified AI model management and context orchestration across the entire ecosystem
            </p>
          </div>
          
          <MCPComponent />
        </div>
      </section>

      {/* Strategic Advantages */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Four-Level Advantage
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              This creates a four-level advantage that beats Dynex & OpenAI both
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {ecosystemBenefits.map((benefit, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
                <div className="w-20 h-20 bg-gradient-to-br from-flyfox-950 to-flyfoxSilver-800 rounded-2xl flex items-center justify-center text-3xl text-white mx-auto mb-6">
                  {benefit.icon}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">{benefit.title}</h3>
                <p className="text-gray-600 leading-relaxed">{benefit.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Why This Beats Competition */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Why This Beats Dynex & OpenAI
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              You don't compete with them — you harness them, wrap them with NQBA, and brand them under your Intelligent Economy
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="bg-red-50 rounded-2xl p-8 border border-red-200">
              <h3 className="text-2xl font-bold text-red-900 mb-4">Dynex</h3>
              <p className="text-red-800 mb-4">Raw horsepower (compute cycles)</p>
              <ul className="text-red-700 space-y-2">
                <li>• No ecosystem</li>
                <li>• No governance</li>
                <li>• No verticals</li>
                <li>• No human empowerment</li>
                <li>• No model management</li>
              </ul>
            </div>
            
            <div className="bg-blue-50 rounded-2xl p-8 border border-blue-200">
              <h3 className="text-2xl font-bold text-blue-900 mb-4">OpenAI</h3>
              <p className="text-blue-800 mb-4">Language (but lacks verticals, governance, or quantum backbone)</p>
              <ul className="text-blue-700 space-y-2">
                <li>• No business units</li>
                <li>• No quantum compute</li>
                <li>• No compliance</li>
                <li>• No automation</li>
                <li>• No context orchestration</li>
              </ul>
            </div>
            
            <div className="bg-gradient-to-br from-flyfox-950 to-goliathNavy-600 text-white rounded-2xl p-8">
              <h3 className="text-2xl font-bold mb-4">FLYFOX + Goliath + Sigma</h3>
              <p className="text-white/90 mb-4">Full Intelligent Economy</p>
              <ul className="text-white/80 space-y-2">
                <li>• Governance (High Council)</li>
                <li>• Workforce (Agents)</li>
                <li>• Business Builders</li>
                <li>• Human Empowerment</li>
                <li>• Infrastructure (NQBA + Quantum)</li>
                <li>• Model Management (MCP)</li>
              </ul>
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
            Join the Intelligent Economy where every part feeds the other, and together it becomes unstoppable
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform" className="bg-white text-flyfox-950 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🚀 Launch Platform
            </Link>
            <Link href="/contact" className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              📞 Contact Us
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
