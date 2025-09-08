'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Bot, Code, Wrench, ClipboardList, Rocket,
  Play, Pause, Settings, TrendingUp, Users,
  Zap, CheckCircle, Clock, AlertCircle
} from 'lucide-react'
import { brand } from '@/lib/brand'

interface Agent {
  id: string
  name: string
  type: 'QDA' | 'QACA' | 'AIBA'
  status: 'active' | 'training' | 'optimizing' | 'deployed'
  performance: number
  advancedEnhancements: string[]
  createdBy: string
  lastOptimized: string
  capabilities: string[]
}

interface ProductionMetric {
  name: string
  value: number
  unit: string
  trend: 'up' | 'down' | 'stable'
  advancedRole: string
}

const agents: Agent[] = [
  {
    id: 'qda-001',
    name: 'Quantum Sales Navigator',
    type: 'QDA',
    status: 'active',
    performance: 94.7,
    advancedEnhancements: ['Optimized Logic', 'Multi-Modal Features', 'Agile Updates'],
    createdBy: 'Senior Programmer',
    lastOptimized: '2024-01-15T10:30:00Z',
    capabilities: ['Lead Qualification', 'Behavioral Analysis', 'Revenue Optimization']
  },
  {
    id: 'qaca-002',
    name: 'Quantum Voice Assistant',
    type: 'QACA',
    status: 'training',
    performance: 87.3,
    advancedEnhancements: ['Voice Integration', 'Digital Twin Presence', 'UX Optimization'],
    createdBy: 'Senior Product Engineer',
    lastOptimized: '2024-01-15T09:45:00Z',
    capabilities: ['Natural Language Processing', 'Emotional Intelligence', 'Call Optimization']
  },
  {
    id: 'aiba-003',
    name: 'Quantum Business Strategist',
    type: 'AIBA',
    status: 'deployed',
    performance: 91.2,
    advancedEnhancements: ['Growth Hacks', 'Market Intelligence', 'Entrepreneurial Logic'],
    createdBy: 'Senior Business Development',
    lastOptimized: '2024-01-15T08:20:00Z',
    capabilities: ['Market Analysis', 'Business Model Innovation', 'Strategic Planning']
  },
  {
    id: 'qda-004',
    name: 'Quantum Project Coordinator',
    type: 'QDA',
    status: 'optimizing',
    performance: 89.8,
    advancedEnhancements: ['Agile Delivery', 'Resource Optimization', 'KPI Tracking'],
    createdBy: 'Senior Project Manager',
    lastOptimized: '2024-01-15T11:15:00Z',
    capabilities: ['Task Automation', 'Team Coordination', 'Performance Monitoring']
  }
]

const productionMetrics: ProductionMetric[] = [
  {
    name: 'Agent Creation Rate',
    value: 12.4,
    unit: '/hour',
    trend: 'up',
    advancedRole: 'Programmer'
  },
  {
    name: 'Feature Integration Speed',
    value: 3.7,
    unit: 'min',
    trend: 'down',
    advancedRole: 'Product Engineer'
  },
  {
    name: 'Deployment Success Rate',
    value: 98.2,
    unit: '%',
    trend: 'stable',
    advancedRole: 'Project Manager'
  },
  {
    name: 'Business Model Innovation',
    value: 15,
    unit: 'models/week',
    trend: 'up',
    advancedRole: 'Dynamic Entrepreneur'
  }
]

const agentTypeColors = {
  'QDA': 'bg-brand-cyan/10 text-brand-cyan border-brand-cyan/30',
  'QACA': 'bg-brand-gold/10 text-brand-gold border-brand-gold/30',
  'AIBA': 'bg-quantum-purple/10 text-quantum-purple border-quantum-purple/30'
}

const statusColors = {
  'active': 'bg-green-100 text-green-700',
  'training': 'bg-blue-100 text-blue-700',
  'optimizing': 'bg-yellow-100 text-yellow-700',
  'deployed': 'bg-purple-100 text-purple-700'
}

const statusIcons = {
  'active': Play,
  'training': Settings,
  'optimizing': Wrench,
  'deployed': CheckCircle
}

export default function AgentFactory() {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)
  const [isProducing, setIsProducing] = useState(true)
  const [realTimeMetrics, setRealTimeMetrics] = useState(productionMetrics)

  // Simulate real-time production updates
  useEffect(() => {
    if (!isProducing) return

    const interval = setInterval(() => {
      setRealTimeMetrics(prev => prev.map(metric => ({
        ...metric,
        value: Math.max(0, metric.value + (Math.random() - 0.5) * 2)
      })))
    }, 3000)

    return () => clearInterval(interval)
  }, [isProducing])

  const agentFactoryRoles = brand.advancedRoles.filter(role => 
    ['Senior Programmer', 'Senior Product Engineer', 'Senior Project Manager', 'Senior Business Development'].includes(role.name)
  )

  return (
    <div className="bg-white">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="w-12 h-12 bg-brand-gold/10 rounded-xl flex items-center justify-center">
            <Bot className="w-6 h-6 text-brand-gold" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-black">Agent Factory</h2>
            <p className="text-gray-600">Advanced Enhanced Agent Production</p>
          </div>
          <div className="flex-1"></div>
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setIsProducing(!isProducing)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-all duration-300 ${
                isProducing 
                  ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                  : 'bg-green-100 text-green-700 hover:bg-green-200'
              }`}
            >
              {isProducing ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              <span>{isProducing ? 'Pause Production' : 'Start Production'}</span>
            </button>
            <div className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full ${isProducing ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
              <span className="text-sm text-gray-600">
                {isProducing ? 'Production Active' : 'Production Paused'}
              </span>
            </div>
          </div>
        </div>
        
        <p className="text-gray-600 mb-6">
          Advanced agent manufacturing enhanced with specialized capabilities for optimized logic, multi-modal features, and entrepreneurial intelligence.
        </p>
      </div>

      {/* Production Metrics */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-black mb-4">Real-time Production Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {realTimeMetrics.map((metric, index) => (
            <motion.div
              key={metric.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-brand-gold transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-black text-sm">{metric.name}</h4>
                <div className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">
                  {metric.advancedRole}
                </div>
              </div>
              
              <div className="flex items-end space-x-2 mb-2">
                <span className="text-2xl font-bold text-black">
                  {metric.value.toFixed(1)}
                </span>
                <span className="text-gray-500 text-sm">{metric.unit}</span>
                <div className="flex-1"></div>
                {metric.trend === 'up' && <TrendingUp className="w-4 h-4 text-green-500" />}
                {metric.trend === 'down' && <TrendingUp className="w-4 h-4 text-red-500 rotate-180" />}
                {metric.trend === 'stable' && <div className="w-4 h-4 bg-gray-400 rounded-full"></div>}
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div 
                  className="bg-brand-gold h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(metric.value * 2, 100)}%` }}
                  transition={{ duration: 1, delay: index * 0.1 }}
                ></motion.div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Active Agents */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-black mb-4">Active Agent Production Line</h3>
        <div className="grid gap-4">
          {agents.map((agent, index) => {
            const StatusIcon = statusIcons[agent.status]
            const isSelected = selectedAgent === agent.id
            
            return (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white border-2 border-gray-200 rounded-xl overflow-hidden hover:border-brand-cyan transition-all duration-300"
              >
                <div 
                  className="p-6 cursor-pointer"
                  onClick={() => setSelectedAgent(isSelected ? null : agent.id)}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center">
                        <Bot className="w-6 h-6 text-gray-600" />
                      </div>
                      <div>
                        <h4 className="text-lg font-bold text-black">{agent.name}</h4>
                        <div className="flex items-center space-x-2 mt-1">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${agentTypeColors[agent.type]}`}>
                            {agent.type}
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[agent.status]}`}>
                            <StatusIcon className="w-3 h-3 inline mr-1" />
                            {agent.status}
                          </span>
                          <span className="text-sm text-gray-500">
                            Performance: {agent.performance.toFixed(1)}%
                          </span>
                        </div>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-brand-cyan font-medium">{agent.createdBy}</div>
                      <div className="text-xs text-gray-500">
                        Last optimized: {new Date(agent.lastOptimized).toLocaleTimeString()}
                      </div>
                    </div>
                  </div>
                </div>

                <AnimatePresence>
                  {isSelected && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="border-t border-gray-200 bg-gray-50"
                    >
                      <div className="p-6">
                        <div className="grid md:grid-cols-2 gap-6">
                          <div>
                            <h5 className="font-semibold text-black mb-3">Advanced Enhancements</h5>
                            <ul className="space-y-2">
                              {agent.advancedEnhancements.map((enhancement, enhIndex) => (
                                <li key={enhIndex} className="flex items-center space-x-2">
                                  <Zap className="w-4 h-4 text-brand-gold" />
                                  <span className="text-sm text-gray-700">{enhancement}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                          
                          <div>
                            <h5 className="font-semibold text-black mb-3">Core Capabilities</h5>
                            <ul className="space-y-2">
                              {agent.capabilities.map((capability, capIndex) => (
                                <li key={capIndex} className="flex items-center space-x-2">
                                  <CheckCircle className="w-4 h-4 text-green-500" />
                                  <span className="text-sm text-gray-700">{capability}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                        </div>
                        
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <div className="flex items-center justify-between">
                            <div className="text-sm text-gray-600">
                              Agent ID: <code className="bg-gray-200 px-2 py-1 rounded text-xs">{agent.id}</code>
                            </div>
                            <div className="flex items-center space-x-4">
                              <button className="text-sm text-brand-cyan hover:text-brand-navy font-medium">
                                View Details
                              </button>
                              <button className="text-sm text-brand-gold hover:text-yellow-600 font-medium">
                                Optimize
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Advanced Roles Integration */}
        <div>
          <h3 className="text-xl font-bold text-black mb-4">Integrated Advanced Roles</h3>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {agentFactoryRoles.map((role, index) => (
            <motion.div
              key={role.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-brand-gold transition-all duration-300"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-brand-gold/10 rounded-lg flex items-center justify-center">
                  <span className="text-lg">{role.icon}</span>
                </div>
                <div>
                  <h4 className="font-bold text-black text-sm">{role.title}</h4>
                  <p className="text-xs text-brand-cyan">{role.brandEntity}</p>
                </div>
              </div>
              
              <p className="text-gray-600 text-sm mb-4">{role.description}</p>
              
              <div className="space-y-2">
                <h5 className="font-medium text-black text-xs">Key Impact:</h5>
                <ul className="space-y-1">
                  {role.capabilities.slice(0, 2).map((capability, capIndex) => (
                    <li key={capIndex} className="flex items-center space-x-2 text-xs text-gray-600">
                      <div className="w-1.5 h-1.5 bg-brand-gold rounded-full"></div>
                      <span>{capability}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  )
}