'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { TrendingUp, Target, Users, DollarSign, Zap, Brain, BarChart3, Filter, ArrowUpRight, Sparkles } from 'lucide-react'
import { brand } from '@/lib/brand'

interface SalesMetric {
  id: string
  name: string
  value: string
  change: string
  trend: 'up' | 'down' | 'stable'
  icon: any
}

interface GrowthHack {
  id: string
  name: string
  type: 'funnel' | 'conversion' | 'retention' | 'acquisition'
  description: string
  impact: string
  status: 'active' | 'testing' | 'planned'
  advancedRole: string
}

interface FunnelStage {
  id: string
  name: string
  conversion: number
  volume: number
  optimizations: string[]
}

const salesMetrics: SalesMetric[] = [
  {
    id: '1',
    name: 'Quantum Lead Score',
    value: '94.7%',
    change: '+12.3%',
    trend: 'up',
    icon: Target
  },
  {
    id: '2',
    name: 'Funnel Velocity',
    value: '2.4x',
    change: '+45%',
    trend: 'up',
    icon: TrendingUp
  },
  {
    id: '3',
    name: 'Conversion Rate',
    value: '31.2%',
    change: '+8.7%',
    trend: 'up',
    icon: BarChart3
  },
  {
    id: '4',
    name: 'Revenue Per Lead',
    value: '$4,890',
    change: '+23.1%',
    trend: 'up',
    icon: DollarSign
  }
]

const growthHacks: GrowthHack[] = [
  {
    id: '1',
    name: 'Quantum Behavioral Triggers',
    type: 'conversion',
    description: 'AI-powered psychological triggers based on user behavior patterns',
    impact: '+47% conversion rate',
    status: 'active',
    advancedRole: 'Market Strategist'
  },
  {
    id: '2',
    name: 'Predictive Lead Scoring',
    type: 'acquisition',
    description: 'Machine learning models predict lead quality in real-time',
    impact: '+62% qualified leads',
    status: 'active',
    advancedRole: 'Lead Generation'
  },
  {
    id: '3',
    name: 'Dynamic Pricing Engine',
    type: 'conversion',
    description: 'Quantum algorithms adjust pricing based on market conditions',
    impact: '+34% revenue per sale',
    status: 'testing',
    advancedRole: 'Market Strategist'
  },
  {
    id: '4',
    name: 'Viral Coefficient Optimizer',
    type: 'acquisition',
    description: 'AI identifies and amplifies viral growth opportunities',
    impact: '+89% organic referrals',
    status: 'planned',
    advancedRole: 'Lead Generation'
  }
]

const funnelStages: FunnelStage[] = [
  {
    id: '1',
    name: 'Awareness',
    conversion: 100,
    volume: 10000,
    optimizations: ['Quantum SEO', 'AI Content Generation', 'Predictive Targeting']
  },
  {
    id: '2',
    name: 'Interest',
    conversion: 23.4,
    volume: 2340,
    optimizations: ['Behavioral Triggers', 'Dynamic Content', 'Personalization Engine']
  },
  {
    id: '3',
    name: 'Consideration',
    conversion: 45.7,
    volume: 1069,
    optimizations: ['Social Proof AI', 'Risk Reversal', 'Quantum Testimonials']
  },
  {
    id: '4',
    name: 'Purchase',
    conversion: 31.2,
    volume: 334,
    optimizations: ['Friction Reduction', 'Payment Optimization', 'Trust Signals']
  },
  {
    id: '5',
    name: 'Advocacy',
    conversion: 67.8,
    volume: 226,
    optimizations: ['Referral Engine', 'Loyalty Programs', 'Community Building']
  }
]

export default function QSalesDivision() {
  const [selectedType, setSelectedType] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')

  const filteredHacks = growthHacks.filter(hack => {
    const typeMatch = selectedType === 'all' || hack.type === selectedType
    const statusMatch = selectedStatus === 'all' || hack.status === selectedStatus
    return typeMatch && statusMatch
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'testing': return 'bg-yellow-100 text-yellow-800'
      case 'planned': return 'bg-blue-100 text-blue-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'funnel': return TrendingUp
      case 'conversion': return Target
      case 'retention': return Users
      case 'acquisition': return Zap
      default: return Brain
    }
  }

  return (
    <div className="space-y-12">
      {/* Header */}
      <div className="text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-purple-100 to-blue-100 px-4 py-2 rounded-full mb-6"
        >
          <TrendingUp className="w-5 h-5 text-purple-600" />
          <span className="text-purple-800 font-medium">Q-Sales Division™</span>
        </motion.div>
        
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
          Quantum Growth Intelligence
        </h2>
        
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Market Strategist and Lead Generation roles embedded with quantum algorithms for exponential growth hacks and funnel optimization.
        </p>
      </div>

      {/* Sales Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {salesMetrics.map((metric, index) => {
          const IconComponent = metric.icon
          return (
            <motion.div
              key={metric.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-gradient-to-r from-purple-100 to-blue-100 rounded-lg">
                  <IconComponent className="w-6 h-6 text-purple-600" />
                </div>
                <div className={`flex items-center gap-1 text-sm font-medium ${
                  metric.trend === 'up' ? 'text-green-600' : 'text-red-600'
                }`}>
                  <ArrowUpRight className="w-4 h-4" />
                  {metric.change}
                </div>
              </div>
              
              <div className="text-2xl font-bold text-gray-900 mb-1">
                {metric.value}
              </div>
              
              <div className="text-sm text-gray-600">
                {metric.name}
              </div>
            </motion.div>
          )
        })}
      </div>

      {/* Growth Hacks */}
      <div>
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-2xl font-bold text-gray-900">Active Growth Hacks</h3>
          
          <div className="flex gap-4">
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="funnel">Funnel</option>
              <option value="conversion">Conversion</option>
              <option value="retention">Retention</option>
              <option value="acquisition">Acquisition</option>
            </select>
            
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="testing">Testing</option>
              <option value="planned">Planned</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredHacks.map((hack, index) => {
            const TypeIcon = getTypeIcon(hack.type)
            return (
              <motion.div
                key={hack.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-gradient-to-r from-purple-100 to-blue-100 rounded-lg">
                      <TypeIcon className="w-5 h-5 text-purple-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{hack.name}</h4>
                      <p className="text-sm text-gray-600 capitalize">{hack.type}</p>
                    </div>
                  </div>
                  
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(hack.status)}`}>
                    {hack.status}
                  </span>
                </div>
                
                <p className="text-gray-600 mb-4">{hack.description}</p>
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4 text-purple-600" />
                    <span className="text-sm font-medium text-purple-600">{hack.impact}</span>
                  </div>
                  
                  <div className="text-xs text-gray-500">
                    {hack.advancedRole}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Quantum Funnel Visualization */}
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Quantum Sales Funnel</h3>
        
        <div className="space-y-4">
          {funnelStages.map((stage, index) => {
            const width = (stage.conversion / 100) * 100
            return (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl p-6 shadow-lg border border-gray-100"
              >
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h4 className="font-semibold text-gray-900">{stage.name}</h4>
                    <p className="text-sm text-gray-600">{stage.volume.toLocaleString()} visitors</p>
                  </div>
                  
                  <div className="text-right">
                    <div className="text-2xl font-bold text-purple-600">{stage.conversion}%</div>
                    <div className="text-sm text-gray-600">conversion</div>
                  </div>
                </div>
                
                <div className="mb-4">
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${width}%` }}
                      transition={{ delay: index * 0.2, duration: 1 }}
                      className="bg-gradient-to-r from-purple-500 to-blue-500 h-3 rounded-full"
                    />
                  </div>
                </div>
                
                <div className="flex flex-wrap gap-2">
                  {stage.optimizations.map((optimization, optIndex) => (
                    <span
                      key={optIndex}
                      className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-xs font-medium"
                    >
                      {optimization}
                    </span>
                  ))}
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </div>
  )
}