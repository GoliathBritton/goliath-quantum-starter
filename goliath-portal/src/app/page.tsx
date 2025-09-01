import Link from 'next/link'
import { ArrowRight, Zap, Brain, Rocket, Target, Users, BarChart3, Shield } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen gradient-bg">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-goliath-100 text-goliath-800 text-sm font-medium mb-8">
              <Zap className="w-4 h-4 mr-2" />
              Powered by Dynex Quantum Computing (410x Performance)
            </div>
            
            <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 mb-6">
              Welcome to{' '}
              <span className="text-gradient">FLYFOX AI</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Quantum-Powered Business Intelligence Platform. Deploy autonomous agents 
              powered by Dynex quantum computing and NVIDIA acceleration for 410x performance.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link href="/packages" className="btn-primary inline-flex items-center">
                Explore FLYFOX AI Solutions
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link href="/auth/register" className="btn-secondary">
                Start Free Trial
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              The Future of Sales is Here
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Transform your business with autonomous sales agents that work 24/7, 
              learn continuously, and generate revenue while you sleep.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">FLYFOX Quantum AI</h3>
              <p className="text-gray-600">Powered by Dynex neuromorphic computing for 410x performance boost</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Rocket className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Metis Autonomous Agents</h3>
              <p className="text-gray-600">Self-evolving agents powered by FLYFOX AI that learn and improve continuously</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-sigma-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Target className="w-8 h-8 text-sigma-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">SigmaEQ Revenue Engine</h3>
              <p className="text-gray-600">24/7 lead generation and conversion optimization with quantum efficiency</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-gray-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Hyperion Scaling</h3>
              <p className="text-gray-600">Deploy from 1 to 500+ agents instantly with FLYFOX AI orchestration</p>
            </div>
          </div>
        </div>
      </section>

      {/* Business Pillars Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              The Three-Pillar Business Empire
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built on the foundation of quantum computing and AI innovation
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="card">
              <div className="card-header bg-gradient-to-br from-goliath-500 to-goliath-600 text-white">
                <h3 className="text-2xl font-bold">GOLIATH</h3>
                <p className="text-goliath-100">Financial & CRM</p>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  The foundation of your financial empire, handling all lending, insurance, 
                  and CRM operations with quantum-enhanced risk assessment.
                </p>
                <div className="flex items-center text-sm text-goliath-600">
                  <Shield className="w-4 h-4 mr-2" />
                  Quantum Risk Assessment
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <h3 className="text-2xl font-bold">FLYFOX AI</h3>
                <p className="text-flyfox-100">Quantum Intelligence Backbone</p>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  The core technology backbone powering all solutions with Dynex quantum computing, 
                  NVIDIA acceleration, and Metis autonomous agents for 410x performance.
                </p>
                <div className="flex items-center text-sm text-flyfox-600">
                  <Zap className="w-4 h-4 mr-2" />
                  Metis AI + 410x Performance
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="card-header bg-gradient-to-br from-sigma-500 to-sigma-600 text-white">
                <h3 className="text-2xl font-bold">SIGMA SELECT</h3>
                <p className="text-sigma-100">Sales & Revenue</p>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  Revenue generation powerhouse with autonomous sales agents, 
                  lead optimization, and conversion maximization.
                </p>
                <div className="flex items-center text-sm text-sigma-600">
                  <BarChart3 className="w-4 h-4 mr-2" />
                  Revenue Optimization
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-goliath-900">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Deploy FLYFOX AI Solutions?
          </h2>
          <p className="text-xl text-goliath-200 mb-8">
            Join the quantum revolution and deploy Metis autonomous agents that work 24/7 
            to grow your business while you focus on strategy.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/packages" className="btn-primary bg-white text-goliath-900 hover:bg-gray-100">
              View Packages & Pricing
            </Link>
            <Link href="/contacts" className="btn-secondary bg-transparent text-white border-white hover:bg-white hover:text-goliath-900">
              Start Contact Import
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
