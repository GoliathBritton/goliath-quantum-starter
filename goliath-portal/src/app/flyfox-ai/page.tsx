import Link from 'next/link'
import { 
  Brain, 
  Zap, 
  Rocket, 
  Target, 
  Users, 
  BarChart3, 
  Shield, 
  Cpu, 
  Database, 
  Network, 
  Activity,
  ArrowRight,
  CheckCircle,
  Star
} from 'lucide-react'

export default function FlyfoxAIPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-flyfox-900 via-flyfox-800 to-flyfox-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-flyfox-100 text-flyfox-800 text-sm font-medium mb-8">
              <Zap className="w-4 h-4 mr-2" />
              Powered by Dynex Quantum Computing (410x Performance)
            </div>
            
            <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6">
              FLYFOX AI
            </h1>
            
            <p className="text-xl md:text-2xl text-flyfox-100 mb-8 max-w-4xl mx-auto">
              The Quantum Intelligence Backbone. Deploy Metis autonomous agents, 
              Hyperion scaling, and quantum-enhanced solutions across your entire business.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
              <Link href="/packages" className="btn-primary bg-white text-flyfox-900 hover:bg-gray-100 inline-flex items-center">
                Explore Solutions
                <ArrowRight className="ml-2 w-5 h-5" />
              </Link>
              <Link href="/case-studies" className="btn-secondary bg-transparent text-white border-white hover:bg-white hover:text-flyfox-900">
                View Case Studies
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Core Technology Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              The FLYFOX AI Technology Stack
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built on the foundation of quantum computing, neuromorphic processing, and autonomous intelligence
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="card border-2 border-flyfox-200">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">Metis AI</h3>
                  <Brain className="w-6 h-6" />
                </div>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  Autonomous intelligence agents that learn, adapt, and optimize continuously. 
                  Named after the Greek goddess of wisdom and strategic warfare.
                </p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    Strategic decision making
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    Context-aware responses
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    Self-evolving capabilities
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="card border-2 border-flyfox-200">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">Hyperion Scaling</h3>
                  <Rocket className="w-6 h-6" />
                </div>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  Named after the Titan of light and observation. Scales from 1 to 500+ 
                  agents instantly with quantum orchestration.
                </p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    Instant agent deployment
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    Quantum load balancing
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    Performance optimization
                  </li>
                </ul>
              </div>
            </div>
            
            <div className="card border-2 border-flyfox-200">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">Dynex Quantum</h3>
                  <Cpu className="w-6 h-6" />
                </div>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  410x performance boost through neuromorphic quantum computing 
                  with NVIDIA acceleration.
                </p>
                <ul className="space-y-2 text-sm">
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    410x performance multiplier
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    NVIDIA GPU acceleration
                  </li>
                  <li className="flex items-center">
                    <CheckCircle className="w-4 h-4 text-flyfox-600 mr-2" />
                    QUBO optimization
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Solutions Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              FLYFOX AI Solutions
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive business solutions powered by quantum intelligence
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="card">
              <div className="card-header bg-gradient-to-br from-goliath-500 to-goliath-600 text-white">
                <h3 className="text-2xl font-bold">GOLIATH</h3>
                <p className="text-goliath-100">Financial & CRM Solutions</p>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  Quantum-enhanced financial services, lending, insurance, and CRM 
                  operations with advanced risk assessment.
                </p>
                <div className="flex items-center text-sm text-goliath-600 mb-4">
                  <Shield className="w-4 h-4 mr-2" />
                  Quantum Risk Assessment
                </div>
                <Link href="/packages" className="text-flyfox-600 hover:text-flyfox-700 font-medium">
                  Explore Goliath Solutions →
                </Link>
              </div>
            </div>
            
            <div className="card border-2 border-flyfox-200">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <h3 className="text-2xl font-bold">FLYFOX AI</h3>
                <p className="text-flyfox-100">Core Technology Backbone</p>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  The quantum intelligence backbone powering all solutions with 
                  Metis AI, Hyperion scaling, and Dynex quantum computing.
                </p>
                <div className="flex items-center text-sm text-flyfox-600 mb-4">
                  <Zap className="w-4 h-4 mr-2" />
                  Metis AI + 410x Performance
                </div>
                <Link href="/packages" className="text-flyfox-600 hover:text-flyfox-700 font-medium">
                  Explore FLYFOX AI Solutions →
                </Link>
              </div>
            </div>
            
            <div className="card">
              <div className="card-header bg-gradient-to-br from-sigma-500 to-sigma-600 text-white">
                <h3 className="text-2xl font-bold">SIGMA SELECT</h3>
                <p className="text-sigma-100">Sales & Revenue Engine</p>
              </div>
              <div className="card-content">
                <p className="text-gray-600 mb-4">
                  Revenue generation powerhouse with SigmaEQ framework, autonomous 
                  sales agents, and conversion optimization.
                </p>
                <div className="flex items-center text-sm text-sigma-600 mb-4">
                  <BarChart3 className="w-4 h-4 mr-2" />
                  SigmaEQ Revenue Engine
                </div>
                <Link href="/packages" className="text-flyfox-600 hover:text-flyfox-700 font-medium">
                  Explore Sigma Select Solutions →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Metrics */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              FLYFOX AI Performance Metrics
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Real-world performance improvements powered by quantum computing
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Activity className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">410x</h3>
              <p className="text-gray-600">Performance Boost</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Target className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">24.7%</h3>
              <p className="text-gray-600">Conversion Rate</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">500+</h3>
              <p className="text-gray-600">Agents Deployed</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Star className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">99.9%</h3>
              <p className="text-gray-600">Uptime</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-flyfox-900">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Deploy FLYFOX AI?
          </h2>
          <p className="text-xl text-flyfox-200 mb-8">
            Join the quantum revolution and transform your business with 
            Metis autonomous agents and Hyperion scaling.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/packages" className="btn-primary bg-white text-flyfox-900 hover:bg-gray-100">
              View Solutions & Pricing
            </Link>
            <Link href="/case-studies" className="btn-secondary bg-transparent text-white border-white hover:bg-white hover:text-flyfox-900">
              See Case Studies
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
