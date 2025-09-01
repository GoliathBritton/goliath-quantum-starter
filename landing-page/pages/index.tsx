import { useState } from 'react'
import Head from 'next/head'
import { motion } from 'framer-motion'
import { 
  Brain, 
  Zap, 
  Shield, 
  TrendingUp, 
  Users, 
  MessageSquare, 
  Phone, 
  User,
  ArrowRight,
  CheckCircle,
  Star,
  BarChart3,
  Globe,
  Lock,
  Cpu
} from 'lucide-react'

export default function Home() {
  const [activeTab, setActiveTab] = useState('council')

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

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      <Head>
        <title>FLYFOX AI - The Intelligence Economy. Powered by NQBA.</title>
        <meta name="description" content="FLYFOX AI is the quantum-native execution layer powering the intelligence economy. Built for adaptive, intelligent quantum execution with business alignment." />
        <meta name="keywords" content="FLYFOX AI, NQBA, quantum computing, neuromorphic computing, AI agents, business intelligence" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-slate-900/80 backdrop-blur-sm z-50 border-b border-slate-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Brain className="h-8 w-8 text-blue-400 mr-3" />
              <span className="text-xl font-bold text-white">FLYFOX AI</span>
            </div>
            <div className="hidden md:block">
              <div className="ml-10 flex items-baseline space-x-4">
                <a href="#how-it-works" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">How It Works</a>
                <a href="#agents" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Agents</a>
                <a href="#trust" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Trust</a>
                <a href="#demo" className="text-gray-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium">Demo</a>
              </div>
            </div>
            <div className="md:hidden">
              <button className="text-gray-400 hover:text-white">
                <span className="sr-only">Open menu</span>
                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6">
              The Intelligence Economy.
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
                Powered by NQBA.
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto">
              FLYFOX AI is the quantum-native execution layer powering FLYFOX AI, Goliath of All Trade, and Sigma Select. 
              Built for adaptive, intelligent quantum execution with business alignment.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="#demo"
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                Book a Demo
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
              <a
                href="#how-it-works"
                className="inline-flex items-center px-8 py-4 border border-gray-600 text-lg font-medium rounded-lg text-gray-300 hover:text-white hover:border-gray-500 transition-all duration-200"
              >
                Learn More
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              How NQBA Works
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Our 5-layer architecture ensures every decision is governed, traceable, and optimized for business outcomes.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-5 gap-8"
          >
            {[
              {
                title: "High Council",
                description: "Strategic directives and business principles",
                icon: Crown,
                color: "from-purple-500 to-pink-500"
              },
              {
                title: "Q-Cortex",
                description: "Policy interpretation and governance",
                icon: Brain,
                color: "from-blue-500 to-cyan-500"
              },
              {
                title: "NQBA Core",
                description: "Quantum-native execution engine",
                icon: Cpu,
                color: "from-green-500 to-emerald-500"
              },
              {
                title: "Agent Mesh",
                description: "AI agents and business intelligence",
                icon: Users,
                color: "from-yellow-500 to-orange-500"
              },
              {
                title: "SaaS Layer",
                description: "Business applications and integrations",
                icon: Globe,
                color: "from-red-500 to-pink-500"
              }
            ].map((layer, index) => (
              <motion.div
                key={layer.title}
                variants={fadeInUp}
                className="text-center group"
              >
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r ${layer.color} mb-4 group-hover:scale-110 transition-transform duration-200`}>
                  <layer.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{layer.title}</h3>
                <p className="text-gray-400 text-sm">{layer.description}</p>
                {index < 4 && (
                  <div className="hidden md:block absolute top-1/2 right-0 transform -translate-y-1/2 translate-x-1/2">
                    <ArrowRight className="h-6 w-6 text-gray-600" />
                  </div>
                )}
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Agents Section */}
      <section id="agents" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              AI Agents & Business Intelligence
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              From chatbots to digital humans, every agent is powered by NQBA's quantum-native decision engine.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          >
            {[
              {
                title: "Digital Humans",
                description: "AI-powered virtual representatives with personality and emotional intelligence",
                icon: User,
                features: ["Visual consistency", "Personality adaptation", "Cultural sensitivity"]
              },
              {
                title: "Voice Agents",
                description: "Natural language processing with accent neutrality and emotion detection",
                icon: Phone,
                features: ["Accent neutrality", "Emotion detection", "Privacy protection"]
              },
              {
                title: "Chatbots",
                description: "Intelligent conversational agents with content filtering and bias detection",
                icon: MessageSquare,
                features: ["Content filtering", "Bias detection", "LTC logging"]
              },
              {
                title: "Business Agents",
                description: "Specialized AI for sales, finance, and operations optimization",
                icon: BarChart3,
                features: ["Business rule compliance", "Audit trail", "Performance metrics"]
              }
            ].map((agent) => (
              <motion.div
                key={agent.title}
                variants={fadeInUp}
                className="bg-slate-800/50 rounded-xl p-6 border border-slate-700 hover:border-blue-500 transition-all duration-200 hover:shadow-lg hover:shadow-blue-500/20"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-blue-600 mb-4">
                  <agent.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">{agent.title}</h3>
                <p className="text-gray-400 text-sm mb-4">{agent.description}</p>
                <ul className="space-y-2">
                  {agent.features.map((feature) => (
                    <li key={feature} className="flex items-center text-sm text-gray-300">
                      <CheckCircle className="h-4 w-4 text-green-400 mr-2 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Trust Section */}
      <section id="trust" className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Trust & Compliance
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Built for enterprise with immutable audit trails and quantum-grade security.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {[
              {
                title: "LTC Provenance",
                description: "Living Technical Codex provides immutable, hash-chained audit trails for every decision",
                icon: Shield,
                color: "from-green-500 to-emerald-500"
              },
              {
                title: "Quantum Security",
                description: "Post-quantum cryptography and quantum random number generation for future-proof security",
                icon: Lock,
                color: "from-blue-500 to-cyan-500"
              },
              {
                title: "Compliance Ready",
                description: "GDPR, HIPAA, SOX compliance with automated validation and audit logging",
                icon: CheckCircle,
                color: "from-purple-500 to-pink-500"
              }
            ].map((trust) => (
              <motion.div
                key={trust.title}
                variants={fadeInUp}
                className="text-center"
              >
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r ${trust.color} mb-4`}>
                  <trust.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-white mb-3">{trust.title}</h3>
                <p className="text-gray-400">{trust.description}</p>
              </motion.div>
            ))}
          </motion.div>

          {/* Performance Metrics */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            viewport={{ once: true }}
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {[
              { label: "API Response Time", value: "< 100ms", icon: Zap },
              { label: "Quantum Success Rate", value: "85%", icon: Star },
              { label: "Test Coverage", value: "92%", icon: CheckCircle },
              { label: "Uptime", value: "99.9%", icon: TrendingUp }
            ].map((metric) => (
              <div key={metric.label} className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-blue-600 mb-3">
                  <metric.icon className="h-6 w-6 text-white" />
                </div>
                <div className="text-2xl font-bold text-white mb-1">{metric.value}</div>
                <div className="text-sm text-gray-400">{metric.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section id="demo" className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Experience the Future?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              See NQBA Core in action with our Sigma Select lead scoring demo. 
              Experience quantum-powered business intelligence with immutable audit trails.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="mailto:demo@flyfox.ai?subject=Book%20NQBA%20Demo&body=Hi,%20I'd%20like%20to%20book%20a%20demo%20of%20NQBA%20Core."
                className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                Book Your Demo
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
              <a
                href="https://github.com/flyfoxai/nqba-core"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center px-8 py-4 border border-gray-600 text-lg font-medium rounded-lg text-gray-300 hover:text-white hover:border-gray-500 transition-all duration-200"
              >
                View on GitHub
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-700 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <Brain className="h-8 w-8 text-blue-400 mr-3" />
                <span className="text-xl font-bold text-white">FLYFOX AI</span>
              </div>
              <p className="text-gray-400 text-sm">
                The Intelligence Economy. Powered by NQBA.
              </p>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Products</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">NQBA Core</a></li>
                <li><a href="#" className="hover:text-white transition-colors">AI Agents</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Business Intelligence</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Business Units</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">FLYFOX AI</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Goliath of All Trade</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Sigma Select</a></li>
              </ul>
            </div>
            <div>
              <h3 className="text-white font-semibold mb-4">Connect</h3>
              <ul className="space-y-2 text-sm text-gray-400">
                <li><a href="mailto:hello@flyfox.ai" className="hover:text-white transition-colors">hello@flyfox.ai</a></li>
                <li><a href="https://github.com/flyfoxai" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">GitHub</a></li>
                <li><a href="#" className="hover:text-white transition-colors">LinkedIn</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-slate-700 text-center">
            <p className="text-gray-400 text-sm">
              © 2025 FLYFOX AI. All rights reserved. Built with quantum-native intelligence.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

// Crown icon component
function Crown(props: any) {
  return (
    <svg
      {...props}
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
      strokeWidth={2}
    >
      <path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"
      />
    </svg>
  )
}
