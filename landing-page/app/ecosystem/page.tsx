'use client'

import { motion } from 'framer-motion'
import { businessUnits, strategicPartners, nqbaLayers } from '@/lib/brand'

interface EcosystemNode {
  id: string
  name: string
  type: 'platform' | 'business_unit' | 'partner' | 'layer'
  description: string
  connections: string[]
  position: { x: number; y: number }
  color: string
}

const ecosystemNodes: EcosystemNode[] = [
  // Core Platform
  {
    id: 'flyfox-ai',
    name: 'FLYFOX AI',
    type: 'platform',
    description: 'Quantum-Powered Intelligence Platform',
    connections: ['goliath', 'sigma', 'nqba-core'],
    position: { x: 50, y: 20 },
    color: '#27E5FF'
  },
  
  // Business Units
  {
    id: 'goliath',
    name: 'Goliath of All Trade',
    type: 'business_unit',
    description: 'Capital • Energy • Insurance',
    connections: ['flyfox-ai', 'dynex', 'nvidia'],
    position: { x: 20, y: 50 },
    color: '#F5C14C'
  },
  {
    id: 'sigma',
    name: 'Sigma Select',
    type: 'business_unit',
    description: 'Elite Training & Development',
    connections: ['flyfox-ai', 'openai', 'uipath'],
    position: { x: 80, y: 50 },
    color: '#F5C14C'
  },
  
  // NQBA Core
  {
    id: 'nqba-core',
    name: 'NQBA Core',
    type: 'layer',
    description: 'Quantum High Council & Architects',
    connections: ['flyfox-ai', 'quantum-council', 'quantum-architects'],
    position: { x: 50, y: 80 },
    color: '#111827'
  },
  
  // Quantum Governance
  {
    id: 'quantum-council',
    name: 'Quantum High Council',
    type: 'layer',
    description: 'Strategic Governance & Policy',
    connections: ['nqba-core', 'dynex'],
    position: { x: 30, y: 90 },
    color: '#111827'
  },
  {
    id: 'quantum-architects',
    name: 'Quantum Architects',
    type: 'layer',
    description: 'QUBO Design & Optimization',
    connections: ['nqba-core', 'nvidia'],
    position: { x: 70, y: 90 },
    color: '#111827'
  },
  
  // Strategic Partners
  {
    id: 'dynex',
    name: 'Dynex',
    type: 'partner',
    description: 'Quantum Computing Platform',
    connections: ['goliath', 'quantum-council'],
    position: { x: 10, y: 70 },
    color: '#6366F1'
  },
  {
    id: 'nvidia',
    name: 'NVIDIA',
    type: 'partner',
    description: 'GPU Acceleration & AI',
    connections: ['goliath', 'quantum-architects'],
    position: { x: 90, y: 70 },
    color: '#10B981'
  },
  {
    id: 'openai',
    name: 'OpenAI',
    type: 'partner',
    description: 'Large Language Models',
    connections: ['sigma'],
    position: { x: 90, y: 30 },
    color: '#10B981'
  },
  {
    id: 'uipath',
    name: 'UiPath',
    type: 'partner',
    description: 'Process Automation',
    connections: ['sigma'],
    position: { x: 70, y: 30 },
    color: '#10B981'
  }
]

export default function EcosystemPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto text-center">
          <motion.h1 
            className="text-5xl font-bold text-black mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            The Intelligence Economy
          </motion.h1>
          <motion.p 
            className="text-xl text-gray-700 mb-12 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            A quantum-powered ecosystem where artificial intelligence, strategic partnerships, 
            and business innovation converge to create unprecedented value across industries.
          </motion.p>
        </div>
      </section>

      {/* Interactive Ecosystem Map */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-black mb-6">Ecosystem Architecture</h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto">
              Explore the interconnected network of platforms, business units, and strategic partnerships 
              that power the Intelligence Economy.
            </p>
          </div>
          
          {/* Ecosystem Visualization */}
          <div className="relative h-96 bg-white rounded-lg border border-gray-200 overflow-hidden">
            <svg className="w-full h-full" viewBox="0 0 100 100">
              {/* Connection Lines */}
              {ecosystemNodes.map(node => 
                node.connections.map(connectionId => {
                  const connectedNode = ecosystemNodes.find(n => n.id === connectionId)
                  if (!connectedNode) return null
                  
                  return (
                    <motion.line
                      key={`${node.id}-${connectionId}`}
                      x1={node.position.x}
                      y1={node.position.y}
                      x2={connectedNode.position.x}
                      y2={connectedNode.position.y}
                      stroke="#E5E7EB"
                      strokeWidth="0.2"
                      initial={{ pathLength: 0 }}
                      animate={{ pathLength: 1 }}
                      transition={{ duration: 1, delay: 0.5 }}
                    />
                  )
                })
              )}
              
              {/* Ecosystem Nodes */}
              {ecosystemNodes.map((node, index) => (
                <motion.g key={node.id}>
                  <motion.circle
                    cx={node.position.x}
                    cy={node.position.y}
                    r={node.type === 'platform' ? "4" : node.type === 'business_unit' ? "3" : "2"}
                    fill={node.color}
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.5, delay: index * 0.1 }}
                    className="cursor-pointer hover:opacity-80"
                  />
                  <motion.text
                    x={node.position.x}
                    y={node.position.y - (node.type === 'platform' ? 6 : node.type === 'business_unit' ? 5 : 4)}
                    textAnchor="middle"
                    className="text-xs font-semibold fill-black"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: index * 0.1 + 0.3 }}
                  >
                    {node.name}
                  </motion.text>
                  <motion.text
                    x={node.position.x}
                    y={node.position.y + (node.type === 'platform' ? 8 : node.type === 'business_unit' ? 7 : 6)}
                    textAnchor="middle"
                    className="text-xs fill-gray-600"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.5, delay: index * 0.1 + 0.5 }}
                  >
                    {node.description}
                  </motion.text>
                </motion.g>
              ))}
            </svg>
          </div>
        </div>
      </section>

      {/* Business Units Detail */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-black mb-6">Business Units</h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto">
              Specialized divisions driving innovation across key market sectors.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            {businessUnits.map((unit, index) => (
              <motion.div
                key={unit.id}
                className="bg-white p-8 rounded-lg border border-gray-200 hover:border-cyan-300 transition-colors"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.2 }}
              >
                <div className="flex items-center mb-4">
                  <div className="w-3 h-3 bg-gold rounded-full mr-3"></div>
                  <h3 className="text-2xl font-bold text-black">{unit.name}</h3>
                </div>
                <p className="text-gray-700 mb-6">{unit.description}</p>
                <div className="space-y-2">
                  <h4 className="font-semibold text-black">Focus Areas:</h4>
                  <ul className="text-gray-700 space-y-1">
                    {unit.focus_areas.map((area, areaIndex) => (
                      <li key={areaIndex} className="flex items-center">
                        <div className="w-1.5 h-1.5 bg-cyan rounded-full mr-2"></div>
                        {area}
                      </li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* NQBA Architecture */}
      <section className="py-20 px-4 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-black mb-6">NQBA Core Architecture</h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto">
              The five-layer quantum architecture powering intelligent decision-making across the ecosystem.
            </p>
          </div>
          
          <div className="space-y-6">
            {nqbaLayers.map((layer, index) => (
              <motion.div
                key={layer.id}
                className="bg-white p-6 rounded-lg border border-gray-200 hover:border-navy-300 transition-colors"
                initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-navy text-white rounded-full flex items-center justify-center font-bold mr-4">
                      {layer.level}
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-black">{layer.name}</h3>
                      <p className="text-gray-700">{layer.description}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-500">Capabilities</div>
                    <div className="text-sm text-navy font-semibold">
                      {layer.capabilities.length} functions
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Strategic Partners */}
      <section className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-black mb-6">Strategic Partners</h2>
            <p className="text-lg text-gray-700 max-w-2xl mx-auto">
              World-class technology partners enabling quantum-scale innovation.
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {strategicPartners.map((partner, index) => (
              <motion.div
                key={partner.id}
                className="bg-white p-6 rounded-lg border border-gray-200 hover:border-green-300 transition-colors text-center"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <div className="w-8 h-8 bg-green-500 rounded-full"></div>
                </div>
                <h3 className="text-xl font-bold text-black mb-2">{partner.name}</h3>
                <p className="text-gray-700 mb-4">{partner.description}</p>
                <div className="text-sm text-green-600 font-semibold">
                  {partner.integration_type}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 px-4 bg-navy text-white">
        <div className="max-w-4xl mx-auto text-center">
          <motion.h2 
            className="text-4xl font-bold mb-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            Join the Intelligence Economy
          </motion.h2>
          <motion.p 
            className="text-xl mb-8 opacity-90"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Partner with us to harness quantum-powered intelligence for your business transformation.
          </motion.p>
          <motion.div 
            className="flex flex-col sm:flex-row gap-4 justify-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <a href="/contact" className="btn-primary bg-cyan hover:bg-cyan-600">
              Become a Partner
            </a>
            <a href="/products" className="btn-secondary border-white text-white hover:bg-white hover:text-navy">
              Explore Solutions
            </a>
          </motion.div>
        </div>
      </section>
    </div>
  )
}