'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Atom, Zap, ArrowRightLeft, Brain, Network, Layers, Sparkles, ChevronDown, ChevronUp } from 'lucide-react'
import { brand } from '@/lib/brand'

interface QuantumPrinciple {
  id: string
  name: string
  description: string
  icon: any
  color: string
  applications: QuantumApplication[]
}

interface QuantumApplication {
  id: string
  advancedRole: string
  implementation: string
  benefit: string
  example: string
}

interface RoleQuantumMapping {
  id: string
  role: string
  brandEntity: string
  layer: string
  quantumPrinciples: {
    superposition: string
    entanglement: string
    tunneling: string
  }
  quantumScore: number
}

const quantumPrinciples: QuantumPrinciple[] = [
  {
    id: 'superposition',
    name: 'Superposition',
    description: 'Multiple states existing simultaneously until observation collapses to optimal solution',
    icon: Layers,
    color: 'blue',
    applications: [
      {
        id: '1',
        advancedRole: 'Project Manager',
        implementation: 'Parallel scenario planning across multiple project timelines',
        benefit: 'Risk mitigation through quantum scenario modeling',
        example: 'Evaluating 16 different project paths simultaneously'
      },
      {
        id: '2',
        advancedRole: 'CFO',
        implementation: 'Quantum financial modeling with multiple market conditions',
        benefit: 'Optimal resource allocation across uncertain futures',
        example: 'Budget optimization across 32 economic scenarios'
      },
      {
        id: '3',
        advancedRole: 'Market Strategist',
        implementation: 'Multi-dimensional market positioning strategies',
        benefit: 'Adaptive positioning based on market quantum states',
        example: 'Brand positioning across infinite market configurations'
      }
    ]
  },
  {
    id: 'entanglement',
    name: 'Entanglement',
    description: 'Instantaneous correlation between distributed system components',
    icon: Network,
    color: 'purple',
    applications: [
      {
        id: '1',
        advancedRole: 'HR Director',
        implementation: 'Quantum team synchronization across global offices',
        benefit: 'Instant cultural alignment and knowledge transfer',
        example: 'Real-time skill sharing between 247 partner locations'
      },
      {
        id: '2',
        advancedRole: 'Human Psychology Insight',
        implementation: 'Entangled behavioral pattern recognition',
        benefit: 'Collective intelligence from distributed insights',
        example: 'Synchronized emotional intelligence across all agents'
      },
      {
        id: '3',
        advancedRole: 'CTO',
        implementation: 'Quantum-entangled microservices architecture',
        benefit: 'Instantaneous system-wide optimization',
        example: 'Zero-latency coordination between 1000+ services'
      }
    ]
  },
  {
    id: 'tunneling',
    name: 'Tunneling',
    description: 'Breaking through classical barriers to achieve impossible outcomes',
    icon: Zap,
    color: 'orange',
    applications: [
      {
        id: '1',
        advancedRole: 'Product Engineer',
        implementation: 'Quantum breakthrough innovation methodology',
        benefit: 'Transcending traditional technical limitations',
        example: 'Creating products that defy industry constraints'
      },
      {
        id: '2',
        advancedRole: 'Dynamic Entrepreneur',
        implementation: 'Market barrier penetration strategies',
        benefit: 'Entering impossible markets through quantum approaches',
        example: 'Disrupting 5 industries simultaneously'
      },
      {
        id: '3',
        advancedRole: 'Operations Manager',
        implementation: 'Quantum efficiency optimization',
        benefit: 'Achieving impossible operational metrics',
        example: '99.99% efficiency with zero resource waste'
      }
    ]
  }
]

const roleQuantumMappings: RoleQuantumMapping[] = [
  {
    id: '1',
    role: 'Chief Technology Officer',
    brandEntity: 'FLYFOX AI',
    layer: 'NQBA Orchestrator',
    quantumPrinciples: {
      superposition: 'Multi-tech roadmap scenarios',
      entanglement: 'Synchronized architecture decisions',
      tunneling: 'Breaking technical impossibilities'
    },
    quantumScore: 98
  },
  {
    id: '2',
    role: 'Senior Data Scientist',
    brandEntity: 'FLYFOX AI',
    layer: 'QSAI Learner',
    quantumPrinciples: {
      superposition: 'Parallel ML model training',
      entanglement: 'Correlated data insights',
      tunneling: 'Breakthrough pattern discovery'
    },
    quantumScore: 96
  },
  {
    id: '3',
    role: 'Chief Financial Officer',
    brandEntity: 'Goliath of All Trade',
    layer: 'Quantum High Council',
    quantumPrinciples: {
      superposition: 'Multi-scenario financial modeling',
      entanglement: 'Global financial synchronization',
      tunneling: 'Impossible ROI achievements'
    },
    quantumScore: 94
  },
  {
    id: '4',
    role: 'Senior Market Strategist',
    brandEntity: 'Sigma Select',
    layer: 'Q-Sales Division',
    quantumPrinciples: {
      superposition: 'Infinite market positioning',
      entanglement: 'Synchronized growth strategies',
      tunneling: 'Market barrier penetration'
    },
    quantumScore: 92
  }
]

export default function QuantumIntegration() {
  const [selectedPrinciple, setSelectedPrinciple] = useState<string>('superposition')
  const [expandedRole, setExpandedRole] = useState<string | null>(null)

  const selectedPrincipleData = quantumPrinciples.find(p => p.id === selectedPrinciple)

  return (
    <div className="space-y-12">
      {/* Header */}
      <div className="text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="inline-flex items-center gap-2 bg-gradient-to-r from-indigo-100 to-purple-100 px-4 py-2 rounded-full mb-6"
        >
          <Atom className="w-5 h-5 text-indigo-600" />
          <span className="text-indigo-800 font-medium">Quantum Integration</span>
        </motion.div>
        
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
          Quantum Principles Across All Roles
        </h2>
        
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Superposition, Entanglement, and Tunneling principles embedded into every advanced role for quantum-enhanced performance.
        </p>
      </div>

      {/* Quantum Principles Selector */}
      <div className="flex justify-center">
        <div className="flex bg-white rounded-xl p-2 shadow-lg border border-gray-100">
          {quantumPrinciples.map((principle) => {
            const IconComponent = principle.icon
            return (
              <button
                key={principle.id}
                onClick={() => setSelectedPrinciple(principle.id)}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg transition-all duration-300 ${
                  selectedPrinciple === principle.id
                    ? `bg-${principle.color}-100 text-${principle.color}-800`
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <IconComponent className="w-5 h-5" />
                <span className="font-medium">{principle.name}</span>
              </button>
            )
          })}
        </div>
      </div>

      {/* Selected Principle Details */}
      {selectedPrincipleData && (
        <motion.div
          key={selectedPrinciple}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-xl p-8 shadow-lg border border-gray-100"
        >
          <div className="text-center mb-8">
            <div className={`inline-flex items-center gap-3 mb-4`}>
              <div className={`p-3 bg-${selectedPrincipleData.color}-100 rounded-lg`}>
                <selectedPrincipleData.icon className={`w-8 h-8 text-${selectedPrincipleData.color}-600`} />
              </div>
              <h3 className="text-2xl font-bold text-gray-900">{selectedPrincipleData.name}</h3>
            </div>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              {selectedPrincipleData.description}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {selectedPrincipleData.applications.map((app, index) => (
              <motion.div
                key={app.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-50 rounded-lg p-6"
              >
                <h4 className="font-semibold text-gray-900 mb-2">{app.advancedRole}</h4>
                <p className="text-sm text-gray-600 mb-3">{app.implementation}</p>
                <div className="space-y-2">
                  <div className={`text-sm font-medium text-${selectedPrincipleData.color}-600`}>
                    {app.benefit}
                  </div>
                  <div className="text-xs text-gray-500 italic">
                    "{app.example}"
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Role Quantum Mappings */}
      <div>
        <h3 className="text-2xl font-bold text-gray-900 mb-8 text-center">Advanced Roles Quantum Integration</h3>
        
        <div className="space-y-4">
          {roleQuantumMappings.map((mapping, index) => (
            <motion.div
              key={mapping.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden"
            >
              <div 
                className="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => setExpandedRole(expandedRole === mapping.id ? null : mapping.id)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg">
                      <Brain className="w-6 h-6 text-indigo-600" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{mapping.role}</h4>
                      <p className="text-sm text-gray-600">{mapping.brandEntity} • {mapping.layer}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <div className="text-2xl font-bold text-indigo-600">{mapping.quantumScore}%</div>
                      <div className="text-sm text-gray-600">Quantum Score</div>
                    </div>
                    
                    {expandedRole === mapping.id ? (
                      <ChevronUp className="w-5 h-5 text-gray-400" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-gray-400" />
                    )}
                  </div>
                </div>
              </div>
              
              {expandedRole === mapping.id && (
                <motion.div
                  initial={{ opacity: 0, height: 0 }}
                  animate={{ opacity: 1, height: 'auto' }}
                  exit={{ opacity: 0, height: 0 }}
                  className="border-t border-gray-100 p-6 bg-gray-50"
                >
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Layers className="w-4 h-4 text-blue-600" />
                        <span className="font-medium text-blue-800">Superposition</span>
                      </div>
                      <p className="text-sm text-gray-600">{mapping.quantumPrinciples.superposition}</p>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Network className="w-4 h-4 text-purple-600" />
                        <span className="font-medium text-purple-800">Entanglement</span>
                      </div>
                      <p className="text-sm text-gray-600">{mapping.quantumPrinciples.entanglement}</p>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex items-center gap-2">
                        <Zap className="w-4 h-4 text-orange-600" />
                        <span className="font-medium text-orange-800">Tunneling</span>
                      </div>
                      <p className="text-sm text-gray-600">{mapping.quantumPrinciples.tunneling}</p>
                    </div>
                  </div>
                </motion.div>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Quantum Integration Summary */}
      <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl p-8 text-center">
        <div className="flex items-center justify-center gap-2 mb-4">
          <Sparkles className="w-6 h-6 text-indigo-600" />
          <h3 className="text-xl font-bold text-gray-900">Quantum-Enhanced Ecosystem</h3>
        </div>
        
        <p className="text-gray-600 max-w-2xl mx-auto mb-6">
          Every advanced role operates with quantum principles, creating an interconnected ecosystem where 
          traditional limitations dissolve and impossible outcomes become achievable.
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">16</div>
            <div className="text-sm text-gray-600">Quantum-Enhanced Roles</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">∞</div>
            <div className="text-sm text-gray-600">Possible Configurations</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-600 mb-2">97%</div>
            <div className="text-sm text-gray-600">Average Quantum Score</div>
          </div>
        </div>
      </div>
    </div>
  )
}