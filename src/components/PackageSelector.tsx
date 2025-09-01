"use client"

import { useState } from 'react'
import { Check, Star, Zap, Brain, Rocket, Crown, ArrowRight, TrendingUp, Users, Target } from 'lucide-react'

interface Package {
  id: string
  name: string
  description: string
  monthlyPrice: number
  setupFee: number
  icon: any
  color: string
  features: string[]
  roi: string
  bestFor: string
  badge?: string
}

export default function PackageSelector() {
  const [selectedPackage, setSelectedPackage] = useState<string | null>(null)
  const [isComparing, setIsComparing] = useState(false)

  const packages: Package[] = [
    {
      id: 'diy',
      name: 'DIY (Do-It-Yourself)',
      description: 'Build your own quantum sales division with expert guidance',
      monthlyPrice: 2500,
      setupFee: 0,
      icon: Brain,
      color: 'goliath',
      features: [
        'Full CRM access with quantum enhancement',
        'QHC consultation and guidance',
        'Contact enrichment and scoring',
        'Basic campaign automation',
        'Community access and support',
        'Self-service deployment',
        'Standard reporting and analytics'
      ],
      roi: '800-1200%',
      bestFor: 'Tech-savvy teams who want full control'
    },
    {
      id: 'dfy',
      name: 'DFY (Done-For-You)',
      description: 'Full setup and deployment by our quantum experts',
      monthlyPrice: 10000,
      setupFee: 25000,
      icon: Rocket,
      color: 'flyfox',
      features: [
        'Everything in DIY + full setup',
        'Quantum Architect deployment',
        'Custom campaign creation',
        'Priority support and training',
        'Performance optimization',
        'Advanced analytics dashboard',
        'White-label customization options',
        'Dedicated success manager'
      ],
      roi: '1000-1500%',
      bestFor: 'Growing companies wanting rapid deployment',
      badge: 'Most Popular'
    },
    {
      id: 'enterprise',
      name: 'Enterprise "Division in a Box"',
      description: 'Complete autonomous sales division with 500+ agents',
      monthlyPrice: 50000,
      setupFee: 250000,
      icon: Crown,
      color: 'sigma',
      features: [
        'Everything in DFY + full division',
        '500+ autonomous agents',
        'White-label options',
        '24/7 dedicated support',
        'Category leadership',
        'Custom integrations',
        'Advanced AI training',
        'Revenue guarantee',
        'Strategic consulting'
      ],
      roi: '1200-2000%',
      bestFor: 'Large enterprises and category leaders'
    }
  ]

  const handlePackageSelect = (packageId: string) => {
    setSelectedPackage(packageId)
    setIsComparing(false)
  }

  const handleCompare = () => {
    setIsComparing(!isComparing)
  }

  const selectedPackageData = packages.find(p => p.id === selectedPackage)

  return (
    <div className="space-y-8">
      {/* Package Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {packages.map((pkg) => {
          const Icon = pkg.icon
          const isSelected = selectedPackage === pkg.id
          
          return (
            <div
              key={pkg.id}
              className={`card cursor-pointer transition-all duration-300 ${
                isSelected 
                  ? `ring-2 ring-${pkg.color}-500 shadow-xl transform scale-105` 
                  : 'hover:shadow-lg hover:transform hover:scale-102'
              }`}
              onClick={() => handlePackageSelect(pkg.id)}
            >
              {/* Header */}
              <div className={`card-header bg-gradient-to-br from-${pkg.color}-500 to-${pkg.color}-600 text-white relative`}>
                {pkg.badge && (
                  <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                    <span className="px-3 py-1 bg-yellow-400 text-yellow-900 text-xs font-bold rounded-full">
                      {pkg.badge}
                    </span>
                  </div>
                )}
                
                <div className="flex items-center justify-between mb-2">
                  <Icon className="w-8 h-8" />
                  <div className="text-right">
                    <div className="text-sm opacity-90">Setup Fee</div>
                    <div className="text-lg font-bold">
                      ${pkg.setupFee.toLocaleString()}
                    </div>
                  </div>
                </div>
                
                <h3 className="text-2xl font-bold mb-1">{pkg.name}</h3>
                <p className="text-sm opacity-90">{pkg.description}</p>
              </div>

              {/* Pricing */}
              <div className="card-content">
                <div className="text-center mb-6">
                  <div className="text-4xl font-bold text-gray-900 mb-1">
                    ${pkg.monthlyPrice.toLocaleString()}
                  </div>
                  <div className="text-gray-600">per month</div>
                </div>

                {/* Features */}
                <ul className="space-y-3 mb-6">
                  {pkg.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <Check className={`w-5 h-5 text-${pkg.color}-600 mr-3 mt-0.5 flex-shrink-0`} />
                      <span className="text-sm text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* ROI and Best For */}
                <div className="space-y-3 mb-6">
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Expected ROI:</span>
                    <span className="text-sm font-bold text-green-600">{pkg.roi}</span>
                  </div>
                  <div className="text-xs text-gray-600 text-center">
                    Best for: {pkg.bestFor}
                  </div>
                </div>

                {/* Action Button */}
                <button
                  className={`w-full btn-primary bg-${pkg.color}-600 hover:bg-${pkg.color}-700`}
                  onClick={(e) => {
                    e.stopPropagation()
                    handlePackageSelect(pkg.id)
                  }}
                >
                  {isSelected ? 'Selected' : 'Choose Package'}
                  <ArrowRight className="ml-2 w-4 h-4" />
                </button>
              </div>
            </div>
          )
        })}
      </div>

      {/* Selected Package Details */}
      {selectedPackageData && (
        <div className="card">
          <div className="card-header bg-gradient-to-br from-goliath-600 to-flyfox-600 text-white">
            <h3 className="text-2xl font-bold">Selected Package: {selectedPackageData.name}</h3>
            <p className="text-goliath-100">Ready to deploy your quantum sales division</p>
          </div>
          <div className="card-content">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-3xl font-bold text-goliath-600 mb-2">
                  ${selectedPackageData.monthlyPrice.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600">Monthly Investment</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-flyfox-600 mb-2">
                  ${selectedPackageData.setupFee.toLocaleString()}
                </div>
                <div className="text-sm text-gray-600">Setup Fee</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-sigma-600 mb-2">
                  {selectedPackageData.roi}
                </div>
                <div className="text-sm text-gray-600">Expected ROI</div>
              </div>
            </div>

            <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
              <button className="btn-primary">
                Deploy Now
                <Rocket className="ml-2 w-5 h-5" />
              </button>
              <button className="btn-secondary">
                Schedule Demo
                <Users className="ml-2 w-5 h-5" />
              </button>
              <button className="btn-success">
                Contact Sales
                <Target className="ml-2 w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Compare Button */}
      <div className="text-center">
        <button
          onClick={handleCompare}
          className="btn-secondary"
        >
          {isComparing ? 'Hide Comparison' : 'Compare All Packages'}
        </button>
      </div>

      {/* Comparison Table */}
      {isComparing && (
        <div className="card">
          <div className="card-header bg-gradient-to-br from-gray-600 to-gray-700 text-white">
            <h3 className="text-2xl font-bold">Package Comparison</h3>
            <p className="text-gray-200">See how our packages stack up</p>
          </div>
          <div className="card-content">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 font-semibold">Feature</th>
                    {packages.map((pkg) => (
                      <th key={pkg.id} className="text-center py-3 font-semibold">
                        {pkg.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr>
                    <td className="py-3 font-medium">Monthly Price</td>
                    {packages.map((pkg) => (
                      <td key={pkg.id} className="text-center py-3">
                        ${pkg.monthlyPrice.toLocaleString()}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Setup Fee</td>
                    {packages.map((pkg) => (
                      <td key={pkg.id} className="text-center py-3">
                        ${pkg.setupFee.toLocaleString()}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Expected ROI</td>
                    {packages.map((pkg) => (
                      <td key={pkg.id} className="text-center py-3">
                        {pkg.roi}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Agent Count</td>
                    {packages.map((pkg) => (
                      <td key={pkg.id} className="text-center py-3">
                        {pkg.id === 'diy' ? '5-25' : pkg.id === 'dfy' ? '25-100' : '500+'}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="py-3 font-medium">Support Level</td>
                    {packages.map((pkg) => (
                      <td key={pkg.id} className="text-center py-3">
                        {pkg.id === 'diy' ? 'Community' : pkg.id === 'dfy' ? 'Priority' : '24/7 Dedicated'}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
