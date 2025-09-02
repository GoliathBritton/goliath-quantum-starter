import Link from "next/link";
import { useState, useEffect } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Home() {
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
  }, []);

  const features = [
    {
      title: "Quantum Computing",
      subtitle: "410x Performance Boost",
      description: "Experience unprecedented computational power with our quantum-optimized algorithms and Dynex integration.",
      icon: "⚛️",
      stats: "410x faster"
    },
    {
      title: "AI Automation",
      subtitle: "Self-Learning Agents",
      description: "Deploy autonomous AI agents that continuously evolve and optimize your business processes without human intervention.",
      icon: "🧠",
      stats: "24/7 operation"
    },
    {
      title: "NQBA Architecture",
      subtitle: "Neuromorphic Foundation",
      description: "Built on our proprietary Neuromorphic Quantum Business Architecture for intelligent decision-making at scale.",
      icon: "🏗️",
      stats: "99.9% uptime"
    }
  ];

  const algorithms = [
    {
      name: "Deutsch-Jozsa",
      description: "Quantum function evaluation with exponential speedup",
      complexity: "O(1) vs O(2^n)",
      category: "Function Analysis"
    },
    {
      name: "Grover's Search",
      description: "Database search with quadratic speedup",
      complexity: "O(√N) vs O(N)",
      category: "Search & Optimization"
    },
    {
      name: "Shor's Algorithm",
      description: "Integer factorization for cryptography",
      complexity: "Exponential speedup",
      category: "Cryptography"
    },
    {
      name: "Quantum ML",
      description: "Machine learning with quantum enhancement",
      complexity: "Variable speedup",
      category: "Artificial Intelligence"
    }
  ];

  return (
    <>
      <Header />
      <main className="min-h-screen bg-white">
        {/* Hero Section - Dynex Style */}
        <section className="relative bg-gradient-to-br from-slate-50 to-blue-50 overflow-hidden">
          <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
          <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
            <div className="text-center">
              {/* Status Badge */}
              <div className={`inline-flex items-center px-4 py-2 rounded-full bg-blue-100 text-blue-800 text-sm font-medium mb-8 transition-all duration-1000 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
                <div className="w-2 h-2 bg-green-500 rounded-full mr-2"></div>
                FLYFOX AI Platform Live
              </div>

              {/* Main Headline */}
              <h1 className={`text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 transition-all duration-1000 delay-200 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                The Future of
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                  Quantum Computing
                </span>
              </h1>

              {/* Subtitle */}
              <p className={`text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto mb-12 leading-relaxed transition-all duration-1000 delay-400 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                FLYFOX AI delivers 410x performance boost through neuromorphic quantum business architecture. 
                Transform your business with autonomous AI agents and quantum-optimized algorithms.
              </p>

              {/* CTA Buttons */}
              <div className={`flex flex-col sm:flex-row gap-4 justify-center mb-16 transition-all duration-1000 delay-600 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                <Link 
                  href="/platform/jobs" 
                  className="inline-flex items-center justify-center px-8 py-4 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  Start Building
                </Link>
                <Link 
                  href="/docs" 
                  className="inline-flex items-center justify-center px-8 py-4 border-2 border-gray-300 text-gray-700 font-semibold rounded-lg hover:border-blue-600 hover:text-blue-600 transition-all duration-200"
                >
                  View Documentation
                </Link>
              </div>

              {/* Stats Grid */}
              <div className={`grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto transition-all duration-1000 delay-800 ${isLoaded ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
                <div className="text-center">
                  <div className="text-4xl md:text-5xl font-bold text-blue-600 mb-2">410x</div>
                  <div className="text-gray-600">Performance Boost</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl md:text-5xl font-bold text-purple-600 mb-2">99.9%</div>
                  <div className="text-gray-600">Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-4xl md:text-5xl font-bold text-green-600 mb-2">24/7</div>
                  <div className="text-gray-600">AI Monitoring</div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                Why Choose FLYFOX AI?
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Built on cutting-edge quantum computing and AI technology to deliver unprecedented business value.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {features.map((feature, index) => (
                <div key={index} className="group bg-white border border-gray-200 rounded-2xl p-8 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2">
                  <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-2xl text-white mb-6 group-hover:scale-110 transition-transform">
                    {feature.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-blue-600 font-semibold mb-4">{feature.subtitle}</p>
                  <p className="text-gray-600 leading-relaxed mb-6">{feature.description}</p>
                  <div className="text-sm font-medium text-gray-500">{feature.stats}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Algorithm Library Section */}
        <section className="py-24 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                Quantum Algorithm Library
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Explore our comprehensive collection of quantum algorithms, each demonstrating unique quantum advantages.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {algorithms.map((algo, index) => (
                <div key={index} className="bg-white border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all duration-300">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-bold text-gray-900 mb-1">{algo.name}</h3>
                      <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 text-sm font-medium rounded-full">
                        {algo.category}
                      </span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm font-medium text-gray-500">Complexity</div>
                      <div className="text-sm font-mono text-gray-700">{algo.complexity}</div>
                    </div>
                  </div>
                  <p className="text-gray-600 mb-4">{algo.description}</p>
                  <button className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors">
                    Run Algorithm
                  </button>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Technology Stack Section */}
        <section className="py-24 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                Technology Stack
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Built on the most advanced quantum computing and AI technologies available today.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {/* Dynex Integration */}
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200 rounded-2xl p-8">
                <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                  ⚛️
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Dynex Quantum</h3>
                <p className="text-gray-600 mb-4">
                  Powered by Dynex's quantum computing infrastructure for 410x performance boost.
                </p>
                <div className="text-sm font-medium text-blue-600">410x faster processing</div>
              </div>

              {/* NQBA Core */}
              <div className="bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200 rounded-2xl p-8">
                <div className="w-16 h-16 bg-purple-600 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                  🏗️
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">NQBA Architecture</h3>
                <p className="text-gray-600 mb-4">
                  Neuromorphic Quantum Business Architecture for intelligent decision-making.
                </p>
                <div className="text-sm font-medium text-purple-600">99.9% uptime</div>
              </div>

              {/* AI Agents */}
              <div className="bg-gradient-to-br from-green-50 to-green-100 border border-green-200 rounded-2xl p-8">
                <div className="w-16 h-16 bg-green-600 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                  🧠
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">AI Automation</h3>
                <p className="text-gray-600 mb-4">
                  Self-learning agents that continuously optimize business processes.
                </p>
                <div className="text-sm font-medium text-green-600">24/7 autonomous operation</div>
              </div>
            </div>
          </div>
        </section>

        {/* Web3 Integration Section */}
        <section className="py-24 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                Web3 Native Features
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Experience the future of decentralized identity and achievement tracking.
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
              {/* Wallet Connection */}
              <div className="bg-white border border-gray-200 rounded-2xl p-8">
                <div className="w-16 h-16 bg-gradient-to-br from-orange-500 to-red-500 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                  🔐
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Connect Your Wallet</h3>
                <p className="text-gray-600 mb-6">
                  Sign in with Ethereum to unlock personalized experiences and track your quantum computing achievements.
                </p>
                
                <div className="space-y-3">
                  <button className="w-full bg-orange-500 text-white py-3 px-6 rounded-lg font-semibold hover:bg-orange-600 transition-colors">
                    Connect MetaMask
                  </button>
                  <button className="w-full bg-blue-500 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-600 transition-colors">
                    Connect WalletConnect
                  </button>
                </div>
              </div>

              {/* Achievements */}
              <div className="bg-white border border-gray-200 rounded-2xl p-8">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-2xl text-white mb-6">
                  🏆
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4">On-Chain Achievements</h3>
                <p className="text-gray-600 mb-6">
                  Mint free, gas-optimized NFTs as proof of your quantum computing milestones.
                </p>
                
                <div className="space-y-3">
                  {[
                    { name: "First Algorithm Run", status: "unlocked", icon: "⚛️" },
                    { name: "Quantum Explorer", status: "unlocked", icon: "🔍" },
                    { name: "Web3 Pioneer", status: "locked", icon: "🌐" }
                  ].map((achievement, index) => (
                    <div key={index} className={`flex items-center space-x-3 p-3 rounded-lg ${achievement.status === 'unlocked' ? 'bg-green-50 border border-green-200' : 'bg-gray-50 border border-gray-200'}`}>
                      <div className="text-xl">{achievement.icon}</div>
                      <div className="flex-1">
                        <div className="font-semibold text-gray-900">{achievement.name}</div>
                        <div className="text-sm text-gray-500">{achievement.status === 'unlocked' ? 'Unlocked' : 'Locked'}</div>
                      </div>
                      {achievement.status === 'unlocked' && (
                        <div className="text-green-500">✓</div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-24 bg-blue-600">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-blue-100 max-w-3xl mx-auto mb-12">
              Join thousands of businesses already using FLYFOX AI to achieve quantum advantage in their operations.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link 
                href="/platform/jobs" 
                className="inline-flex items-center justify-center px-8 py-4 bg-white text-blue-600 font-semibold rounded-lg hover:bg-gray-100 transition-all duration-200 transform hover:scale-105"
              >
                Start Building Now
              </Link>
              <Link 
                href="/contact" 
                className="inline-flex items-center justify-center px-8 py-4 border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-blue-600 transition-all duration-200"
              >
                Contact Sales
              </Link>
            </div>
          </div>
        </section>
      </main>
      <Footer />
    </>
  );
}