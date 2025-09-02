import { useState } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function NQBAArchitecture() {
  const [activeLayer, setActiveLayer] = useState(1);

  const layers = [
    {
      id: 1,
      name: "Quantum Digital Agent Layer",
      description: "AI agents with quantum-enhanced decision making",
      features: ["Self-learning capabilities", "Quantum optimization", "Real-time adaptation", "Industry specialization"],
      color: "from-blue-500 to-cyan-500"
    },
    {
      id: 2,
      name: "Business Logic Layer",
      description: "Core business processes and automation",
      features: ["Workflow orchestration", "Process automation", "Business rules engine", "Integration hub"],
      color: "from-green-500 to-emerald-500"
    },
    {
      id: 3,
      name: "Data Management Layer",
      description: "Quantum-enhanced data processing and storage",
      features: ["Quantum databases", "Real-time analytics", "Data encryption", "IPFS integration"],
      color: "from-purple-500 to-pink-500"
    },
    {
      id: 4,
      name: "Security & Compliance Layer",
      description: "Quantum-anchored security and governance",
      features: ["Quantum encryption", "Compliance automation", "Audit logging", "Risk management"],
      color: "from-red-500 to-orange-500"
    },
    {
      id: 5,
      name: "Infrastructure Layer",
      description: "Scalable cloud and quantum infrastructure",
      features: ["Auto-scaling", "Edge computing", "Quantum computing", "Global distribution"],
      color: "from-indigo-500 to-purple-500"
    }
  ];

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            NQBA Architecture
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            Neuromorphic Quantum Business Architecture - The foundation of the next generation 
            of AI-powered business automation with quantum computing capabilities.
          </p>
        </div>
      </section>

      {/* Architecture Overview */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              The NQBA Stack
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              A 5-layer architecture that combines neuromorphic computing, quantum optimization, 
              and business automation for unprecedented performance and scalability.
            </p>
          </div>

          {/* Layer Navigation */}
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            {layers.map((layer) => (
              <button
                key={layer.id}
                onClick={() => setActiveLayer(layer.id)}
                className={`px-6 py-3 rounded-lg font-medium transition-all duration-200 ${
                  activeLayer === layer.id
                    ? `bg-gradient-to-r ${layer.color} text-white shadow-lg`
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Layer {layer.id}
              </button>
            ))}
          </div>

          {/* Active Layer Display */}
          <div className="bg-gray-50 rounded-2xl p-8">
            {layers.map((layer) => (
              <div key={layer.id} className={activeLayer === layer.id ? 'block' : 'hidden'}>
                <div className="text-center mb-8">
                  <h3 className="text-3xl font-bold text-gray-900 mb-4">{layer.name}</h3>
                  <p className="text-xl text-gray-600 max-w-2xl mx-auto">{layer.description}</p>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {layer.features.map((feature, index) => (
                    <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                      <div className="w-12 h-12 bg-gradient-to-r from-primary-500 to-flyfox-500 rounded-lg flex items-center justify-center mb-4 mx-auto">
                        <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <p className="text-gray-700 text-center font-medium">{feature}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Core Components */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-6">
              Core NQBA Components
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              The building blocks that power the entire FLYFOX AI ecosystem
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">qdLLM</h3>
              <p className="text-gray-600 mb-6">
                Quantum-enhanced Large Language Model with 410x performance boost through Dynex integration
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Quantum optimization</li>
                <li>• Real-time learning</li>
                <li>• Industry specialization</li>
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Quantum Digital Agent</h3>
              <p className="text-gray-600 mb-6">
                Autonomous AI agents with quantum-enhanced decision making and self-learning capabilities
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Autonomous operation</li>
                <li>• Quantum decision making</li>
                <li>• Continuous learning</li>
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Security Manager</h3>
              <p className="text-gray-600 mb-6">
                Quantum-anchored security with compliance automation and risk management
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Quantum encryption</li>
                <li>• Compliance automation</li>
                <li>• Risk assessment</li>
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Observability</h3>
              <p className="text-gray-600 mb-6">
                Comprehensive monitoring and analytics for system performance and business insights
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Real-time monitoring</li>
                <li>• Performance analytics</li>
                <li>• Business intelligence</li>
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-500 to-blue-500 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Business Units</h3>
              <p className="text-gray-600 mb-6">
                Modular business units that integrate seamlessly with the NQBA architecture
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Goliath Capital</li>
                <li>• Sigma Select</li>
                <li>• FLYFOX AI</li>
              </ul>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center mb-6">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Hyperion Scaling</h3>
              <p className="text-gray-600 mb-6">
                Instant deployment and performance optimization with real-time scaling
              </p>
              <ul className="text-sm text-gray-600 space-y-2">
                <li>• Auto-scaling</li>
                <li>• Global distribution</li>
                <li>• Performance optimization</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary-900 to-flyfox-900 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl font-bold mb-6">
            Ready to Experience NQBA?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            See the future of business automation with our quantum-enhanced architecture
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dashboard" className="bg-white text-primary-900 font-semibold py-4 px-8 rounded-lg text-lg hover:bg-gray-100 transition-colors duration-200">
              🚀 Launch Platform
            </Link>
            <Link href="/login" className="bg-primary-600 hover:bg-primary-700 text-white font-semibold py-4 px-8 rounded-lg text-lg transition-colors duration-200">
              🔐 Login
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
