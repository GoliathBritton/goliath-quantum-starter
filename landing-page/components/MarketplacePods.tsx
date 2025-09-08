'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Store, Users, Settings, TrendingUp, Globe, Shield, Zap, Award, Building, UserCheck, DollarSign, BarChart3 } from 'lucide-react'
import { brand } from '@/lib/brand'

interface Pod {
  id: string
  name: string
  type: 'enterprise' | 'startup' | 'agency' | 'saas'
  status: 'active' | 'onboarding' | 'scaling'
  revenue: string
  growth: string
  employees: number
  advancedRoles: string[]
  services: string[]
  region: string
}

interface PartnerMetric {
  id: string
  name: string
  value: string
  change: string
  icon: any
  color: string
}

interface ScalingInitiative {
  id: string
  title: string
  description: string
  advancedRole: string
  impact: string
  timeline: string
  status: 'planning' | 'executing' | 'completed'
}

const marketplacePods: Pod[] = [
  {
    id: '1',
    name: 'TechFlow Solutions',
    type: 'enterprise',
    status: 'active',
    revenue: '$2.4M',
    growth: '+127%',
    employees: 45,
    advancedRoles: ['CMO', 'Operations Manager'],
    services: ['AI Consulting', 'Quantum Analytics', 'Digital Transformation'],
    region: 'North America'
  },
  {
    id: '2',
    name: 'Quantum Startups Hub',
    type: 'startup',
    status: 'scaling',
    revenue: '$890K',
    growth: '+234%',
    employees: 12,
    advancedRoles: ['HR Director', 'CMO'],
    services: ['MVP Development', 'Market Validation', 'Investor Readiness'],
    region: 'Europe'
  },
  {
    id: '3',
    name: 'Digital Agency Network',
    type: 'agency',
    status: 'active',
    revenue: '$1.8M',
    growth: '+89%',
    employees: 28,
    advancedRoles: ['CMO', 'Operations Manager', 'HR Director'],
    services: ['Brand Strategy', 'Performance Marketing', 'Creative Services'],
    region: 'Asia Pacific'
  },
  {
    id: '4',
    name: 'SaaS Accelerator',
    type: 'saas',
    status: 'onboarding',
    revenue: '$450K',
    growth: '+156%',
    employees: 8,
    advancedRoles: ['Operations Manager', 'HR Director'],
    services: ['Product Development', 'Go-to-Market', 'Customer Success'],
    region: 'Latin America'
  }
]

const partnerMetrics: PartnerMetric[] = [
  {
    id: '1',
    name: 'Active Partners',
    value: '247',
    change: '+34%',
    icon: Building,
    color: 'blue'
  },
  {
    id: '2',
    name: 'Total Revenue',
    value: '$12.8M',
    change: '+156%',
    icon: DollarSign,
    color: 'green'
  },
  {
    id: '3',
    name: 'Employee Growth',
    value: '1,247',
    change: '+89%',
    icon: Users,
    color: 'purple'
  },
  {
    id: '4',
    name: 'Market Reach',
    value: '67 Countries',
    change: '+23%',
    icon: Globe,
    color: 'orange'
  }
]

const scalingInitiatives: ScalingInitiative[] = [
  {
    id: '1',
    title: 'Global Brand Unification',
    description: 'Standardize brand guidelines and marketing strategies across all partner pods',
    advancedRole: 'CMO',
    impact: '+45% brand recognition',
    timeline: 'Q2 2024',
    status: 'executing'
  },
  {
    id: '2',
    title: 'Automated Onboarding Pipeline',
    description: 'Streamline partner onboarding with AI-powered process automation',
    advancedRole: 'Operations Manager',
    impact: '70% faster onboarding',
    timeline: 'Q1 2024',
    status: 'completed'
  },
  {
    id: '3',
    title: 'Talent Exchange Program',
    description: 'Cross-pod talent sharing and development program for skill optimization',
    advancedRole: 'HR Director',
    impact: '+60% employee satisfaction',
    timeline: 'Q3 2024',
    status: 'planning'
  },
  {
    id: '4',
    title: 'Revenue Sharing Optimization',
    description: 'AI-driven revenue allocation model based on performance metrics',
    advancedRole: 'Operations Manager',
    impact: '+32% partner profitability',
    timeline: 'Q2 2024',
    status: 'executing'
  }
]

export default function MarketplacePods() {
  const [selectedType, setSelectedType] = useState<string>('all')
  const [selectedStatus, setSelectedStatus] = useState<string>('all')

  const filteredPods = marketplacePods.filter(pod => {
    const typeMatch = selectedType === 'all' || pod.type === selectedType
    const statusMatch = selectedStatus === 'all' || pod.status === selectedStatus
    return typeMatch && statusMatch
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'bg-green-100 text-green-800'
      case 'scaling': return 'bg-blue-100 text-blue-800'
      case 'onboarding': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'enterprise': return Building
      case 'startup': return Zap
      case 'agency': return Award
      case 'saas': return Settings
      default: return Store
    }
  }

  const getInitiativeStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'executing': return 'bg-blue-100 text-blue-800'
      case 'planning': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="space-y-12">
      {/* Header */}
      <div className="text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-orange-100 to-red-100 px-4 py-2 rounded-full mb-6"
        >
          <Store className="w-5 h-5 text-orange-600" />
          <span className="text-orange-800 font-medium">Marketplace Pods</span>
        </motion.div>
        
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
          Partner Ecosystem Scaling
        </h2>
        
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          CMO, Operations Manager, and HR Director roles orchestrating global partner growth with quantum-enhanced scaling strategies.
        </p>
      </div>

      {/* Partner Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {partnerMetrics.map((metric, index) => {
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
                <div className={`p-3 bg-gradient-to-r from-${metric.color}-100 to-${metric.color}-200 rounded-lg`}>
                  <IconComponent className={`w-6 h-6 text-${metric.color}-600`} />
                </div>
                <div className="flex items-center gap-1 text-sm font-medium text-green-600">
                  <TrendingUp className="w-4 h-4" />
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

      {/* Active Pods */}
      <div>
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-2xl font-bold text-gray-900">Active Partner Pods</h3>
          
          <div className="flex gap-4">
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="enterprise">Enterprise</option>
              <option value="startup">Startup</option>
              <option value="agency">Agency</option>
              <option value="saas">SaaS</option>
            </select>
            
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="all">All Status</option>
              <option value="active">Active</option>
              <option value="scaling">Scaling</option>
              <option value="onboarding">Onboarding</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredPods.map((pod, index) => {
            const TypeIcon = getTypeIcon(pod.type)
            return (
              <motion.div
                key={pod.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-gradient-to-r from-orange-100 to-red-100 rounded-lg">
                      <TypeIcon className="w-5 h-5 text-orange-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{pod.name}</h4>
                      <p className="text-sm text-gray-600">{pod.region}</p>
                    </div>
                  </div>
                  
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(pod.status)}`}>
                    {pod.status}
                  </span>
                </div>
                
                <div className="grid grid-cols-3 gap-4 mb-4">
                  <div>
                    <div className="text-lg font-bold text-gray-900">{pod.revenue}</div>
                    <div className="text-xs text-gray-600">Revenue</div>
                  </div>
                  <div>
                    <div className="text-lg font-bold text-green-600">{pod.growth}</div>
                    <div className="text-xs text-gray-600">Growth</div>
                  </div>
                  <div>
                    <div className="text-lg font-bold text-blue-600">{pod.employees}</div>
                    <div className="text-xs text-gray-600">Employees</div>
                  </div>
                </div>
                
                <div className="mb-4">
                  <div className="text-sm font-medium text-gray-700 mb-2">Advanced Roles:</div>
                  <div className="flex flex-wrap gap-1">
                    {pod.advancedRoles.map((role, roleIndex) => (
                      <span
                        key={roleIndex}
                        className="px-2 py-1 bg-orange-100 text-orange-800 rounded text-xs font-medium"
                      >
                        {role}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div>
                  <div className="text-sm font-medium text-gray-700 mb-2">Services:</div>
                  <div className="flex flex-wrap gap-1">
                    {pod.services.map((service, serviceIndex) => (
                      <span
                        key={serviceIndex}
                        className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                      >
                        {service}
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Scaling Initiatives */}
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-8">Strategic Scaling Initiatives</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {scalingInitiatives.map((initiative, index) => (
            <motion.div
              key={initiative.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl p-6 shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300"
            >
              <div className="flex items-start justify-between mb-4">
                <h4 className="font-semibold text-gray-900 flex-1">{initiative.title}</h4>
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${getInitiativeStatusColor(initiative.status)}`}>
                  {initiative.status}
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">{initiative.description}</p>
              
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Led by:</span>
                  <span className="text-sm font-medium text-orange-600">{initiative.advancedRole}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Impact:</span>
                  <span className="text-sm font-medium text-green-600">{initiative.impact}</span>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-600">Timeline:</span>
                  <span className="text-sm font-medium text-blue-600">{initiative.timeline}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}