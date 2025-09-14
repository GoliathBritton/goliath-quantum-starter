import React from "react";
import Link from "next/link";
import Head from "next/head";

export default function Home() {
  return (
    <>
      <Head>
        <title>FLYFOX AI - Quantum Platform</title>
        <meta name="description" content="Quantum-enhanced business automation platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900">
        <div className="container mx-auto px-6 py-12">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-white mb-4 quantum-glow">
              🚀 FLYFOX AI Quantum Platform
            </h1>
            <p className="text-xl text-gray-300 mb-8">
              Next-generation business automation powered by quantum computing
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            {/* Workflow Builder Card */}
            <Link href="/workflow-builder">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 hover:bg-white/20 transition-all duration-300 cursor-pointer border border-gray-600 hover:border-flyfox">
                <div className="text-center">
                  <div className="text-4xl mb-4">⚡</div>
                  <h2 className="text-2xl font-bold text-white mb-4">
                    Quantum Workflow Builder
                  </h2>
                  <p className="text-gray-300 mb-6">
                    Design and deploy quantum-enhanced business workflows with
                    drag-and-drop simplicity. Premium nodes leverage Dynex QUBO
                    optimization for superior performance.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    <span className="px-3 py-1 bg-flyfox text-black rounded-full text-sm">
                      ReactFlow
                    </span>
                    <span className="px-3 py-1 bg-pink-600 text-white rounded-full text-sm">
                      ⚡ Quantum
                    </span>
                    <span className="px-3 py-1 bg-purple-600 text-white rounded-full text-sm">
                      QUBO
                    </span>
                  </div>
                </div>
              </div>
            </Link>

            {/* Entanglement Map Card */}
            <Link href="/entanglement-map">
              <div className="bg-white/10 backdrop-blur-sm rounded-xl p-8 hover:bg-white/20 transition-all duration-300 cursor-pointer border border-gray-600 hover:border-flyfox">
                <div className="text-center">
                  <div className="text-4xl mb-4">🌐</div>
                  <h2 className="text-2xl font-bold text-white mb-4">
                    3D Entanglement Map
                  </h2>
                  <p className="text-gray-300 mb-6">
                    Visualize your quantum ecosystem in real-time 3D. Monitor
                    agent activity, system entanglements, and quantum processing
                    flows across your entire business infrastructure.
                  </p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    <span className="px-3 py-1 bg-flyfox text-black rounded-full text-sm">
                      3D Visualization
                    </span>
                    <span className="px-3 py-1 bg-green-600 text-white rounded-full text-sm">
                      Live Data
                    </span>
                    <span className="px-3 py-1 bg-blue-600 text-white rounded-full text-sm">
                      Three.js
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          </div>

          {/* Features Grid */}
          <div className="mt-16 grid md:grid-cols-3 gap-6 max-w-6xl mx-auto">
            <div className="bg-white/5 rounded-lg p-6 text-center">
              <div className="text-2xl mb-3">🧠</div>
              <h3 className="text-lg font-semibold text-white mb-2">
                Quantum Intelligence
              </h3>
              <p className="text-gray-400 text-sm">
                NQBA-powered decision making with quantum advantage
              </p>
            </div>
            
            <div className="bg-white/5 rounded-lg p-6 text-center">
              <div className="text-2xl mb-3">🔗</div>
              <h3 className="text-lg font-semibold text-white mb-2">
                Dynex Integration
              </h3>
              <p className="text-gray-400 text-sm">
                Neuromorphic computing for complex optimization problems
              </p>
            </div>
            
            <div className="bg-white/5 rounded-lg p-6 text-center">
              <div className="text-2xl mb-3">📊</div>
              <h3 className="text-lg font-semibold text-white mb-2">
                Real-time Analytics
              </h3>
              <p className="text-gray-400 text-sm">
                Live monitoring and quantum performance insights
              </p>
            </div>
          </div>

          {/* CTA Section */}
          <div className="mt-16 text-center">
            <div className="bg-white/5 rounded-xl p-8 max-w-2xl mx-auto">
              <h3 className="text-2xl font-bold text-white mb-4">
                Ready to Experience Quantum Business Automation?
              </h3>
              <p className="text-gray-300 mb-6">
                Join the quantum revolution and transform your business operations
                with AI-powered automation and quantum optimization.
              </p>
              <div className="flex gap-4 justify-center">
                <Link href="/workflow-builder">
                  <button className="px-6 py-3 bg-flyfox text-black rounded-lg font-medium hover:bg-opacity-90 transition-colors">
                    Start Building
                  </button>
                </Link>
                <Link href="/entanglement-map">
                  <button className="px-6 py-3 bg-transparent border border-flyfox text-flyfox rounded-lg font-medium hover:bg-flyfox hover:text-black transition-colors">
                    Explore Map
                  </button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}