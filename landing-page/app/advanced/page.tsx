'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Brain, 
  Crown, 
  ChevronRight, 
  Code, 
  Database, 
  Shield, 
  Users, 
  Briefcase, 
  TrendingUp, 
  Zap, 
  Target,
  Settings,
  Globe,
  BarChart3,
  Lightbulb,
  UserCheck
} from 'lucide-react'
import { brand } from '@/lib/brand'
import RoleServiceMapping from '@/components/RoleServiceMapping'
import QSAILearner from '@/components/QSAILearner'
import AgentFactory from '@/components/AgentFactory'
import QSalesDivision from '@/components/QSalesDivision'
import MarketplacePods from '@/components/MarketplacePods'
import QuantumIntegration from '@/components/QuantumIntegration'

const layerIcons = {
  'Quantum High Council': Crown,
  'NQBA Orchestrator': Brain,
  'QSAI Learner': Database,
  'Agent Factory': Settings,
  'Marketplace Pods': Globe
}

const roleIcons = {
  'crown': Crown,
  'briefcase': Briefcase,
  'brain': Brain,
  'code': Code,
  'database': Database,
  'shield': Shield,
  'users': Users,
  'trending-up': TrendingUp,
  'bar-chart': BarChart3,
  'lightbulb': Lightbulb,
  'user-check': UserCheck,
  'settings': Settings,
  'globe': Globe
}

export default function AdvancedPage() {
  const [selectedLayer, setSelectedLayer] = useState<string | null>(null)
  const [selectedRole, setSelectedRole] = useState<string | null>(null)

  const getCouncilMembers = () => {
    return brand.quantumHighCouncil.map(member => ({
      role: member.role,
      title: member.title,
      focus: member.focus,
      quantumAdvantage: member.quantumAdvantage
    }))
  }

  const getLayerRoles = (layerName: string) => {
    const layer = brand.nqbaLayers.find(l => l.name === layerName)
    if (!layer) return []
    
    return layer.advancedRoles.map(roleName => {
      const role = brand.advancedRoles.find(r => r.name === roleName)
      return role || { name: roleName, title: roleName, description: '', capabilities: [], quantumPrinciples: [], brandEntity: '', icon: 'code' }
    })
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Hero Section */}
      <section className="section-padding bg-gradient-to-br from-quantum-purple/5 via-brand-cyan/5 to-brand-gold/5">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-4xl mx-auto"
          >
            <h1 className="text-5xl md:text-7xl font-bold text-black mb-6">
              Advanced AI Integration
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8">
              A living ecosystem of 16 specialized AI roles, quantum-enhanced and integrated across the NQBA architecture for autonomous intelligence.
            </p>
            <div className="flex flex-wrap justify-center gap-4 text-sm text-gray-500">
              <span className="px-4 py-2 bg-white/50 rounded-full border border-gray-200">
                16 Specialized Roles
              </span>
              <span className="px-4 py-2 bg-white/50 rounded-full border border-gray-200">
                5-Layer Architecture
              </span>
              <span className="px-4 py-2 bg-white/50 rounded-full border border-gray-200">
                Quantum-Enhanced
              </span>
              <span className="px-4 py-2 bg-white/50 rounded-full border border-gray-200">
                Cross-feeding Loops
              </span>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Quantum High Council */}
      <section className="section-padding bg-white">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Quantum High Council
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Strategic governance enhanced with advanced advisors for ethical AI, financial optimization, and behavioral architecture.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {getCouncilMembers().map((member, index) => (
              <motion.div
                key={member.role}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-brand-cyan transition-all duration-300 hover:shadow-lg"
              >
                <div className="w-12 h-12 bg-quantum-purple/10 rounded-lg flex items-center justify-center mb-4">
                  <Crown className="w-6 h-6 text-quantum-purple" />
                </div>
                <h3 className="text-lg font-bold text-black mb-2">{member.title}</h3>
                <p className="text-sm text-gray-600 mb-3">{member.focus}</p>
                <div className="text-xs text-brand-cyan font-medium">
                  {member.quantumAdvantage}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* NQBA Architecture Layers */}
      <section className="section-padding bg-gray-50">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Living Ecosystem Architecture
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Each layer enhanced with specialized advanced roles for autonomous intelligence and quantum-optimized operations.
            </p>
          </motion.div>

          <div className="space-y-8">
            {brand.nqbaLayers.map((layer, index) => {
              const LayerIcon = layerIcons[layer.name as keyof typeof layerIcons] || Brain
              const layerRoles = getLayerRoles(layer.name)
              const isSelected = selectedLayer === layer.name

              return (
                <motion.div
                  key={layer.name}
                  initial={{ opacity: 0, x: -20 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-xl border-2 border-gray-200 overflow-hidden hover:border-brand-cyan transition-all duration-300"
                >
                  <div 
                    className="p-6 cursor-pointer"
                    onClick={() => setSelectedLayer(isSelected ? null : layer.name)}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div 
                          className="w-12 h-12 rounded-lg flex items-center justify-center"
                          style={{ backgroundColor: `${layer.color}20` }}
                        >
                          <LayerIcon className="w-6 h-6" style={{ color: layer.color }} />
                        </div>
                        <div>
                          <h3 className="text-xl font-bold text-black">{layer.name}</h3>
                          <p className="text-gray-600">{layer.description}</p>
                        </div>
                      </div>
                      <ChevronRight 
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
                          <h4 className="text-lg font-semibold text-black mb-4">Advanced Roles</h4>
                          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {layerRoles.map((role) => {
                              const RoleIcon = roleIcons[role.icon as keyof typeof roleIcons] || Code
                              return (
                                <div
                                  key={role.name}
                                  className="bg-white rounded-lg p-4 border border-gray-200 hover:border-brand-gold transition-all duration-300 cursor-pointer"
                                  onClick={() => setSelectedRole(selectedRole === role.name ? null : role.name)}
                                >
                                  <div className="flex items-center space-x-3 mb-2">
                                    <RoleIcon className="w-5 h-5 text-brand-gold" />
                                    <span className="font-medium text-black text-sm">{role.title}</span>
                                  </div>
                                  <p className="text-xs text-gray-600 mb-2">{role.description}</p>
                                  <div className="text-xs text-brand-cyan font-medium">
                                    {role.brandEntity}
                                  </div>
                                </div>
                              )
                            })}
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
      </section>

      {/* Role Details Modal */}
      <AnimatePresence>
        {selectedRole && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            onClick={() => setSelectedRole(null)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              className="bg-white rounded-xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              {(() => {
                const role = brand.advancedRoles.find(r => r.name === selectedRole)
                if (!role) return null
                const RoleIcon = roleIcons[role.icon as keyof typeof roleIcons] || Code

                return (
                  <>
                    <div className="flex items-center space-x-4 mb-6">
                      <div className="w-16 h-16 bg-brand-gold/10 rounded-xl flex items-center justify-center">
                        <RoleIcon className="w-8 h-8 text-brand-gold" />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-black">{role.title}</h3>
                        <p className="text-brand-cyan font-medium">{role.brandEntity}</p>
                      </div>
                    </div>

                    <p className="text-gray-600 mb-6">{role.description}</p>

                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-black mb-3">Core Capabilities</h4>
                      <ul className="space-y-2">
                        {role.capabilities.map((capability, index) => (
                          <li key={index} className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-brand-gold rounded-full"></div>
                            <span className="text-gray-700">{capability}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div>
                      <h4 className="text-lg font-semibold text-black mb-3">Quantum Principles</h4>
                      <ul className="space-y-2">
                        {role.quantumPrinciples.map((principle, index) => (
                          <li key={index} className="flex items-center space-x-2">
                            <div className="w-2 h-2 bg-brand-cyan rounded-full"></div>
                            <span className="text-gray-700">{principle}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </>
                )
              })()
              }
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Integration Benefits */}
      <section className="section-padding bg-white">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              What This Unlocks
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              A living ecosystem where every critical organizational function is AI-augmented and quantum-enhanced.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-brand-cyan/10 rounded-xl flex items-center justify-center mx-auto mb-6">
                <Zap className="w-8 h-8 text-brand-cyan" />
              </div>
              <h3 className="text-xl font-bold text-black mb-4">Living Ecosystem of Roles</h3>
              <p className="text-gray-600">
                Every critical organizational function is AI-augmented and quantum-enhanced for autonomous operation.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-brand-gold/10 rounded-xl flex items-center justify-center mx-auto mb-6">
                <TrendingUp className="w-8 h-8 text-brand-gold" />
              </div>
              <h3 className="text-xl font-bold text-black mb-4">Cross-feeding Loops</h3>
              <p className="text-gray-600">
                Each role's outputs are fed into NQBA, re-optimized by QSAI, and deployed into intelligent agents.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
              className="text-center"
            >
              <div className="w-16 h-16 bg-quantum-purple/10 rounded-xl flex items-center justify-center mx-auto mb-6">
                <Target className="w-8 h-8 text-quantum-purple" />
              </div>
              <h3 className="text-xl font-bold text-black mb-4">Branded Business Model</h3>
              <p className="text-gray-600">
                FLYFOX AI (Technology), Goliath (Finance & Energy), Sigma Select (Sales & Leadership) unified.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Role-to-Service Mapping */}
      <section className="section-padding bg-gray-50">
        <div className="container-quantum">
          <RoleServiceMapping />
        </div>
      </section>

      {/* QSAI Learner - Self-Healing Intelligence */}
      <section className="section-padding bg-white">
        <div className="container-quantum">
          <QSAILearner />
        </div>
      </section>

      {/* Agent Factory - Enhanced Production */}
      <section className="section-padding bg-gray-50">
        <div className="container-quantum">
          <AgentFactory />
        </div>
      </section>

      {/* Q-Sales Division - Growth Intelligence */}
      <section className="section-padding bg-white">
        <div className="container-quantum">
          <QSalesDivision />
        </div>
      </section>

      {/* Marketplace Pods - Partner Ecosystem */}
      <section className="section-padding bg-gray-50">
        <div className="container-quantum">
          <MarketplacePods />
        </div>
      </section>

      {/* Quantum Integration - Universal Principles */}
      <section className="section-padding bg-white">
        <div className="container-quantum">
          <QuantumIntegration />
        </div>
      </section>
    </div>
  )
}