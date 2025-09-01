import PackageSelector from '@/components/PackageSelector'
import { Check, Star, Zap, Brain, Rocket, Crown } from 'lucide-react'

export default function PackagesPage() {
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
            Choose Your{' '}
            <span className="text-gradient">FLYFOX AI Solution</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            From DIY deployment to full enterprise "Metis AI Division" - every tier 
            powered by FLYFOX quantum computing and autonomous agents.
          </p>
        </div>

        {/* Package Selector */}
        <PackageSelector />

        {/* Features Comparison */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            What You Get with Each Tier
          </h2>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* DIY Features */}
            <div className="card">
              <div className="card-header bg-gradient-to-br from-goliath-500 to-goliath-600 text-white">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">DIY Features</h3>
                  <Brain className="w-6 h-6" />
                </div>
              </div>
              <div className="card-content">
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-goliath-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Full CRM access with quantum enhancement</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-goliath-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>QHC consultation and guidance</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-goliath-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Contact enrichment and scoring</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-goliath-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Basic campaign automation</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-goliath-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Community access and support</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* DFY Features */}
            <div className="card">
              <div className="card-header bg-gradient-to-br from-flyfox-500 to-flyfox-600 text-white">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">DFY Features</h3>
                  <Rocket className="w-6 h-6" />
                </div>
              </div>
              <div className="card-content">
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-flyfox-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Everything in DIY + full setup</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-flyfox-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Quantum Architect deployment</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-flyfox-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Custom campaign creation</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-flyfox-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Priority support and training</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-flyfox-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Performance optimization</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Enterprise Features */}
            <div className="card">
              <div className="card-header bg-gradient-to-br from-sigma-500 to-sigma-600 text-white">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-bold">Enterprise Features</h3>
                  <Crown className="w-6 h-6" />
                </div>
              </div>
              <div className="card-content">
                <ul className="space-y-3">
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-sigma-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Everything in DFY + full division</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-sigma-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>500+ autonomous agents</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-sigma-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>White-label options</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-sigma-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>24/7 dedicated support</span>
                  </li>
                  <li className="flex items-start">
                    <Check className="w-5 h-5 text-sigma-600 mr-3 mt-0.5 flex-shrink-0" />
                    <span>Category leadership</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* ROI Calculator */}
        <div className="mt-20">
          <div className="card max-w-4xl mx-auto">
            <div className="card-header bg-gradient-to-br from-goliath-600 to-flyfox-600 text-white">
              <h3 className="text-2xl font-bold">ROI Calculator</h3>
              <p className="text-goliath-100">See the potential returns on your investment</p>
            </div>
            <div className="card-content">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
                <div>
                  <div className="text-3xl font-bold text-goliath-600 mb-2">800-1500%</div>
                  <div className="text-sm text-gray-600">Expected ROI (30 days)</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-flyfox-600 mb-2">24/7</div>
                  <div className="text-sm text-gray-600">Agent availability</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-sigma-600 mb-2">410x</div>
                  <div className="text-sm text-gray-600">Performance boost</div>
                </div>
              </div>
              
              <div className="mt-8 p-4 bg-gray-50 rounded-xl">
                <p className="text-sm text-gray-600">
                  <strong>Example:</strong> A $15,000/month DFY package can generate $120,000-$225,000 
                  in additional revenue within 30 days, representing an 800-1500% ROI.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to Transform Your Business?
          </h3>
          <p className="text-lg text-gray-600 mb-8">
            Join the quantum revolution and deploy your autonomous sales division today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="#packages" className="btn-primary">
              View All Packages
            </a>
            <a href="/contacts" className="btn-secondary">
              Start with Contact Import
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
