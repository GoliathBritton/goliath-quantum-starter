'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { 
  Cpu, 
  Shield, 
  Zap, 
  Brain, 
  Crown, 
  Globe, 
  Lock, 
  BarChart3,
  ArrowRight,
  CheckCircle,
  Star,
  Users,
  Clock,
  Database,
  Code,
  Workflow,
  MessageSquare,
  Phone,
  User
} from 'lucide-react'
import { nqbaLayers, strategicPartners, pricingTiers } from '../../lib/brand'
import Link from 'next/link'

export default function ProductsPage() {
  const [activeTab, setActiveTab] = useState('core')
  const [activePricing, setActivePricing] = useState('pro')

  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  const staggerContainer = {
    animate: {
      transition: {
        staggerChildren: 0.1
      }
    }
  }

  const products = {
    core: {
      name: "NQBA Core",
      tagline: "Quantum-Native Business Architecture",
      description: "The foundational platform that powers all quantum business intelligence with immutable audit trails and ethical AI governance.",
      features: [
        "5-layer quantum architecture",
        "Immutable LTC provenance",
        "Real-time decision optimization",
        "Compliance automation",
        "Multi-provider quantum access",
        "Enterprise-grade security"
      ],
      capabilities: [
        {
          title: "Quantum High Council",
          description: "Strategic governance layer ensuring all decisions align with business objectives and ethical standards.",
          icon: Crown
        },
        {
          title: "Quantum Architects",
          description: "Design and orchestration layer that structures business processes for quantum optimization.",
          icon: Brain
        },
        {
          title: "QUBO Optimization",
          description: "Core quantum processing layer that solves complex business optimization problems.",
          icon: Cpu
        },
        {
          title: "LTC Provenance",
          description: "Living Technical Codex providing immutable audit trails for every business decision.",
          icon: Shield
        },
        {
          title: "Business Intelligence",
          description: "Advanced analytics and reporting with quantum-enhanced insights and predictions.",
          icon: BarChart3
        }
      ]
    },
    agents: {
      name: "AI Agents Suite",
      tagline: "Quantum-Powered Business Agents",
      description: "Intelligent agents for every business function, powered by NQBA Core with built-in compliance and audit trails.",
      features: [
        "Digital humans with personality",
        "Voice agents with emotion detection",
        "Chatbots with bias filtering",
        "Business process automation",
        "Multi-modal interactions",
        "Real-time compliance monitoring"
      ],
      capabilities: [
        {
          title: "Digital Humans",
          description: "AI-powered virtual representatives with consistent personality and cultural sensitivity.",
          icon: User
        },
        {
          title: "Voice Agents",
          description: "Natural language processing with accent neutrality and emotional intelligence.",
          icon: Phone
        },
        {
          title: "Chatbots",
          description: "Intelligent conversational agents with content filtering and bias detection.",
          icon: MessageSquare
        },
        {
          title: "Business Agents",
          description: "Specialized AI for sales, finance, operations, and customer service automation.",
          icon: BarChart3
        },
        {
          title: "Workflow Automation",
          description: "End-to-end process automation with quantum-optimized decision making.",
          icon: Workflow
        }
      ]
    },
    platform: {
      name: "Enterprise Platform",
      tagline: "Complete Quantum Business Ecosystem",
      description: "Full-stack quantum business platform with integrated development tools, monitoring, and enterprise features.",
      features: [
        "Visual pipeline builder",
        "Real-time monitoring dashboard",
        "API management console",
        "Multi-tenant architecture",
        "Advanced security controls",
        "24/7 quantum monitoring"
      ],
      capabilities: [
        {
          title: "Pipeline Builder",
          description: "Visual drag-and-drop interface for creating quantum business workflows and QUBO recipes.",
          icon: Code
        },
        {
          title: "Monitoring Dashboard",
          description: "Real-time visibility into quantum processing, performance metrics, and business outcomes.",
          icon: BarChart3
        },
        {
          title: "API Gateway",
          description: "Secure, scalable API management with rate limiting, authentication, and monitoring.",
          icon: Globe
        },
        {
          title: "Data Management",
          description: "Enterprise data integration with quantum-safe encryption and compliance controls.",
          icon: Database
        },
        {
          title: "Security Center",
          description: "Comprehensive security management with post-quantum cryptography and audit logging.",
          icon: Lock
        }
      ]
    }
  }

  const integrations = [
    {
      name: "Dynex",
      category: "Quantum Computing",
      description: "Primary quantum computing platform for QUBO optimization",
      icon: "⚛️",
      status: "Native"
    },
    {
      name: "NVIDIA",
      category: "GPU Computing",
      description: "High-performance GPU acceleration for quantum simulations",
      icon: "🚀",
      status: "Integrated"
    },
    {
      name: "OpenAI",
      category: "AI Models",
      description: "Large language models for natural language processing",
      icon: "🧠",
      status: "Connected"
    },
    {
      name: "UiPath",
      category: "RPA",
      description: "Robotic process automation for business workflows",
      icon: "🤖",
      status: "Partner"
    },
    {
      name: "n8n",
      category: "Workflow",
      description: "Lightweight workflow automation and integration",
      icon: "🔗",
      status: "Partner"
    },
    {
      name: "Mendix",
      category: "Low-Code",
      description: "Low-code application development platform",
      icon: "⚡",
      status: "Partner"
    },
    {
      name: "Prismatic",
      category: "Integration",
      description: "SaaS integration platform for customer workflows",
      icon: "🔌",
      status: "Partner"
    }
  ]

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="hero-gradient section-padding">
        <div className="container-quantum text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-black mb-6">
              <span className="text-gradient-cyan">Quantum-Powered</span>
              <br />Business Intelligence
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Transform your business with NQBA Core - the world's first quantum-native 
              business architecture with immutable audit trails.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#pricing" className="btn-primary">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="#demo" className="btn-secondary">
                Book a Demo
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Product Tabs */}
      <section className="section-padding">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Complete Quantum Business Suite
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need to build, deploy, and scale quantum-powered business intelligence.
            </p>
          </motion.div>

          {/* Tab Navigation */}
          <div className="flex flex-col sm:flex-row justify-center mb-12">
            <div className="inline-flex bg-gray-100 rounded-lg p-1">
              {Object.entries(products).map(([key, product]) => (
                <button
                  key={key}
                  onClick={() => setActiveTab(key)}
                  className={`px-6 py-3 rounded-md font-medium transition-all duration-200 ${
                    activeTab === key
                      ? 'bg-white text-brand-cyan shadow-sm'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {product.name}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center"
          >
            <div>
              <h3 className="text-3xl font-bold text-black mb-4">
                {products[activeTab].name}
              </h3>
              <div className="text-brand-cyan font-semibold mb-4">
                {products[activeTab].tagline}
              </div>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                {products[activeTab].description}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8">
                {products[activeTab].features.map((feature) => (
                  <div key={feature} className="flex items-center space-x-2">
                    <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{feature}</span>
                  </div>
                ))}
              </div>
              <Link href="#pricing" className="btn-primary">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </div>

            <div className="space-y-4">
              {products[activeTab].capabilities.map((capability) => (
                <div key={capability.title} className="card group hover:shadow-lg transition-shadow duration-200">
                  <div className="flex items-start space-x-4">
                    <div className="w-12 h-12 bg-brand-cyan rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
                      <capability.icon className="h-6 w-6 text-white" />
                    </div>
                    <div className="flex-1">
                      <h4 className="text-lg font-semibold text-black mb-2">
                        {capability.title}
                      </h4>
                      <p className="text-gray-600 text-sm">
                        {capability.description}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* NQBA Architecture */}
      <section className="section-padding bg-gray-50">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              NQBA 5-Layer Architecture
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Every layer designed for quantum-native business intelligence with 
              immutable audit trails and ethical AI governance.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-5 gap-6"
          >
            {nqbaLayers.map((layer, index) => (
              <motion.div
                key={layer.name}
                variants={fadeInUp}
                className="text-center group relative"
              >
                <div 
                  className="inline-flex items-center justify-center w-20 h-20 rounded-full mb-6 group-hover:scale-110 transition-transform duration-200"
                  style={{ backgroundColor: layer.color }}
                >
                  <span className="text-3xl">{layer.icon}</span>
                </div>
                <h3 className="text-xl font-semibold text-black mb-3">{layer.name}</h3>
                <p className="text-gray-600 text-sm leading-relaxed">{layer.description}</p>
                {index < nqbaLayers.length - 1 && (
                  <div className="hidden md:block absolute top-10 -right-3 transform">
                    <ArrowRight className="h-6 w-6 text-gray-400" />
                  </div>
                )}
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Integrations */}
      <section className="section-padding">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Strategic Integrations
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built-in connections to leading quantum, AI, and workflow platforms.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
          >
            {integrations.map((integration) => (
              <motion.div
                key={integration.name}
                variants={fadeInUp}
                className="card group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="flex items-start space-x-4">
                  <div className="text-3xl">{integration.icon}</div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold text-black">{integration.name}</h3>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        integration.status === 'Native' ? 'bg-green-100 text-green-800' :
                        integration.status === 'Integrated' ? 'bg-blue-100 text-blue-800' :
                        integration.status === 'Connected' ? 'bg-purple-100 text-purple-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {integration.status}
                      </span>
                    </div>
                    <div className="text-sm text-brand-cyan font-medium mb-2">
                      {integration.category}
                    </div>
                    <p className="text-gray-600 text-sm">
                      {integration.description}
                    </p>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="section-padding bg-gray-50">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Choose Your Quantum Journey
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From startups to enterprise, we have a plan that scales with your quantum ambitions.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {pricingTiers.map((tier) => (
              <motion.div
                key={tier.name}
                variants={fadeInUp}
                className={`card relative overflow-hidden ${
                  tier.popular ? 'ring-2 ring-brand-cyan' : ''
                }`}
              >
                {tier.popular && (
                  <div className="absolute top-0 right-0 bg-brand-cyan text-white px-3 py-1 text-sm font-medium">
                    Most Popular
                  </div>
                )}
                <div className="text-center mb-6">
                  <h3 className="text-2xl font-bold text-black mb-2">{tier.name}</h3>
                  <div className="text-4xl font-bold text-brand-cyan mb-2">
                    {tier.price}
                    {tier.price !== 'Custom' && <span className="text-lg text-gray-500">/month</span>}
                  </div>
                  <p className="text-gray-600">{tier.description}</p>
                </div>
                
                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                      <span className="text-sm text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <Link
                  href={tier.cta.link}
                  className={`w-full text-center ${
                    tier.popular ? 'btn-primary' : 'btn-secondary'
                  }`}
                >
                  {tier.cta.text}
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Call to Action */}
      <section id="demo" className="section-padding">
        <div className="container-narrow text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Ready to Go Quantum?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join leading enterprises already transforming their business with NQBA Core. 
              Start your quantum journey today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8"
                className="btn-primary"
              >
                Book Your Demo
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
              <Link href="/resources/recipes" className="btn-secondary">
                Try QUBO Builder
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}