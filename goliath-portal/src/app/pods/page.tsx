import SalesPodDashboard from '@/components/SalesPodDashboard'
import { Rocket, Users, Target, BarChart3, Zap, Brain, Crown, TrendingUp } from 'lucide-react'

export default function PodsPage() {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-goliath-100 text-goliath-800 text-sm font-medium mb-6">
            <Zap className="w-4 h-4 mr-2" />
            Powered by Dynex Quantum Computing (410x Performance)
          </div>
          
          <h1 className="text-4xl md:text-6xl font-extrabold text-gray-900 mb-6">
            Deploy Your{' '}
            <span className="text-gradient">Quantum Sales Pods</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Launch autonomous sales agents that work 24/7, learn continuously, 
            and generate revenue while you focus on strategy.
          </p>
        </div>

        {/* Sales Pod Dashboard */}
        <SalesPodDashboard />

        {/* Pod Types Section */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Choose Your Pod Configuration
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="card text-center">
              <div className="card-header bg-gradient-to-br from-goliath-500 to-goliath-600 text-white">
                <h3 className="text-xl font-bold">Starter Pod</h3>
                <p className="text-goliath-100">5 Agents</p>
              </div>
              <div className="card-content">
                <div className="text-3xl font-bold text-goliath-600 mb-2">$2,500/mo</div>
                <p className="text-sm text-gray-600 mb-4">Perfect for small businesses</p>
                <ul className="text-sm text-gray-600 space-y-1 mb-6">
                  <li>• 5 autonomous agents</li>
                  <li>• Basic campaign automation</li>
                  <li>• Email & SMS campaigns</li>
                  <li>• Standard reporting</li>
                </ul>
                <button className="btn-primary w-full">Deploy Now</button>
              </div>
            </div>
            
            <div className="card text-center">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <h3 className="text-xl font-bold">Growth Pod</h3>
                <p className="text-flyfox-100">25 Agents</p>
              </div>
              <div className="card-content">
                <div className="text-3xl font-bold text-flyfox-600 mb-2">$10,000/mo</div>
                <p className="text-sm text-gray-600 mb-4">Ideal for growing companies</p>
                <ul className="text-sm text-gray-600 space-y-1 mb-6">
                  <li>• 25 autonomous agents</li>
                  <li>• Multi-channel campaigns</li>
                  <li>• Advanced analytics</li>
                  <li>• Priority support</li>
                </ul>
                <button className="btn-primary w-full">Deploy Now</button>
              </div>
            </div>
            
            <div className="card text-center">
              <div className="card-header bg-gradient-to-br from-sigma-500 to-sigma-600 text-white">
                <h3 className="text-xl font-bold">Scale Pod</h3>
                <p className="text-sigma-100">100 Agents</p>
              </div>
              <div className="card-content">
                <div className="text-3xl font-bold text-sigma-600 mb-2">$35,000/mo</div>
                <p className="text-sm text-gray-600 mb-4">For established enterprises</p>
                <ul className="text-sm text-gray-600 space-y-1 mb-6">
                  <li>• 100 autonomous agents</li>
                  <li>• Full automation suite</li>
                  <li>• Custom integrations</li>
                  <li>• Dedicated manager</li>
                </ul>
                <button className="btn-primary w-full">Deploy Now</button>
              </div>
            </div>
            
            <div className="card text-center">
              <div className="card-header bg-gradient-to-br from-gray-700 to-gray-900 text-white">
                <h3 className="text-xl font-bold">Enterprise</h3>
                <p className="text-gray-300">500+ Agents</p>
              </div>
              <div className="card-content">
                <div className="text-3xl font-bold text-gray-700 mb-2">Custom</div>
                <p className="text-sm text-gray-600 mb-4">Full division in a box</p>
                <ul className="text-sm text-gray-600 space-y-1 mb-6">
                  <li>• 500+ autonomous agents</li>
                  <li>• White-label options</li>
                  <li>• Custom development</li>
                  <li>• 24/7 dedicated support</li>
                </ul>
                <button className="btn-secondary w-full">Contact Sales</button>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Metrics */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Expected Performance Metrics
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="card text-center">
              <div className="w-16 h-16 bg-goliath-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Target className="w-8 h-8 text-goliath-600" />
              </div>
              <h3 className="text-2xl font-bold text-goliath-600 mb-2">15-25%</h3>
              <p className="text-gray-600">Conversion Rate</p>
              <p className="text-sm text-gray-500 mt-2">
                Industry average is 2-5%. Our quantum AI achieves 15-25%.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <TrendingUp className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-2xl font-bold text-flyfox-600 mb-2">800-1500%</h3>
              <p className="text-gray-600">ROI (30 days)</p>
              <p className="text-sm text-gray-500 mt-2">
                Typical marketing ROI is 122%. We deliver 800-1500%.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-sigma-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-sigma-600" />
              </div>
              <h3 className="text-2xl font-bold text-sigma-600 mb-2">24/7</h3>
              <p className="text-gray-600">Availability</p>
              <p className="text-sm text-gray-500 mt-2">
                Agents work around the clock, never sleep, never take breaks.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Brain className="w-8 h-8 text-gray-600" />
              </div>
              <h3 className="text-2xl font-bold text-gray-600 mb-2">410x</h3>
              <p className="text-gray-600">Performance Boost</p>
              <p className="text-sm text-gray-500 mt-2">
                Powered by Dynex quantum computing and NVIDIA acceleration.
              </p>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-20">
          <div className="card max-w-4xl mx-auto">
            <div className="card-header bg-gradient-to-br from-goliath-600 to-flyfox-600 text-white">
              <h3 className="text-2xl font-bold">How Quantum Sales Pods Work</h3>
              <p className="text-goliath-100">The future of autonomous sales</p>
            </div>
            <div className="card-content">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-goliath-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl font-bold text-goliath-600">1</span>
                  </div>
                  <h4 className="text-lg font-semibold mb-2">Deploy</h4>
                  <p className="text-sm text-gray-600">
                    Choose your pod size and deploy instantly. Agents are ready in minutes.
                  </p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-flyfox-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl font-bold text-flyfox-600">2</span>
                  </div>
                  <h4 className="text-lg font-semibold mb-2">Learn</h4>
                  <p className="text-sm text-gray-600">
                    Agents learn from every interaction, continuously improving performance.
                  </p>
                </div>
                
                <div className="text-center">
                  <div className="w-16 h-16 bg-sigma-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-2xl font-bold text-sigma-600">3</span>
                  </div>
                  <h4 className="text-lg font-semibold mb-2">Scale</h4>
                  <p className="text-sm text-gray-600">
                    Scale from 5 to 500+ agents as your business grows.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to Launch Your Sales Pods?
          </h3>
          <p className="text-lg text-gray-600 mb-8">
            Join the quantum revolution and deploy autonomous sales agents today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/packages" className="btn-primary">
              View All Packages
            </a>
            <a href="/contacts" className="btn-secondary">
              Import Contacts First
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
