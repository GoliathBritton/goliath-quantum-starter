import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function PlatformSetup() {
  const [currentStep, setCurrentStep] = useState(1);
  const [setupProgress, setSetupProgress] = useState({
    nqba: 0,
    flyfox: 0,
    goliath: 0,
    sigma: 0,
    integration: 0
  });

  const [systemStatus, setSystemStatus] = useState({
    nqba: "Initializing",
    quantum: "Connecting",
    agents: "Loading",
    security: "Configuring"
  });

  useEffect(() => {
    // Simulate setup progress
    const interval = setInterval(() => {
      setSetupProgress(prev => ({
        nqba: Math.min(100, prev.nqba + Math.random() * 15),
        flyfox: Math.min(100, prev.flyfox + Math.random() * 12),
        goliath: Math.min(100, prev.goliath + Math.random() * 10),
        sigma: Math.min(100, prev.sigma + Math.random() * 8),
        integration: Math.min(100, prev.integration + Math.random() * 5)
      }));
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const setupSteps = [
    {
      id: 1,
      title: "NQBA Core Initialization",
      description: "Setting up the Neuromorphic Quantum Business Architecture foundation",
      icon: "🏗️",
      status: "active"
    },
    {
      id: 2,
      title: "FLYFOX AI Platform",
      description: "Configuring the quantum-powered AI platform and business automation",
      icon: "🦊",
      status: "pending"
    },
    {
      id: 3,
      title: "Goliath Capital Integration",
      description: "Setting up quantum-enhanced financial services and investment management",
      icon: "🏛️",
      status: "pending"
    },
    {
      id: 4,
      title: "Sigma Select Configuration",
      description: "Configuring AI-powered lead generation and sales optimization",
      icon: "Σ",
      status: "pending"
    },
    {
      id: 5,
      title: "Cross-Platform Integration",
      description: "Establishing seamless data flow and shared quantum resources",
      icon: "🔗",
      status: "pending"
    }
  ];

  const nqbaComponents = [
    { name: "Quantum Computing Hub", status: "Active", efficiency: "99.9%", icon: "⚛️" },
    { name: "AI Agent Management", status: "Active", efficiency: "99.7%", icon: "🤖" },
    { name: "Security & Compliance", status: "Active", efficiency: "99.8%", icon: "🔒" },
    { name: "Data Integration Layer", status: "Active", efficiency: "99.5%", icon: "📊" },
    { name: "Business Logic Engine", status: "Active", efficiency: "99.6%", icon: "⚡" },
    { name: "Observability & Monitoring", status: "Active", efficiency: "99.4%", icon: "📈" }
  ];

  return (
    <>
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-900 via-purple-900 to-indigo-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              NQBA Platform Setup
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
              Configure the complete Neuromorphic Quantum Business Architecture ecosystem.
              Powered by FLYFOX AI - The world's first intelligent economy platform.
            </p>
            
            {/* Setup Progress Overview */}
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <div className="flex items-center space-x-2 bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                <span>NQBA Core: {Math.round(setupProgress.nqba)}%</span>
              </div>
              <div className="flex items-center space-x-2 bg-orange-500/20 backdrop-blur-sm border border-orange-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-orange-400 rounded-full animate-pulse"></div>
                <span>FLYFOX AI: {Math.round(setupProgress.flyfox)}%</span>
              </div>
              <div className="flex items-center space-x-2 bg-green-500/20 backdrop-blur-sm border border-green-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>Integration: {Math.round(setupProgress.integration)}%</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Setup Steps */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Platform Setup Progress</h2>
            <p className="text-xl text-gray-600">Step-by-step configuration of the complete NQBA ecosystem</p>
          </div>

          <div className="space-y-6">
            {setupSteps.map((step, index) => (
              <div key={step.id} className="bg-gray-50 rounded-2xl p-6 border border-gray-200">
                <div className="flex items-center space-x-6">
                  <div className="flex-shrink-0">
                    <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-2xl ${
                      step.status === 'active' 
                        ? 'bg-gradient-to-br from-purple-500 to-indigo-500 text-white animate-pulse'
                        : step.status === 'completed'
                        ? 'bg-gradient-to-br from-green-500 to-emerald-500 text-white'
                        : 'bg-gray-300 text-gray-600'
                    }`}>
                      {step.icon}
                    </div>
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 mb-2">{step.title}</h3>
                    <p className="text-gray-600 mb-4">{step.description}</p>
                    
                    {/* Progress Bar */}
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div 
                        className={`h-3 rounded-full transition-all duration-1000 ${
                          step.status === 'active' 
                            ? 'bg-gradient-to-r from-purple-500 to-indigo-500'
                            : step.status === 'completed'
                            ? 'bg-gradient-to-r from-green-500 to-emerald-500'
                            : 'bg-gray-300'
                        }`}
                        style={{ 
                          width: step.status === 'active' 
                            ? `${setupProgress.nqba}%`
                            : step.status === 'completed' 
                            ? '100%' 
                            : '0%' 
                        }}
                      ></div>
                    </div>
                  </div>
                  
                  <div className="flex-shrink-0">
                    <span className={`px-4 py-2 rounded-full text-sm font-semibold ${
                      step.status === 'active'
                        ? 'bg-purple-100 text-purple-800'
                        : step.status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {step.status === 'active' ? 'In Progress' : 
                       step.status === 'completed' ? 'Completed' : 'Pending'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* NQBA Core Components */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">NQBA Core Components</h2>
            <p className="text-xl text-gray-600">The foundation that powers all business units</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {nqbaComponents.map((component, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
                <div className="text-center">
                  <div className="text-4xl mb-4">{component.icon}</div>
                  <h3 className="text-lg font-bold text-gray-900 mb-2">{component.name}</h3>
                  <div className="flex items-center justify-center space-x-2 mb-3">
                    <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                    <span className="text-sm text-green-600 font-semibold">{component.status}</span>
                  </div>
                  <div className="text-2xl font-bold text-gray-900">{component.efficiency}</div>
                  <p className="text-sm text-gray-600 mt-2">Efficiency</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* System Status */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">System Status</h2>
            <p className="text-xl text-gray-600">Real-time monitoring of platform components</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-gradient-to-br from-purple-500 to-indigo-500 text-white p-6 rounded-xl text-center">
              <div className="text-4xl mb-4">🏗️</div>
              <h3 className="text-xl font-bold mb-2">NQBA Core</h3>
              <p className="text-purple-100 mb-3">{systemStatus.nqba}</p>
              <div className="text-2xl font-bold">Active</div>
            </div>

            <div className="bg-gradient-to-br from-blue-500 to-cyan-500 text-white p-6 rounded-xl text-center">
              <div className="text-4xl mb-4">⚛️</div>
              <h3 className="text-xl font-bold mb-2">Quantum Computing</h3>
              <p className="text-blue-100 mb-3">{systemStatus.quantum}</p>
              <div className="text-2xl font-bold">410x</div>
            </div>

            <div className="bg-gradient-to-br from-green-500 to-emerald-500 text-white p-6 rounded-xl text-center">
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-xl font-bold mb-2">AI Agents</h3>
              <p className="text-green-100 mb-3">{systemStatus.agents}</p>
              <div className="text-2xl font-bold">247</div>
            </div>

            <div className="bg-gradient-to-br from-orange-500 to-red-500 text-white p-6 rounded-xl text-center">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-bold mb-2">Security</h3>
              <p className="text-orange-100 mb-3">{systemStatus.security}</p>
              <div className="text-2xl font-bold">99.9%</div>
            </div>
          </div>
        </div>
      </section>

      {/* Business Unit Setup Links */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Business Unit Configuration</h2>
            <p className="text-xl text-gray-600">Set up individual business units with NQBA integration</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-6xl mb-6">🦊</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">FLYFOX AI</h3>
              <p className="text-gray-600 mb-6">
                Configure the AI platform and business automation systems
              </p>
              <Link 
                href="/setup/flyfox-ai"
                className="inline-block bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-3 rounded-xl font-semibold hover:from-orange-600 hover:to-red-600 transition-all"
              >
                Configure FLYFOX AI →
              </Link>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-6xl mb-6">🏛️</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Goliath Capital</h3>
              <p className="text-gray-600 mb-6">
                Set up financial services and investment management
              </p>
              <Link 
                href="/setup/goliath-capital"
                className="inline-block bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-xl font-semibold hover:from-green-600 hover:to-emerald-600 transition-all"
              >
                Configure Goliath →
              </Link>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-6xl mb-6">Σ</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Sigma Select</h3>
              <p className="text-gray-600 mb-6">
                Configure lead generation and sales optimization
              </p>
              <Link 
                href="/setup/sigma-select"
                className="inline-block bg-gradient-to-r from-blue-500 to-cyan-500 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-600 hover:to-cyan-600 transition-all"
              >
                Configure Sigma →
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Complete the Setup?</h2>
          <p className="text-xl text-purple-100 mb-8 max-w-3xl mx-auto">
            Complete the configuration of your NQBA-powered intelligent economy platform
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/setup_auth" className="bg-white text-purple-600 px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
              Configure Authentication
            </Link>
            <Link href="/platform-dashboard" className="bg-purple-700 text-white px-8 py-4 rounded-xl font-semibold hover:bg-purple-800 transition-colors">
              Access Dashboard
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
