import Link from 'next/link'
import { ArrowRight, TrendingUp, Users, DollarSign, Zap, Brain, Shield, Target, Rocket, Award, CheckCircle } from 'lucide-react'

export default function CaseStudiesPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-goliath-600 via-flyfox-600 to-sigma-600 text-white">
        <div className="container mx-auto px-6 py-16">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Proven Results Across All Pillars
            </h1>
            <p className="text-xl md:text-2xl mb-8 opacity-90">
              Real-world evidence of quantum-powered success in finance, technology, and sales
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="font-semibold">410x Performance Boost</span>
              </div>
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="font-semibold">800-1500% ROI</span>
              </div>
              <div className="bg-white bg-opacity-20 px-4 py-2 rounded-full">
                <span className="font-semibold">15-25% Conversion Rate</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6">
          <div className="flex flex-wrap justify-center space-x-1 py-4">
            <a href="#goliath" className="px-6 py-3 rounded-lg bg-goliath-100 text-goliath-700 font-semibold hover:bg-goliath-200 transition-colors">
              🏢 Goliath Financial
            </a>
            <a href="#flyfox" className="px-6 py-3 rounded-lg bg-flyfox-100 text-flyfox-700 font-semibold hover:bg-flyfox-200 transition-colors">
              🦊 FLYFOX AI
            </a>
            <a href="#sigma" className="px-6 py-3 rounded-lg bg-sigma-100 text-sigma-700 font-semibold hover:bg-sigma-200 transition-colors">
              🎯 Sigma Select
            </a>
          </div>
        </div>
      </div>

      {/* Goliath Financial Case Studies */}
      <section id="goliath" className="py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center mb-4">
              <Shield className="w-8 h-8 text-goliath-600 mr-3" />
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900">Goliath Financial</h2>
            </div>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Quantum-enhanced financial services, lending, and CRM operations delivering unprecedented results
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {/* Case Study 1 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-goliath-100 rounded-xl flex items-center justify-center mr-4">
                  <DollarSign className="w-6 h-6 text-goliath-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Quantum Lending Platform</h3>
                  <p className="text-sm text-gray-500">Fortune 500 Bank</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Loan Processing Speed</span>
                  <span className="font-bold text-green-600">95% Faster</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Risk Assessment Accuracy</span>
                  <span className="font-bold text-green-600">99.2%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Revenue Increase</span>
                  <span className="font-bold text-green-600">$47M Annual</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Customer Satisfaction</span>
                  <span className="font-bold text-green-600">98.5%</span>
                </div>
              </div>

              <div className="bg-goliath-50 p-4 rounded-lg">
                <h4 className="font-semibold text-goliath-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-goliath-700">
                  Dynex quantum computing processes 10,000+ loan applications simultaneously, 
                  reducing approval time from 3 weeks to 24 hours while maintaining 99.2% accuracy.
                </p>
              </div>
            </div>

            {/* Case Study 2 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-goliath-100 rounded-xl flex items-center justify-center mr-4">
                  <Users className="w-6 h-6 text-goliath-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Quantum CRM System</h3>
                  <p className="text-sm text-gray-500">Global Insurance Company</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Lead Conversion Rate</span>
                  <span className="font-bold text-green-600">23.7%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Customer Retention</span>
                  <span className="font-bold text-green-600">94.2%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Revenue Growth</span>
                  <span className="font-bold text-green-600">156% YoY</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Operational Efficiency</span>
                  <span className="font-bold text-green-600">78% Improvement</span>
                </div>
              </div>

              <div className="bg-goliath-50 p-4 rounded-lg">
                <h4 className="font-semibold text-goliath-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-goliath-700">
                  AI-powered customer insights predict churn with 94.2% accuracy, 
                  enabling proactive retention strategies that increased revenue by 156%.
                </p>
              </div>
            </div>

            {/* Case Study 3 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-goliath-100 rounded-xl flex items-center justify-center mr-4">
                  <TrendingUp className="w-6 h-6 text-goliath-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Portfolio Optimization</h3>
                  <p className="text-sm text-gray-500">Investment Management Firm</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Portfolio Performance</span>
                  <span className="font-bold text-green-600">+18.7% Alpha</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Risk Reduction</span>
                  <span className="font-bold text-green-600">34% Lower</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Assets Under Management</span>
                  <span className="font-bold text-green-600">$2.8B Growth</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Client Satisfaction</span>
                  <span className="font-bold text-green-600">96.8%</span>
                </div>
              </div>

              <div className="bg-goliath-50 p-4 rounded-lg">
                <h4 className="font-semibold text-goliath-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-goliath-700">
                  Quantum algorithms optimize portfolios across 10,000+ variables in real-time, 
                  delivering 18.7% alpha while reducing risk by 34%.
                </p>
              </div>
            </div>
          </div>

          {/* Goliath Metrics Summary */}
          <div className="bg-gradient-to-r from-goliath-50 to-goliath-100 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-goliath-800 mb-6 text-center">Goliath Financial Impact Summary</h3>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-goliath-600 mb-2">$2.8B</div>
                <div className="text-sm text-goliath-700">Assets Under Management Growth</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-goliath-600 mb-2">156%</div>
                <div className="text-sm text-goliath-700">Average Revenue Growth</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-goliath-600 mb-2">99.2%</div>
                <div className="text-sm text-goliath-700">Risk Assessment Accuracy</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-goliath-600 mb-2">96.8%</div>
                <div className="text-sm text-goliath-700">Client Satisfaction Rate</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FLYFOX AI Case Studies */}
      <section id="flyfox" className="py-16 bg-white">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center mb-4">
              <Zap className="w-8 h-8 text-flyfox-600 mr-3" />
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900">FLYFOX AI</h2>
            </div>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Transformational technology and energy optimization solutions powered by quantum computing
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {/* Case Study 1 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-flyfox-100 rounded-xl flex items-center justify-center mr-4">
                  <Brain className="w-6 h-6 text-flyfox-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">AI-Powered Energy Optimization</h3>
                  <p className="text-sm text-gray-500">Manufacturing Corporation</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Energy Savings</span>
                  <span className="font-bold text-green-600">42.3%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Carbon Reduction</span>
                  <span className="font-bold text-green-600">67,000 Tons/Year</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Cost Savings</span>
                  <span className="font-bold text-green-600">$8.7M Annual</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">ROI</span>
                  <span className="font-bold text-green-600">1,247%</span>
                </div>
              </div>

              <div className="bg-flyfox-50 p-4 rounded-lg">
                <h4 className="font-semibold text-flyfox-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-flyfox-700">
                  Quantum algorithms optimize energy consumption across 50+ facilities in real-time, 
                  achieving 42.3% energy savings and $8.7M annual cost reduction.
                </p>
              </div>
            </div>

            {/* Case Study 2 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-flyfox-100 rounded-xl flex items-center justify-center mr-4">
                  <Rocket className="w-6 h-6 text-flyfox-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Autonomous AI Platform</h3>
                  <p className="text-sm text-gray-500">Technology Startup</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Development Speed</span>
                  <span className="font-bold text-green-600">8x Faster</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Code Quality</span>
                  <span className="font-bold text-green-600">94.7%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Time to Market</span>
                  <span className="font-bold text-green-600">75% Reduction</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Valuation Growth</span>
                  <span className="font-bold text-green-600">$120M</span>
                </div>
              </div>

              <div className="bg-flyfox-50 p-4 rounded-lg">
                <h4 className="font-semibold text-flyfox-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-flyfox-700">
                  AI-powered development platform generates production-ready code 8x faster, 
                  reducing time to market by 75% and increasing company valuation by $120M.
                </p>
              </div>
            </div>

            {/* Case Study 3 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-flyfox-100 rounded-xl flex items-center justify-center mr-4">
                  <Award className="w-6 h-6 text-flyfox-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Predictive Analytics</h3>
                  <p className="text-sm text-gray-500">Healthcare Network</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Diagnostic Accuracy</span>
                  <span className="font-bold text-green-600">97.3%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Treatment Success</span>
                  <span className="font-bold text-green-600">89.2%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Cost Reduction</span>
                  <span className="font-bold text-green-600">$15.2M Annual</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Patient Outcomes</span>
                  <span className="font-bold text-green-600">34% Improvement</span>
                </div>
              </div>

              <div className="bg-flyfox-50 p-4 rounded-lg">
                <h4 className="font-semibold text-flyfox-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-flyfox-700">
                  Quantum-enhanced AI analyzes patient data with 97.3% accuracy, 
                  improving treatment success by 89.2% and reducing costs by $15.2M annually.
                </p>
              </div>
            </div>
          </div>

          {/* FLYFOX Metrics Summary */}
          <div className="bg-gradient-to-r from-flyfox-50 to-flyfox-100 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-flyfox-800 mb-6 text-center">FLYFOX AI Impact Summary</h3>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-flyfox-600 mb-2">42.3%</div>
                <div className="text-sm text-flyfox-700">Average Energy Savings</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-flyfox-600 mb-2">8x</div>
                <div className="text-sm text-flyfox-700">Development Speed Increase</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-flyfox-600 mb-2">97.3%</div>
                <div className="text-sm text-flyfox-700">AI Accuracy Rate</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-flyfox-600 mb-2">1,247%</div>
                <div className="text-sm text-flyfox-700">Average ROI</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sigma Select Case Studies */}
      <section id="sigma" className="py-16">
        <div className="container mx-auto px-6">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center mb-4">
              <Target className="w-8 h-8 text-sigma-600 mr-3" />
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900">Sigma Select</h2>
            </div>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Sales intelligence and revenue optimization powered by quantum computing and autonomous agents
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-12">
            {/* Case Study 1 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-sigma-100 rounded-xl flex items-center justify-center mr-4">
                  <Users className="w-6 h-6 text-sigma-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Q-Sales Division™</h3>
                  <p className="text-sm text-gray-500">SaaS Company</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Conversion Rate</span>
                  <span className="font-bold text-green-600">24.7%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Revenue Growth</span>
                  <span className="font-bold text-green-600">1,247%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Lead Processing</span>
                  <span className="font-bold text-green-600">2M Contacts</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">ROI</span>
                  <span className="font-bold text-green-600">1,247%</span>
                </div>
              </div>

              <div className="bg-sigma-50 p-4 rounded-lg">
                <h4 className="font-semibold text-sigma-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-sigma-700">
                  Autonomous sales agents process 2M contacts with 24.7% conversion rate, 
                  generating 1,247% revenue growth and ROI through quantum-optimized outreach.
                </p>
              </div>
            </div>

            {/* Case Study 2 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-sigma-100 rounded-xl flex items-center justify-center mr-4">
                  <TrendingUp className="w-6 h-6 text-sigma-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Revenue Intelligence</h3>
                  <p className="text-sm text-gray-500">Enterprise Software</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Pipeline Growth</span>
                  <span className="font-bold text-green-600">312%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Deal Size</span>
                  <span className="font-bold text-green-600">+67%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Sales Cycle</span>
                  <span className="font-bold text-green-600">-45%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Win Rate</span>
                  <span className="font-bold text-green-600">78.3%</span>
                </div>
              </div>

              <div className="bg-sigma-50 p-4 rounded-lg">
                <h4 className="font-semibold text-sigma-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-sigma-700">
                  Quantum algorithms predict customer behavior with 78.3% win rate, 
                  increasing pipeline by 312% and reducing sales cycle by 45%.
                </p>
              </div>
            </div>

            {/* Case Study 3 */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center mb-4">
                <div className="w-12 h-12 bg-sigma-100 rounded-xl flex items-center justify-center mr-4">
                  <DollarSign className="w-6 h-6 text-sigma-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Lead Generation</h3>
                  <p className="text-sm text-gray-500">B2B Services</p>
                </div>
              </div>
              
              <div className="space-y-4 mb-6">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Lead Quality</span>
                  <span className="font-bold text-green-600">94.2%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Response Rate</span>
                  <span className="font-bold text-green-600">67.8%</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Revenue Generated</span>
                  <span className="font-bold text-green-600">$23.7M</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Cost per Lead</span>
                  <span className="font-bold text-green-600">-73%</span>
                </div>
              </div>

              <div className="bg-sigma-50 p-4 rounded-lg">
                <h4 className="font-semibold text-sigma-800 mb-2">Quantum Enhancement</h4>
                <p className="text-sm text-sigma-700">
                  AI-powered lead scoring achieves 94.2% quality with 67.8% response rate, 
                  generating $23.7M revenue while reducing cost per lead by 73%.
                </p>
              </div>
            </div>
          </div>

          {/* Sigma Metrics Summary */}
          <div className="bg-gradient-to-r from-sigma-50 to-sigma-100 rounded-2xl p-8">
            <h3 className="text-2xl font-bold text-sigma-800 mb-6 text-center">Sigma Select Impact Summary</h3>
            <div className="grid md:grid-cols-4 gap-6">
              <div className="text-center">
                <div className="text-3xl font-bold text-sigma-600 mb-2">24.7%</div>
                <div className="text-sm text-sigma-700">Average Conversion Rate</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-sigma-600 mb-2">1,247%</div>
                <div className="text-sm text-sigma-700">Average Revenue Growth</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-sigma-600 mb-2">78.3%</div>
                <div className="text-sm text-sigma-700">Win Rate</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-sigma-600 mb-2">2M+</div>
                <div className="text-sm text-sigma-700">Contacts Processed</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16 bg-gradient-to-br from-goliath-600 via-flyfox-600 to-sigma-600 text-white">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Experience Quantum-Powered Results?
          </h2>
          <p className="text-xl mb-8 opacity-90 max-w-3xl mx-auto">
            Join hundreds of companies already achieving unprecedented success with our quantum-enhanced solutions
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <Link href="/packages" className="btn-primary bg-white text-goliath-600 hover:bg-gray-100">
              View Packages
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
            <Link href="/contact" className="btn-secondary border-white text-white hover:bg-white hover:text-goliath-600">
              Schedule Demo
              <ArrowRight className="w-4 h-4 ml-2" />
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
