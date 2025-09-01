"use client"

import { useState, useEffect } from 'react'
import { Rocket, Users, Target, BarChart3, Zap, Brain, TrendingUp, Activity, Clock, Check } from 'lucide-react'

interface PodMetrics {
  callsMade: number
  emailsSent: number
  leads: number
  meetingsBooked: number
  conversionRate: number
  revenue: number
}

export default function SalesPodDashboard() {
  const [selectedAgents, setSelectedAgents] = useState(5)
  const [isDeployed, setIsDeployed] = useState(false)
  const [isDeploying, setIsDeploying] = useState(false)
  const [metrics, setMetrics] = useState<PodMetrics>({
    callsMade: 0,
    emailsSent: 0,
    leads: 0,
    meetingsBooked: 0,
    conversionRate: 0,
    revenue: 0
  })

  const agentOptions = [5, 10, 25, 50, 100, 500]

  const deployPod = async () => {
    setIsDeploying(true)
    
    // Simulate deployment process
    await new Promise(resolve => setTimeout(resolve, 3000))
    
    setIsDeployed(true)
    setIsDeploying(false)
    
    // Start live metrics simulation
    startMetricsSimulation()
  }

  const startMetricsSimulation = () => {
    const interval = setInterval(() => {
      setMetrics(prev => ({
        callsMade: prev.callsMade + Math.floor(Math.random() * 10) + 1,
        emailsSent: prev.emailsSent + Math.floor(Math.random() * 20) + 2,
        leads: prev.leads + Math.floor(Math.random() * 3),
        meetingsBooked: prev.meetingsBooked + Math.floor(Math.random() * 2),
        conversionRate: Math.min(25, prev.conversionRate + Math.random() * 0.5),
        revenue: prev.revenue + Math.floor(Math.random() * 500) + 100
      }))
    }, 2000)

    // Cleanup interval after 5 minutes
    setTimeout(() => clearInterval(interval), 300000)
  }

  const getPodSize = (agents: number) => {
    if (agents <= 10) return 'Starter Pod'
    if (agents <= 25) return 'Growth Pod'
    if (agents <= 100) return 'Scale Pod'
    if (agents <= 500) return 'Enterprise Pod'
    return 'Division Pod'
  }

  const getEstimatedROI = (agents: number) => {
    const baseROI = 800
    const agentMultiplier = Math.log10(agents + 1) * 100
    return Math.min(2000, baseROI + agentMultiplier)
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Deployment Section */}
      <div className="card mb-8">
        <div className="card-header bg-gradient-to-br from-goliath-600 to-flyfox-600 text-white">
          <h2 className="text-2xl font-bold">🚀 Deploy Your Quantum Sales Pod</h2>
          <p className="text-goliath-100">Launch autonomous sales agents powered by Dynex quantum computing</p>
        </div>
        <div className="card-content">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Agent Selection */}
            <div>
              <h3 className="text-lg font-semibold mb-4">Choose Your Pod Size</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
                {agentOptions.map((agents) => (
                  <button
                    key={agents}
                    onClick={() => setSelectedAgents(agents)}
                    className={`
                      p-4 rounded-lg border-2 transition-all duration-200 text-center
                      ${selectedAgents === agents 
                        ? 'border-goliath-500 bg-goliath-50 text-goliath-700' 
                        : 'border-gray-200 hover:border-gray-300'
                      }
                    `}
                  >
                    <div className="text-2xl font-bold">{agents}</div>
                    <div className="text-sm text-gray-600">Agents</div>
                    <div className="text-xs text-gray-500 mt-1">{getPodSize(agents)}</div>
                  </button>
                ))}
              </div>
              
              <div className="p-4 bg-gray-50 rounded-lg">
                <h4 className="font-semibold mb-2">Pod Configuration</h4>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span>Pod Type:</span>
                    <span className="font-medium">{getPodSize(selectedAgents)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Estimated ROI:</span>
                    <span className="font-medium text-goliath-600">{getEstimatedROI(selectedAgents)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Monthly Cost:</span>
                    <span className="font-medium">
                      ${selectedAgents <= 10 ? '2,500' : selectedAgents <= 25 ? '10,000' : selectedAgents <= 100 ? '35,000' : 'Custom'}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Deployment Action */}
            <div className="flex flex-col justify-center">
              <div className="text-center mb-6">
                <div className="w-24 h-24 bg-goliath-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Rocket className="w-12 h-12 text-goliath-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">Ready to Launch?</h3>
                <p className="text-gray-600">
                  Deploy {selectedAgents} autonomous sales agents that will work 24/7 
                  to generate leads and revenue for your business.
                </p>
              </div>
              
              <button
                onClick={deployPod}
                disabled={isDeploying || isDeployed}
                className="btn-primary text-lg px-8 py-4 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isDeploying ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Deploying Pod...
                  </div>
                ) : isDeployed ? (
                  <div className="flex items-center justify-center">
                    <Check className="w-6 h-6 mr-2" />
                    Pod Deployed!
                  </div>
                ) : (
                  <div className="flex items-center justify-center">
                    <Rocket className="w-6 h-6 mr-2" />
                    Deploy Now
                  </div>
                )}
              </button>
              
              {isDeployed && (
                <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <div className="flex items-center text-green-700">
                    <Check className="w-4 h-4 mr-2" />
                    <span className="text-sm font-medium">Pod successfully deployed!</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Live Dashboard */}
      {isDeployed && (
        <div className="card">
          <div className="card-header bg-gradient-to-br from-sigma-500 to-sigma-600 text-white">
            <h2 className="text-2xl font-bold">📊 Live Performance Dashboard</h2>
            <p className="text-sigma-100">Real-time metrics from your autonomous sales agents</p>
          </div>
          <div className="card-content">
            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              <div className="p-6 bg-gradient-to-br from-goliath-50 to-goliath-100 rounded-xl border border-goliath-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="w-12 h-12 bg-goliath-100 rounded-lg flex items-center justify-center">
                    <Users className="w-6 h-6 text-goliath-600" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-goliath-600" />
                </div>
                <div className="text-2xl font-bold text-goliath-700">{metrics.callsMade}</div>
                <div className="text-sm text-goliath-600">Calls Made</div>
                <div className="text-xs text-goliath-500 mt-1">Last 24 hours</div>
              </div>
              
              <div className="p-6 bg-gradient-to-br from-flyfox-50 to-flyfox-100 rounded-xl border border-flyfox-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="w-12 h-12 bg-flyfox-100 rounded-lg flex items-center justify-center">
                    <Target className="w-6 h-6 text-flyfox-600" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-flyfox-600" />
                </div>
                <div className="text-2xl font-bold text-flyfox-700">{metrics.leads}</div>
                <div className="text-sm text-flyfox-600">Leads Generated</div>
                <div className="text-xs text-flyfox-500 mt-1">Qualified prospects</div>
              </div>
              
              <div className="p-6 bg-gradient-to-br from-sigma-50 to-sigma-100 rounded-xl border border-sigma-200">
                <div className="flex items-center justify-between mb-2">
                  <div className="w-12 h-12 bg-sigma-100 rounded-lg flex items-center justify-center">
                    <BarChart3 className="w-6 h-6 text-sigma-600" />
                  </div>
                  <TrendingUp className="w-5 h-5 text-sigma-600" />
                </div>
                <div className="text-2xl font-bold text-sigma-700">{metrics.conversionRate.toFixed(1)}%</div>
                <div className="text-sm text-sigma-600">Conversion Rate</div>
                <div className="text-xs text-sigma-500 mt-1">Industry avg: 2-5%</div>
              </div>
            </div>

            {/* Additional Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <div className="p-4 bg-gray-50 rounded-lg text-center">
                <div className="text-lg font-bold text-gray-700">{metrics.emailsSent}</div>
                <div className="text-sm text-gray-600">Emails Sent</div>
              </div>
              
              <div className="p-4 bg-gray-50 rounded-lg text-center">
                <div className="text-lg font-bold text-gray-700">{metrics.meetingsBooked}</div>
                <div className="text-sm text-gray-600">Meetings Booked</div>
              </div>
              
              <div className="p-4 bg-gray-50 rounded-lg text-center">
                <div className="text-lg font-bold text-gray-700">${metrics.revenue.toLocaleString()}</div>
                <div className="text-sm text-gray-600">Revenue Generated</div>
              </div>
              
              <div className="p-4 bg-gray-50 rounded-lg text-center">
                <div className="text-lg font-bold text-gray-700">24/7</div>
                <div className="text-sm text-gray-600">Agent Availability</div>
              </div>
            </div>

            {/* Agent Health Status */}
            <div className="p-6 bg-gray-50 rounded-lg">
              <h3 className="text-lg font-semibold mb-4">Agent Health Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div className="flex items-center p-3 bg-white rounded-lg">
                  <div className="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium">Learning & Improving</span>
                </div>
                
                <div className="flex items-center p-3 bg-white rounded-lg">
                  <div className="w-3 h-3 bg-blue-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium">Campaign Active</span>
                </div>
                
                <div className="flex items-center p-3 bg-white rounded-lg">
                  <div className="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium">Performance Review</span>
                </div>
              </div>
            </div>

            {/* Quantum Computing Status */}
            <div className="mt-6 p-4 bg-gradient-to-r from-goliath-50 to-flyfox-50 rounded-lg border border-goliath-200">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Brain className="w-6 h-6 text-goliath-600" />
                  <div>
                    <div className="font-semibold text-goliath-700">Dynex Quantum Computing</div>
                    <div className="text-sm text-goliath-600">410x performance boost active</div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                  <span className="text-sm text-goliath-600">Active</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Next Steps */}
      {isDeployed && (
        <div className="mt-8 text-center">
          <h3 className="text-xl font-bold text-gray-900 mb-4">
            Your Quantum Sales Pod is Live! 🎉
          </h3>
          <p className="text-lg text-gray-600 mb-6">
            Your autonomous sales agents are now working 24/7 to generate leads and revenue. 
            Monitor their performance and scale up as needed.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="btn-primary">
              View Detailed Analytics
            </button>
            <button className="btn-secondary">
              Scale Up Pod
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
