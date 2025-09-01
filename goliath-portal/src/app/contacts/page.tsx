import ContactWizard from '@/components/ContactWizard'
import { Upload, Database, Zap, Target, Users, BarChart3 } from 'lucide-react'

export default function ContactsPage() {
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
            Contact Import &{' '}
            <span className="text-gradient">Campaign Setup</span>
          </h1>
          
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Import your contacts, enrich them with quantum AI, and launch automated 
            campaigns that generate leads 24/7.
          </p>
        </div>

        {/* Contact Wizard */}
        <ContactWizard />

        {/* Features Section */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
            Why Choose Our Contact Management?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <div className="card text-center">
              <div className="w-16 h-16 bg-goliath-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Upload className="w-8 h-8 text-goliath-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Easy Import</h3>
              <p className="text-gray-600">
                Import from CSV, HubSpot, Salesforce, or connect via API. 
                We handle the heavy lifting.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Database className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Enrichment</h3>
              <p className="text-gray-600">
                Quantum AI automatically fills missing data, scores contacts, 
                and identifies decision makers.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-sigma-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Target className="w-8 h-8 text-sigma-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Smart Scoring</h3>
              <p className="text-gray-600">
                AI-powered scoring identifies hot leads, warm prospects, 
                and cold contacts for optimal targeting.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-goliath-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Users className="w-8 h-8 text-goliath-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Campaign Automation</h3>
              <p className="text-gray-600">
                Launch multi-channel campaigns across email, SMS, voice, 
                and digital humans automatically.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-flyfox-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <BarChart3 className="w-8 h-8 text-flyfox-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Real-time Analytics</h3>
              <p className="text-gray-600">
                Track campaign performance, conversion rates, and ROI 
                in real-time dashboards.
              </p>
            </div>
            
            <div className="card text-center">
              <div className="w-16 h-16 bg-sigma-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Zap className="w-8 h-8 text-sigma-600" />
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Quantum Optimization</h3>
              <p className="text-gray-600">
                Dynex quantum computing continuously optimizes campaigns 
                for maximum performance and ROI.
              </p>
            </div>
          </div>
        </div>

        {/* CSV Format Guide */}
        <div className="mt-20">
          <div className="card max-w-4xl mx-auto">
            <div className="card-header bg-gradient-to-br from-goliath-600 to-flyfox-600 text-white">
              <h3 className="text-2xl font-bold">CSV Format Guide</h3>
              <p className="text-goliath-100">Prepare your contacts for optimal import</p>
            </div>
            <div className="card-content">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-gray-200">
                      <th className="text-left py-2 font-semibold">Field</th>
                      <th className="text-left py-2 font-semibold">Required</th>
                      <th className="text-left py-2 font-semibold">Description</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">company_name</td>
                      <td className="py-2">Yes</td>
                      <td className="py-2">Company or organization name</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">contact_name</td>
                      <td className="py-2">Yes</td>
                      <td className="py-2">Full name of the contact</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">title</td>
                      <td className="py-2">No</td>
                      <td className="py-2">Job title or position</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">phone</td>
                      <td className="py-2">No</td>
                      <td className="py-2">Phone number</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">email</td>
                      <td className="py-2">Yes</td>
                      <td className="py-2">Email address</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">industry</td>
                      <td className="py-2">No</td>
                      <td className="py-2">Industry or sector</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">company_size</td>
                      <td className="py-2">No</td>
                      <td className="py-2">Number of employees</td>
                    </tr>
                    <tr>
                      <td className="py-2 font-mono text-goliath-600">annual_revenue</td>
                      <td className="py-2">No</td>
                      <td className="py-2">Annual revenue range</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-xl">
                <p className="text-sm text-gray-600">
                  <strong>Tip:</strong> The more data you provide, the better our quantum AI can 
                  enrich and score your contacts. Missing fields will be automatically filled 
                  using our AI enrichment system.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center">
          <h3 className="text-2xl font-bold text-gray-900 mb-4">
            Ready to Import Your Contacts?
          </h3>
          <p className="text-lg text-gray-600 mb-8">
            Start building your quantum-powered sales campaigns today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/pods" className="btn-primary">
              Deploy Sales Pods
            </a>
            <a href="/packages" className="btn-secondary">
              View Packages
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}
