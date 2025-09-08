'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, Shield, TrendingUp, Users, Zap, 
  Activity, AlertTriangle, CheckCircle, 
  BarChart3, Eye, Cpu, Database
} from 'lucide-react'
import { brand } from '@/lib/brand'

interface LearningMetric {
  name: string
  value: number
  unit: string
  trend: 'up' | 'down' | 'stable'
  role: string
}

interface SelfHealingEvent {
  id: string
  timestamp: string
  type: 'anomaly_detected' | 'bias_corrected' | 'performance_optimized' | 'threat_mitigated'
  description: string
  role: string
  severity: 'low' | 'medium' | 'high'
  status: 'active' | 'resolved' | 'monitoring'
}

const learningMetrics: LearningMetric[] = [
  {
    name: 'Quantum ML Accuracy',
    value: 94.7,
    unit: '%',
    trend: 'up',
    role: 'Data Scientist'
  },
  {
    name: 'Real-time Insights',
    value: 1247,
    unit: '/min',
    trend: 'up',
    role: 'Data Analyst'
  },
  {
    name: 'Bias Detection Rate',
    value: 99.2,
    unit: '%',
    trend: 'stable',
    role: 'Human Psychology'
  },
  {
    name: 'Threat Response Time',
    value: 0.3,
    unit: 'ms',
    trend: 'down',
    role: 'Cybersecurity'
  },
  {
    name: 'Model Adaptation Speed',
    value: 15.8,
    unit: 's',
    trend: 'down',
    role: 'Data Scientist'
  },
  {
    name: 'Behavioral Optimization',
    value: 87.3,
    unit: '%',
    trend: 'up',
    role: 'Human Psychology'
  }
]

const selfHealingEvents: SelfHealingEvent[] = [
  {
    id: '1',
    timestamp: '2024-01-15T10:30:00Z',
    type: 'anomaly_detected',
    description: 'Unusual pattern in quantum state transitions detected and auto-corrected',
    role: 'Data Scientist',
    severity: 'medium',
    status: 'resolved'
  },
  {
    id: '2',
    timestamp: '2024-01-15T10:25:00Z',
    type: 'bias_corrected',
    description: 'Gender bias in recommendation algorithm automatically neutralized',
    role: 'Human Psychology',
    severity: 'high',
    status: 'resolved'
  },
  {
    id: '3',
    timestamp: '2024-01-15T10:20:00Z',
    type: 'threat_mitigated',
    description: 'Potential quantum cryptographic attack vector identified and blocked',
    role: 'Cybersecurity',
    severity: 'high',
    status: 'resolved'
  },
  {
    id: '4',
    timestamp: '2024-01-15T10:15:00Z',
    type: 'performance_optimized',
    description: 'Query performance improved by 23% through automatic index optimization',
    role: 'Data Analyst',
    severity: 'low',
    status: 'active'
  }
]

const roleColors = {
  'Data Scientist': 'text-brand-cyan',
  'Data Analyst': 'text-brand-gold',
  'Human Psychology': 'text-quantum-purple',
  'Cybersecurity': 'text-red-600'
}

const eventTypeIcons = {
  'anomaly_detected': AlertTriangle,
  'bias_corrected': Users,
  'performance_optimized': TrendingUp,
  'threat_mitigated': Shield
}

const severityColors = {
  'low': 'bg-green-100 text-green-700 border-green-300',
  'medium': 'bg-yellow-100 text-yellow-700 border-yellow-300',
  'high': 'bg-red-100 text-red-700 border-red-300'
}

const statusColors = {
  'active': 'bg-blue-100 text-blue-700',
  'resolved': 'bg-green-100 text-green-700',
  'monitoring': 'bg-yellow-100 text-yellow-700'
}

export default function QSAILearner() {
  const [selectedRole, setSelectedRole] = useState<string | null>(null)
  const [realTimeMetrics, setRealTimeMetrics] = useState(learningMetrics)
  const [isLearning, setIsLearning] = useState(true)

  // Simulate real-time learning updates
  useEffect(() => {
    if (!isLearning) return

    const interval = setInterval(() => {
      setRealTimeMetrics(prev => prev.map(metric => ({
        ...metric,
        value: metric.value + (Math.random() - 0.5) * 2
      })))
    }, 2000)

    return () => clearInterval(interval)
  }, [isLearning])

  const qsaiRoles = brand.advancedRoles.filter(role => 
    ['Senior Data Scientist', 'Senior Data Analyst', 'Senior Human Psychology Insight', 'Senior Cybersecurity Specialist'].includes(role.name)
  )

  const filteredMetrics = selectedRole 
    ? realTimeMetrics.filter(m => m.role === selectedRole)
    : realTimeMetrics

  const filteredEvents = selectedRole 
    ? selfHealingEvents.filter(e => e.role === selectedRole)
    : selfHealingEvents

  return (
    <div className="bg-white">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="w-12 h-12 bg-brand-cyan/10 rounded-xl flex items-center justify-center">
            <Brain className="w-6 h-6 text-brand-cyan" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-black">QSAI Learner</h2>
            <p className="text-gray-600">Self-Healing Intelligence Layer</p>
          </div>
          <div className="flex-1"></div>
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full ${isLearning ? 'bg-green-500 animate-pulse' : 'bg-gray-400'}`}></div>
            <span className="text-sm text-gray-600">
              {isLearning ? 'Learning Active' : 'Learning Paused'}
            </span>
          </div>
        </div>
        
        <p className="text-gray-600 mb-6">
          Advanced AI system integrating Data Science, Analytics, Human Psychology, and Cybersecurity for autonomous learning and self-correction.
        </p>
      </div>

      {/* Role Filter */}
      <div className="mb-8">
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedRole(null)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
              selectedRole === null 
                ? 'bg-brand-navy text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            All Roles
          </button>
          {['Data Scientist', 'Data Analyst', 'Human Psychology', 'Cybersecurity'].map(role => (
            <button
              key={role}
              onClick={() => setSelectedRole(selectedRole === role ? null : role)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 ${
                selectedRole === role 
                  ? 'bg-brand-navy text-white' 
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {role}
            </button>
          ))}
        </div>
      </div>

      {/* Real-time Metrics */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-black mb-4">Real-time Learning Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredMetrics.map((metric, index) => (
            <motion.div
              key={metric.name}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-brand-cyan transition-all duration-300"
            >
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-black text-sm">{metric.name}</h4>
                <div className={`text-xs px-2 py-1 rounded-full ${roleColors[metric.role as keyof typeof roleColors]} bg-gray-100`}>
                  {metric.role}
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
                {metric.trend === 'stable' && <Activity className="w-4 h-4 text-gray-500" />}
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-2">
                <motion.div 
                  className="bg-brand-cyan h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${Math.min(metric.value, 100)}%` }}
                  transition={{ duration: 1, delay: index * 0.1 }}
                ></motion.div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Self-Healing Events */}
      <div className="mb-8">
        <h3 className="text-xl font-bold text-black mb-4">Self-Healing Events</h3>
        <div className="space-y-4">
          {filteredEvents.map((event, index) => {
            const EventIcon = eventTypeIcons[event.type]
            
            return (
              <motion.div
                key={event.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-white border border-gray-200 rounded-lg p-4 hover:border-brand-gold transition-all duration-300"
              >
                <div className="flex items-start space-x-4">
                  <div className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <EventIcon className="w-5 h-5 text-gray-600" />
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="font-medium text-black">{event.description}</span>
                    </div>
                    
                    <div className="flex items-center space-x-4 text-sm">
                      <span className={`px-2 py-1 rounded-full ${roleColors[event.role as keyof typeof roleColors]} bg-gray-100`}>
                        {event.role}
                      </span>
                      <span className={`px-2 py-1 rounded-full border ${severityColors[event.severity]}`}>
                        {event.severity}
                      </span>
                      <span className={`px-2 py-1 rounded-full ${statusColors[event.status]}`}>
                        {event.status}
                      </span>
                      <span className="text-gray-500">
                        {new Date(event.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  </div>
                  
                  {event.status === 'resolved' && (
                    <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  )}
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>

      {/* Embedded Roles */}
      <div>
        <h3 className="text-xl font-bold text-black mb-4">Embedded Advanced Roles</h3>
        <div className="grid md:grid-cols-2 gap-6">
          {qsaiRoles.map((role, index) => (
            <motion.div
              key={role.name}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-brand-cyan transition-all duration-300"
            >
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-brand-gold/10 rounded-lg flex items-center justify-center">
                  <span className="text-lg">{role.icon}</span>
                </div>
                <div>
                  <h4 className="font-bold text-black">{role.title}</h4>
                  <p className="text-sm text-brand-cyan">{role.brandEntity}</p>
                </div>
              </div>
              
              <p className="text-gray-600 text-sm mb-4">{role.description}</p>
              
              <div className="space-y-2">
                <h5 className="font-medium text-black text-sm">Key Capabilities:</h5>
                <ul className="space-y-1">
                  {role.capabilities.slice(0, 2).map((capability, capIndex) => (
                    <li key={capIndex} className="flex items-center space-x-2 text-sm text-gray-600">
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