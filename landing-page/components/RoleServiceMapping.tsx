'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Code, Database, Cloud, Shield, TrendingUp, 
  Users, Briefcase, Settings, Target, Megaphone,
  ArrowRight, ExternalLink, Zap
} from 'lucide-react'
import { brand } from '@/lib/brand'

interface ServiceMapping {
  role: string
  services: {
    name: string
    type: 'API' | 'Microservice' | 'Platform Module' | 'Database' | 'Infrastructure'
    description: string
    endpoint?: string
    status: 'Active' | 'Development' | 'Planned'
  }[]
}

const serviceMappings: ServiceMapping[] = [
  {
    role: 'Chief Technology Officer',
    services: [
      {
        name: 'Architecture Decision API',
        type: 'API',
        description: 'Multi-tech roadmap and quantum adoption strategies',
        endpoint: '/api/v1/architecture/decisions',
        status: 'Active'
      },
      {
        name: 'Technology Stack Optimizer',
        type: 'Microservice',
        description: 'Automated technology selection and integration',
        status: 'Development'
      },
      {
        name: 'Quantum Readiness Assessment',
        type: 'Platform Module',
        description: 'Evaluates system quantum compatibility',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Software Engineer',
    services: [
      {
        name: 'Code Generation API',
        type: 'API',
        description: 'Quantum-safe microservices generation',
        endpoint: '/api/v1/codegen',
        status: 'Active'
      },
      {
        name: 'Security Audit Engine',
        type: 'Microservice',
        description: 'Automated security vulnerability scanning',
        status: 'Active'
      },
      {
        name: 'Deployment Orchestrator',
        type: 'Infrastructure',
        description: 'Multi-environment deployment automation',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Data Scientist',
    services: [
      {
        name: 'Quantum ML Pipeline',
        type: 'API',
        description: 'Quantum machine learning model training',
        endpoint: '/api/v1/quantum-ml',
        status: 'Development'
      },
      {
        name: 'Predictive Analytics Engine',
        type: 'Microservice',
        description: 'Real-time prediction and forecasting',
        status: 'Active'
      },
      {
        name: 'Model Registry',
        type: 'Database',
        description: 'Centralized ML model versioning and deployment',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Data Analyst',
    services: [
      {
        name: 'Real-time Analytics API',
        type: 'API',
        description: 'Live business intelligence and insights',
        endpoint: '/api/v1/analytics/realtime',
        status: 'Active'
      },
      {
        name: 'Performance Metrics Engine',
        type: 'Microservice',
        description: 'KPI tracking and optimization recommendations',
        status: 'Active'
      },
      {
        name: 'Data Visualization Platform',
        type: 'Platform Module',
        description: 'Interactive dashboards and reporting',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Cybersecurity Specialist',
    services: [
      {
        name: 'Threat Detection API',
        type: 'API',
        description: 'Real-time anomaly detection and response',
        endpoint: '/api/v1/security/threats',
        status: 'Active'
      },
      {
        name: 'Post-Quantum Crypto Service',
        type: 'Microservice',
        description: 'Quantum-resistant encryption protocols',
        status: 'Development'
      },
      {
        name: 'Security Compliance Monitor',
        type: 'Platform Module',
        description: 'Automated compliance checking and reporting',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Programmer',
    services: [
      {
        name: 'Agent Logic Optimizer',
        type: 'API',
        description: 'QUBO workflow optimization and reusability',
        endpoint: '/api/v1/agents/optimize',
        status: 'Active'
      },
      {
        name: 'Code Quality Analyzer',
        type: 'Microservice',
        description: 'Automated code review and improvement suggestions',
        status: 'Active'
      },
      {
        name: 'Agent Factory SDK',
        type: 'Platform Module',
        description: 'Development toolkit for quantum agents',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Product Engineer',
    services: [
      {
        name: 'Multi-Modal Features API',
        type: 'API',
        description: 'Voice and digital twin integration',
        endpoint: '/api/v1/features/multimodal',
        status: 'Development'
      },
      {
        name: 'User Experience Optimizer',
        type: 'Microservice',
        description: 'A/B testing and UX improvement automation',
        status: 'Active'
      },
      {
        name: 'Feature Flag Manager',
        type: 'Platform Module',
        description: 'Dynamic feature rollout and management',
        status: 'Active'
      }
    ]
  },
  {
    role: 'Senior Project Manager',
    services: [
      {
        name: 'Agile Delivery API',
        type: 'API',
        description: 'Project tracking and KPI management',
        endpoint: '/api/v1/projects/agile',
        status: 'Active'
      },
      {
        name: 'Resource Allocation Engine',
        type: 'Microservice',
        description: 'Optimal team and resource distribution',
        status: 'Active'
      },
      {
        name: 'Version Control Integration',
        type: 'Platform Module',
        description: 'Automated release management and versioning',
        status: 'Active'
      }
    ]
  }
]

const serviceTypeColors = {
  'API': 'bg-brand-cyan/10 text-brand-cyan border-brand-cyan/30',
  'Microservice': 'bg-brand-gold/10 text-brand-gold border-brand-gold/30',
  'Platform Module': 'bg-quantum-purple/10 text-quantum-purple border-quantum-purple/30',
  'Database': 'bg-green-100 text-green-700 border-green-300',
  'Infrastructure': 'bg-orange-100 text-orange-700 border-orange-300'
}

const statusColors = {
  'Active': 'bg-green-100 text-green-700',
  'Development': 'bg-yellow-100 text-yellow-700',
  'Planned': 'bg-gray-100 text-gray-700'
}

export default function RoleServiceMapping() {
  const [selectedRole, setSelectedRole] = useState<string | null>(null)
  const [filterType, setFilterType] = useState<string>('All')
  const [filterStatus, setFilterStatus] = useState<string>('All')

  const serviceTypes = ['All', 'API', 'Microservice', 'Platform Module', 'Database', 'Infrastructure']
  const statuses = ['All', 'Active', 'Development', 'Planned']

  const filteredMappings = serviceMappings.filter(mapping => {
    if (selectedRole && mapping.role !== selectedRole) return false
    
    const hasMatchingType = filterType === 'All' || mapping.services.some(s => s.type === filterType)
    const hasMatchingStatus = filterStatus === 'All' || mapping.services.some(s => s.status === filterStatus)
    
    return hasMatchingType && hasMatchingStatus
  })

  return (
    <div className="bg-white">
      {/* Header */}
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-black mb-4">Role-to-Service Mapping Grid</h2>
        <p className="text-gray-600 mb-6">
          Comprehensive mapping of advanced roles to specific APIs, microservices, and platform modules.
        </p>
        
        {/* Filters */}
        <div className="flex flex-wrap gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Service Type</label>
            <select 
              value={filterType} 
              onChange={(e) => setFilterType(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-cyan focus:border-transparent"
            >
              {serviceTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select 
              value={filterStatus} 
              onChange={(e) => setFilterStatus(e.target.value)}
              className="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-brand-cyan focus:border-transparent"
            >
              {statuses.map(status => (
                <option key={status} value={status}>{status}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Role Cards */}
      <div className="space-y-6">
        {filteredMappings.map((mapping, index) => {
          const role = brand.advancedRoles.find(r => r.name === mapping.role)
          const isSelected = selectedRole === mapping.role
          
          return (
            <motion.div
              key={mapping.role}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="bg-white border-2 border-gray-200 rounded-xl overflow-hidden hover:border-brand-cyan transition-all duration-300"
            >
              <div 
                className="p-6 cursor-pointer"
                onClick={() => setSelectedRole(isSelected ? null : mapping.role)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-brand-gold/10 rounded-lg flex items-center justify-center">
                      <Code className="w-6 h-6 text-brand-gold" />
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-black">{role?.title || mapping.role}</h3>
                      <p className="text-gray-600">{role?.brandEntity}</p>
                      <div className="flex items-center space-x-2 mt-1">
                        <span className="text-sm text-brand-cyan font-medium">
                          {mapping.services.length} Services
                        </span>
                        <span className="text-gray-400">•</span>
                        <span className="text-sm text-gray-500">
                          {mapping.services.filter(s => s.status === 'Active').length} Active
                        </span>
                      </div>
                    </div>
                  </div>
                  <ArrowRight 
                    className={`w-5 h-5 text-gray-400 transition-transform duration-300 ${
                      isSelected ? 'rotate-90' : ''
                    }`} 
                  />
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
                      <div className="grid gap-4">
                        {mapping.services.map((service, serviceIndex) => (
                          <motion.div
                            key={service.name}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: serviceIndex * 0.1 }}
                            className="bg-white rounded-lg p-4 border border-gray-200 hover:border-brand-gold transition-all duration-300"
                          >
                            <div className="flex items-start justify-between mb-3">
                              <div className="flex-1">
                                <div className="flex items-center space-x-3 mb-2">
                                  <h4 className="font-semibold text-black">{service.name}</h4>
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${serviceTypeColors[service.type]}`}>
                                    {service.type}
                                  </span>
                                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${statusColors[service.status]}`}>
                                    {service.status}
                                  </span>
                                </div>
                                <p className="text-gray-600 text-sm mb-2">{service.description}</p>
                                {service.endpoint && (
                                  <div className="flex items-center space-x-2">
                                    <code className="text-xs bg-gray-100 px-2 py-1 rounded font-mono text-gray-700">
                                      {service.endpoint}
                                    </code>
                                    <ExternalLink className="w-3 h-3 text-gray-400" />
                                  </div>
                                )}
                              </div>
                            </div>
                          </motion.div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )
        })}
      </div>

      {/* Service Type Legend */}
      <div className="mt-8 p-6 bg-gray-50 rounded-xl">
        <h3 className="text-lg font-semibold text-black mb-4">Service Type Legend</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {Object.entries(serviceTypeColors).map(([type, className]) => (
            <div key={type} className="flex items-center space-x-2">
              <div className={`w-3 h-3 rounded-full border ${className}`}></div>
              <span className="text-sm text-gray-700">{type}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}