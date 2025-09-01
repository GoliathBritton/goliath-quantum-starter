import Link from 'next/link'
import { Check, Star, Zap, Shield, Target, Users, TrendingUp, DollarSign, ArrowRight, Award, Clock, Headphones } from 'lucide-react'

export default function SubscriptionPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-goliath-600 via-flyfox-600 to-sigma-600 text-white">
        <div className="container mx-auto px-6 py-16">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Choose Your Quantum-Powered Success
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              Transform your business with our proven subscription services
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="font-semibold">410x Performance Boost</span>
              </div>
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="font-semibold">800-1500% ROI</span>
              </div>
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="font-semibold">24/7 Support</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Q-Sales Division™ Packages */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Q-Sales Division™ Packages
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Autonomous sales agents powered by quantum computing and NQBA architecture
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {/* DIY Package */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 relative">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">DIY Package</h3>
                <p className="text-gray-600">Self-Service Platform</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-goliath-600">$997</span>
                  <span className="text-gray-600">/month</span>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Up to 5 Autonomous Sales Agents</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Quantum-Enhanced Lead Scoring</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Multi-Channel Outreach (Email, SMS)</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Basic Analytics Dashboard</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>CSV Contact Import</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Email Support</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Up to 10,000 Contacts</span>
                </div>
              </div>

              <Link href="/contact?package=diy" className="btn-primary w-full text-center">
                Get Started
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </div>

            {/* DFY Package */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-goliath-500 relative transform scale-105">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div className="bg-goliath-500 text-white px-4 py-2 rounded-full text-sm font-semibold">
                  MOST POPULAR
                </div>
              </div>

              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">DFY Package</h3>
                <p className="text-gray-600">Done-For-You Service</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-goliath-600">$2,997</span>
                  <span className="text-gray-600">/month</span>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Up to 25 Autonomous Sales Agents</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Advanced Quantum Optimization</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Multi-Channel Outreach (Email, SMS, Voice)</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Advanced Analytics & Reporting</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom Campaign Strategy</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Dedicated Success Manager</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Priority Support (24/7)</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Up to 100,000 Contacts</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Weekly Performance Reviews</span>
                </div>
              </div>

              <Link href="/contact?package=dfy" className="btn-primary w-full text-center">
                Get Started
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </div>

            {/* Enterprise Package */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 relative">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Enterprise</h3>
                <p className="text-gray-600">Full Customization</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-goliath-600">$9,997</span>
                  <span className="text-gray-600">/month</span>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Unlimited Autonomous Sales Agents</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom Quantum Algorithms</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>All Channels + Custom Integrations</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom Analytics & White-labeling</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom Playbook Development</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Dedicated Account Team</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>24/7 Phone Support</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Unlimited Contacts</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom API Access</span>
                </div>
              </div>

              <Link href="/contact?package=enterprise" className="btn-primary w-full text-center">
                Contact Sales
                <ArrowRight className="w-4 h-4 ml-2" />
              </Link>
            </div>
          </div>

          {/* Q-Sales Division Benefits */}
          <div className="bg-gradient-to-r from-goliath-50 to-goliath-100 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-goliath-800 mb-6 text-center">Q-Sales Division™ Benefits</h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-goliath-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-goliath-800 mb-2">24.7% Conversion Rate</h4>
                <p className="text-sm text-goliath-700">vs industry average of 2-5%</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-goliath-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <DollarSign className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-goliath-800 mb-2">1,247% ROI</h4>
                <p className="text-sm text-goliath-700">Average return on investment</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-goliath-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <Users className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-goliath-800 mb-2">2M+ Contacts</h4>
                <p className="text-sm text-goliath-700">Successfully processed</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sigma Select Packages */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Sigma Select Packages
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Sales intelligence and revenue optimization powered by quantum computing
            </p>
            <div className="mt-4">
              <span className="bg-sigma-100 text-sigma-800 px-4 py-2 rounded-full text-sm font-semibold">
                Coming Soon - Q1 2024
              </span>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8 mb-12">
            {/* Starter Package */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 relative opacity-75">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Starter</h3>
                <p className="text-gray-600">Basic Sales Intelligence</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-sigma-600">$1,497</span>
                  <span className="text-gray-600">/month</span>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Basic Lead Generation</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Simple Analytics Dashboard</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Email Support</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Up to 5,000 Prospects</span>
                </div>
              </div>

              <button className="btn-secondary w-full text-center opacity-50 cursor-not-allowed">
                Coming Soon
              </button>
            </div>

            {/* Professional Package */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-sigma-500 relative opacity-75">
              <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                <div className="bg-sigma-500 text-white px-4 py-2 rounded-full text-sm font-semibold">
                  RECOMMENDED
                </div>
              </div>

              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Professional</h3>
                <p className="text-gray-600">Advanced Analytics</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-sigma-600">$3,497</span>
                  <span className="text-gray-600">/month</span>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Advanced Lead Generation</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Predictive Analytics</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Revenue Intelligence</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Priority Support</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Up to 50,000 Prospects</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom Integrations</span>
                </div>
              </div>

              <button className="btn-secondary w-full text-center opacity-50 cursor-not-allowed">
                Coming Soon
              </button>
            </div>

            {/* Enterprise Package */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 relative opacity-75">
              <div className="text-center mb-6">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">Enterprise</h3>
                <p className="text-gray-600">Full Platform Access</p>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-sigma-600">$12,497</span>
                  <span className="text-gray-600">/month</span>
                </div>
              </div>

              <div className="space-y-4 mb-8">
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Unlimited Lead Generation</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom AI Models</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>White-label Solutions</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Dedicated Account Team</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>24/7 Phone Support</span>
                </div>
                <div className="flex items-center">
                  <Check className="w-5 h-5 text-green-500 mr-3" />
                  <span>Custom API Access</span>
                </div>
              </div>

              <button className="btn-secondary w-full text-center opacity-50 cursor-not-allowed">
                Coming Soon
              </button>
            </div>
          </div>

          {/* Sigma Select Benefits */}
          <div className="bg-gradient-to-r from-sigma-50 to-sigma-100 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-sigma-800 mb-6 text-center">Sigma Select Benefits</h3>
            <div className="grid md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="w-12 h-12 bg-sigma-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-sigma-800 mb-2">78.3% Win Rate</h4>
                <p className="text-sm text-sigma-700">vs industry average of 25%</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-sigma-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-sigma-800 mb-2">312% Pipeline Growth</h4>
                <p className="text-sm text-sigma-700">Average pipeline increase</p>
              </div>
              <div className="text-center">
                <div className="w-12 h-12 bg-sigma-600 rounded-xl flex items-center justify-center mx-auto mb-4">
                  <Clock className="w-6 h-6 text-white" />
                </div>
                <h4 className="font-semibold text-sigma-800 mb-2">45% Faster Sales</h4>
                <p className="text-sm text-sigma-700">Reduced sales cycle time</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Comparison */}
      <section className="py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Feature Comparison
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Compare the features and capabilities across all our packages
            </p>
          </div>

          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-4 text-left text-sm font-semibold text-gray-900">Feature</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold text-gray-900">DIY</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold text-gray-900">DFY</th>
                    <th className="px-6 py-4 text-center text-sm font-semibold text-gray-900">Enterprise</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Autonomous Agents</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Up to 5</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Up to 25</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Quantum Optimization</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Basic</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Advanced</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Custom</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Channels</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Email, SMS</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Email, SMS, Voice</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">All + Custom</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Analytics</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Basic</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Advanced</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Custom</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Support</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Email</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">24/7 Priority</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">24/7 Phone</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Contacts</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">10,000</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">100,000</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">Unlimited</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Success Manager</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">-</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">✓</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">✓</td>
                  </tr>
                  <tr>
                    <td className="px-6 py-4 text-sm text-gray-900">Custom API</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">-</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">-</td>
                    <td className="px-6 py-4 text-center text-sm text-gray-600">✓</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-gradient-to-br from-goliath-600 via-flyfox-600 to-sigma-600 text-white">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
            Join hundreds of companies already achieving unprecedented success with our quantum-powered solutions
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/contact" className="btn-primary bg-white text-goliath-600 hover:bg-gray-100">
              Schedule Demo
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
            <Link href="/case-studies" className="btn-secondary border-white text-white hover:bg-white hover:text-goliath-600">
              View Case Studies
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
