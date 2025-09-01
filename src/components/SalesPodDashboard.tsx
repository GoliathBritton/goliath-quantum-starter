"use client"

import { useState } from 'react'
import { 
  Rocket, 
  Users, 
  Target, 
  BarChart3, 
  Zap, 
  Brain, 
  Crown, 
  TrendingUp,
  Play,
  Pause,
  Settings,
  Eye,
  MessageSquare,
  Phone,
  Mail,
  Globe,
  Activity,
  CheckCircle,
  Clock,
  AlertCircle,
  X
} from 'lucide-react'

interface SalesPod {
  id: string
  name: string
  status: 'active' | 'paused' | 'deploying' | 'error'
  agentCount: number
  contacts: number
  channels: string[]
  performance: {
    conversionRate: number
    roi: number
    revenue: number
    calls: number
    emails: number
    responses: number
  }
  lastActivity: string
  health: 'excellent' | 'good' | 'warning' | 'critical'
}

interface PodMetrics {
  totalPods: number
  activeAgents: number
  totalContacts: number
  totalRevenue: number
  avgConversionRate: number
  avgROI: number
}

export default function SalesPodDashboard() {
  const [selectedPod, setSelectedPod] = useState<string | null>(null)
  const [isDeploying, setIsDeploying] = useState(false)
  const [deploymentProgress, setDeploymentProgress] = useState(0)

  const mockPods: SalesPod[] = [
    {
      id: 'pod-1',
      name: 'Enterprise Outreach Pod',
      status: 'active',
      agentCount: 25,
      contacts: 5000,
      channels: ['email', 'voice', 'social'],
      performance: {
        conversionRate: 18.5,
        roi: 1250,
        revenue: 125000,
        calls: 1250,
        emails: 3750,
        responses: 925
      },
      lastActivity: '2 minutes ago',
      health: 'excellent'
    },
    {
      id: 'pod-2',
      name: 'SMB Growth Pod',
      status: 'active',
      agentCount: 10,
      contacts: 2000,
      channels: ['email', 'sms'],
      performance: {
        conversionRate: 12.3,
        roi: 890,
        revenue: 44500,
        calls: 0,
        emails: 2000,
        responses: 246
      },
      lastActivity: '5 minutes ago',
      health: 'good'
    },
    {
      id: 'pod-3',
      name: 'Startup Accelerator Pod',
      status: 'deploying',
      agentCount: 5,
      contacts: 1000,
      channels: ['email', 'social'],
      performance: {
        conversionRate: 0,
        roi: 0,
        revenue: 0,
        calls: 0,
        emails: 0,
        responses: 0
      },
      lastActivity: 'Deploying...',
      health: 'warning'
    }
  ]

  const metrics: PodMetrics = {
    totalPods: mockPods.length,
    activeAgents: mockPods.filter(pod => pod.status === 'active').reduce((sum, pod) => sum + pod.agentCount, 0),
    totalContacts: mockPods.reduce((sum, pod) => sum + pod.contacts, 0),
    totalRevenue: mockPods.reduce((sum, pod) => sum + pod.performance.revenue, 0),
    avgConversionRate: mockPods.filter(pod => pod.status === 'active').reduce((sum, pod) => sum + pod.performance.conversionRate, 0) / mockPods.filter(pod => pod.status === 'active').length,
    avgROI: mockPods.filter(pod => pod.status === 'active').reduce((sum, pod) => sum + pod.performance.roi, 0) / mockPods.filter(pod => pod.status === 'active').length
  }

  const handleDeployPod = async () => {
    setIsDeploying(true)
    setDeploymentProgress(0)

    const interval = setInterval(() => {
      setDeploymentProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          return 100
        }
        return prev + 10
      })
    }, 300)

    // Simulate deployment
    setTimeout(() => {
      setIsDeploying(false)
      setDeploymentProgress(100)
      // Add new pod to list
    }, 3000)
  }

  const handlePodAction = (podId: string, action: 'play' | 'pause' | 'settings') => {
    console.log(`${action} action for pod ${podId}`)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100'
      case 'paused': return 'text-yellow-600 bg-yellow-100'
      case 'deploying': return 'text-blue-600 bg-blue-100'
      case 'error': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  const getHealthColor = (health: string) => {
    switch (health) {
      case 'excellent': return 'text-green-600'
      case 'good': return 'text-blue-600'
      case 'warning': return 'text-yellow-600'
      case 'critical': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  const getChannelIcon = (channel: string) => {
    switch (channel) {
      case 'email': return <Mail className="w-4 h-4" />
      case 'voice': return <Phone className="w-4 h-4" />
      case 'sms': return <MessageSquare className="w-4 h-4" />
      case 'social': return <Globe className="w-4 h-4" />
      default: return <MessageSquare className="w-4 h-4" />
    }
  }

  return (
    <div className="space-y-8">
      {/* Metrics Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="card-content text-center">
            <div className="w-12 h-12 bg-goliath-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Rocket className="w-6 h-6 text-goliath-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">{metrics.totalPods}</div>
            <div className="text-sm text-gray-600">Active Pods</div>
          </div>
        </div>

        <div className="card">
          <div className="card-content text-center">
            <div className="w-12 h-12 bg-flyfox-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Users className="w-6 h-6 text-flyfox-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">{metrics.activeAgents}</div>
            <div className="text-sm text-gray-600">Active Agents</div>
          </div>
        </div>

        <div className="card">
          <div className="card-content text-center">
            <div className="w-12 h-12 bg-sigma-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Target className="w-6 h-6 text-sigma-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">{metrics.totalContacts.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Total Contacts</div>
          </div>
        </div>

        <div className="card">
          <div className="card-content text-center">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <TrendingUp className="w-6 h-6 text-green-600" />
            </div>
            <div className="text-2xl font-bold text-gray-900 mb-1">${metrics.totalRevenue.toLocaleString()}</div>
            <div className="text-sm text-gray-600">Total Revenue</div>
          </div>
        </div>
      </div>

      {/* Performance Summary */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Performance Overview</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Average Conversion Rate</span>
                <span className="text-lg font-semibold text-goliath-600">{metrics.avgConversionRate.toFixed(1)}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Average ROI</span>
                <span className="text-lg font-semibold text-flyfox-600">{metrics.avgROI.toFixed(0)}%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Total Responses</span>
                <span className="text-lg font-semibold text-sigma-600">
                  {mockPods.reduce((sum, pod) => sum + pod.performance.responses, 0).toLocaleString()}
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="text-lg font-semibold text-gray-900">Quantum Computing Status</h3>
          </div>
          <div className="card-content">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Dynex Status</span>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm font-medium text-green-600">Active</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">Performance Boost</span>
                <span className="text-sm font-semibold text-flyfox-600">410x</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">NVIDIA Acceleration</span>
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span className="text-sm font-medium text-green-600">Enabled</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Pod Management */}
      <div className="card">
        <div className="card-header flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">Sales Pods</h3>
          <button
            onClick={handleDeployPod}
            disabled={isDeploying}
            className="btn-primary"
          >
            {isDeploying ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                Deploying...
              </div>
            ) : (
              <>
                Deploy New Pod
                <Rocket className="ml-2 w-5 h-5" />
              </>
            )}
          </button>
        </div>

        {isDeploying && (
          <div className="px-6 py-4 border-b border-gray-100">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <Rocket className="w-5 h-5 text-blue-600" />
              </div>
              <div className="flex-1">
                <div className="text-sm font-medium text-gray-900">Deploying New Sales Pod...</div>
                <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${deploymentProgress}%` }}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="card-content">
          <div className="space-y-4">
            {mockPods.map((pod) => (
              <div
                key={pod.id}
                className={`p-4 border rounded-lg transition-all cursor-pointer ${
                  selectedPod === pod.id 
                    ? 'border-goliath-500 bg-goliath-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
                onClick={() => setSelectedPod(pod.id)}
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-goliath-100 rounded-lg flex items-center justify-center">
                      <Rocket className="w-5 h-5 text-goliath-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{pod.name}</h4>
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(pod.status)}`}>
                          {pod.status.charAt(0).toUpperCase() + pod.status.slice(1)}
                        </span>
                        <span className={`text-xs ${getHealthColor(pod.health)}`}>
                          {pod.health.charAt(0).toUpperCase() + pod.health.slice(1)} Health
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handlePodAction(pod.id, pod.status === 'active' ? 'pause' : 'play')
                      }}
                      className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      {pod.status === 'active' ? (
                        <Pause className="w-4 h-4" />
                      ) : (
                        <Play className="w-4 h-4" />
                      )}
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handlePodAction(pod.id, 'settings')
                      }}
                      className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      <Settings className="w-4 h-4" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        setSelectedPod(pod.id)
                      }}
                      className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div className="text-center">
                    <div className="text-lg font-semibold text-gray-900">{pod.agentCount}</div>
                    <div className="text-xs text-gray-500">Agents</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold text-gray-900">{pod.contacts.toLocaleString()}</div>
                    <div className="text-xs text-gray-500">Contacts</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold text-gray-900">{pod.performance.conversionRate}%</div>
                    <div className="text-xs text-gray-500">Conversion</div>
                  </div>
                  <div className="text-center">
                    <div className="text-lg font-semibold text-gray-900">${pod.performance.revenue.toLocaleString()}</div>
                    <div className="text-xs text-gray-500">Revenue</div>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    {pod.channels.map((channel) => (
                      <div key={channel} className="w-6 h-6 bg-gray-100 rounded flex items-center justify-center">
                        {getChannelIcon(channel)}
                      </div>
                    ))}
                  </div>
                  <div className="text-xs text-gray-500 flex items-center">
                    <Activity className="w-3 h-3 mr-1" />
                    {pod.lastActivity}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Pod Details Sidebar */}
      {selectedPod && (
        <div className="fixed inset-y-0 right-0 w-96 bg-white border-l border-gray-200 shadow-xl z-50 overflow-y-auto">
          <div className="p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">Pod Details</h3>
              <button
                onClick={() => setSelectedPod(null)}
                className="p-2 text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {(() => {
              const pod = mockPods.find(p => p.id === selectedPod)
              if (!pod) return null

              return (
                <div className="space-y-6">
                  <div className="text-center">
                    <div className="w-16 h-16 bg-goliath-100 rounded-full flex items-center justify-center mx-auto mb-4">
                      <Rocket className="w-8 h-8 text-goliath-600" />
                    </div>
                    <h4 className="text-xl font-bold text-gray-900 mb-2">{pod.name}</h4>
                    <div className="flex items-center justify-center space-x-2">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(pod.status)}`}>
                        {pod.status.charAt(0).toUpperCase() + pod.status.slice(1)}
                      </span>
                      <span className={`text-sm ${getHealthColor(pod.health)}`}>
                        {pod.health.charAt(0).toUpperCase() + pod.health.slice(1)} Health
                      </span>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center p-3 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-goliath-600">{pod.agentCount}</div>
                        <div className="text-sm text-gray-600">Active Agents</div>
                      </div>
                      <div className="text-center p-3 bg-gray-50 rounded-lg">
                        <div className="text-2xl font-bold text-flyfox-600">{pod.contacts.toLocaleString()}</div>
                        <div className="text-sm text-gray-600">Contacts</div>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h5 className="font-semibold text-gray-900">Performance Metrics</h5>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Conversion Rate</span>
                          <span className="text-sm font-medium text-gray-900">{pod.performance.conversionRate}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">ROI</span>
                          <span className="text-sm font-medium text-gray-900">{pod.performance.roi}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Revenue</span>
                          <span className="text-sm font-medium text-gray-900">${pod.performance.revenue.toLocaleString()}</span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h5 className="font-semibold text-gray-900">Activity</h5>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Calls Made</span>
                          <span className="text-sm font-medium text-gray-900">{pod.performance.calls}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Emails Sent</span>
                          <span className="text-sm font-medium text-gray-900">{pod.performance.emails}</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-sm text-gray-600">Responses</span>
                          <span className="text-sm font-medium text-gray-900">{pod.performance.responses}</span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h5 className="font-semibold text-gray-900">Channels</h5>
                      <div className="flex flex-wrap gap-2">
                        {pod.channels.map((channel) => (
                          <div key={channel} className="flex items-center space-x-2 px-3 py-2 bg-gray-100 rounded-lg">
                            {getChannelIcon(channel)}
                            <span className="text-sm text-gray-700 capitalize">{channel}</span>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="pt-4 border-t border-gray-200">
                      <button className="w-full btn-primary">
                        View Full Analytics
                        <BarChart3 className="ml-2 w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              )
            })()}
          </div>
        </div>
      )}
    </div>
  )
}
