'use client'

import { motion } from 'framer-motion'
import { 
  Brain, 
  Zap, 
  Shield, 
  Users, 
  Target, 
  Globe, 
  Crown, 
  Cpu,
  ArrowRight,
  CheckCircle,
  Star,
  Award,
  TrendingUp
} from 'lucide-react'
import { businessUnits, nqbaLayers, strategicPartners } from '../../lib/brand'
import Link from 'next/link'

export default function AboutPage() {
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

  const teamMembers = [
    {
      name: "Dr. Sarah Chen",
      role: "Chief Quantum Officer",
      bio: "Former IBM Quantum researcher with 15+ years in quantum computing and business optimization.",
      expertise: "Quantum Algorithms, QUBO Optimization"
    },
    {
      name: "Marcus Rodriguez",
      role: "Head of AI Ethics",
      bio: "Leading expert in AI governance and compliance frameworks for enterprise applications.",
      expertise: "AI Ethics, Regulatory Compliance"
    },
    {
      name: "Dr. Priya Patel",
      role: "Director of Business Intelligence",
      bio: "Former McKinsey partner specializing in data-driven business transformation.",
      expertise: "Business Strategy, Data Analytics"
    }
  ]

  const milestones = [
    {
      year: "2023",
      title: "NQBA Core Foundation",
      description: "Developed the 5-layer quantum-native business architecture with immutable audit trails."
    },
    {
      year: "2024",
      title: "Strategic Partnerships",
      description: "Established partnerships with Dynex, NVIDIA, and leading workflow automation platforms."
    },
    {
      year: "2024",
      title: "Intelligence Economy Launch",
      description: "Launched three business units: FLYFOX AI, Goliath of All Trade, and Sigma Select."
    },
    {
      year: "2025",
      title: "Quantum-First Enterprise",
      description: "Scaling quantum-powered business intelligence across Fortune 500 companies."
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
              About <span className="text-gradient-cyan">FLYFOX AI</span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              We're building the future of business intelligence with quantum-native architecture 
              and immutable decision provenance.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="section-padding">
        <div className="container-quantum">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-black mb-6">Our Mission</h2>
              <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                To democratize quantum-powered business intelligence while ensuring every decision 
                is traceable, auditable, and ethically sound. We believe that the future of business 
                lies in quantum-native architectures that can handle the complexity of modern enterprises.
              </p>
              <div className="space-y-4">
                {[
                  "Quantum-first business architecture",
                  "Immutable audit trails for all decisions",
                  "AI ethics and compliance by design",
                  "Democratized access to quantum computing"
                ].map((item) => (
                  <div key={item} className="flex items-center space-x-3">
                    <CheckCircle className="h-5 w-5 text-green-500 flex-shrink-0" />
                    <span className="text-gray-700">{item}</span>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="bg-gray-50 p-8 rounded-2xl"
            >
              <h3 className="text-2xl font-bold text-black mb-4">Our Vision</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                A world where every business decision is optimized by quantum computing, 
                governed by ethical AI, and backed by immutable provenance records.
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-brand-cyan mb-1">99.9%</div>
                  <div className="text-sm text-gray-600">Decision Accuracy</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-brand-gold mb-1">100%</div>
                  <div className="text-sm text-gray-600">Audit Compliance</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-brand-cyan mb-1">50x</div>
                  <div className="text-sm text-gray-600">Processing Speed</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-brand-gold mb-1">24/7</div>
                  <div className="text-sm text-gray-600">Quantum Monitoring</div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Intelligence Economy Structure */}
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
              The Intelligence Economy
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our three-pillar approach to quantum-powered business transformation.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8"
          >
            {businessUnits.map((unit, index) => (
              <motion.div
                key={unit.name}
                variants={fadeInUp}
                className="card-quantum group relative overflow-hidden"
              >
                <div className="absolute top-0 right-0 w-20 h-20 opacity-10">
                  <div className="text-6xl" style={{ color: unit.color }}>
                    {unit.icon}
                  </div>
                </div>
                <div className="relative z-10">
                  <div className="text-4xl mb-4">{unit.icon}</div>
                  <h3 className="text-2xl font-bold text-black mb-3">{unit.name}</h3>
                  <p className="text-gray-600 mb-4">{unit.description}</p>
                  <div className="text-sm font-semibold mb-4" style={{ color: unit.color }}>
                    {unit.focus}
                  </div>
                  <div className="text-sm text-gray-500 mb-6">
                    {unit.quantumAdvantage}
                  </div>
                  <Link 
                    href={`/industries#${unit.name.toLowerCase().replace(/\s+/g, '-')}`}
                    className="inline-flex items-center text-sm font-medium hover:text-brand-cyan transition-colors duration-200"
                    style={{ color: unit.color }}
                  >
                    Learn More
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Link>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* NQBA Architecture Deep Dive */}
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
              NQBA Core Architecture
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our 5-layer quantum-native business architecture ensures every decision 
              is governed, traceable, and optimized.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="space-y-8"
          >
            {nqbaLayers.map((layer, index) => (
              <motion.div
                key={layer.name}
                variants={fadeInUp}
                className={`flex flex-col lg:flex-row items-center gap-8 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}
              >
                <div className="lg:w-1/2">
                  <div className="flex items-center space-x-4 mb-4">
                    <div 
                      className="w-12 h-12 rounded-full flex items-center justify-center"
                      style={{ backgroundColor: layer.color }}
                    >
                      <span className="text-2xl">{layer.icon}</span>
                    </div>
                    <div>
                      <h3 className="text-2xl font-bold text-black">{layer.name}</h3>
                      <div className="text-sm text-gray-500">Layer {index + 1}</div>
                    </div>
                  </div>
                  <p className="text-gray-600 text-lg leading-relaxed mb-6">
                    {layer.description}
                  </p>
                  <div className="space-y-2">
                    {layer.capabilities?.map((capability) => (
                      <div key={capability} className="flex items-center space-x-2">
                        <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                        <span className="text-sm text-gray-700">{capability}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="lg:w-1/2">
                  <div 
                    className="w-full h-64 rounded-2xl flex items-center justify-center"
                    style={{ backgroundColor: `${layer.color}20` }}
                  >
                    <div className="text-8xl opacity-50" style={{ color: layer.color }}>
                      {layer.icon}
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Team Section */}
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
              Leadership Team
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              World-class experts in quantum computing, AI ethics, and business intelligence.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {teamMembers.map((member) => (
              <motion.div
                key={member.name}
                variants={fadeInUp}
                className="card text-center"
              >
                <div className="w-24 h-24 bg-gradient-to-br from-brand-cyan to-brand-gold rounded-full mx-auto mb-6 flex items-center justify-center">
                  <User className="h-12 w-12 text-white" />
                </div>
                <h3 className="text-xl font-bold text-black mb-2">{member.name}</h3>
                <div className="text-brand-cyan font-semibold mb-3">{member.role}</div>
                <p className="text-gray-600 text-sm mb-4 leading-relaxed">{member.bio}</p>
                <div className="text-xs text-gray-500 font-medium">
                  Expertise: {member.expertise}
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Company Timeline */}
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
              Our Journey
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From quantum research to enterprise-ready business intelligence platform.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="relative"
          >
            {/* Timeline line */}
            <div className="absolute left-1/2 transform -translate-x-px h-full w-0.5 bg-gray-300"></div>
            
            {milestones.map((milestone, index) => (
              <motion.div
                key={milestone.year}
                variants={fadeInUp}
                className={`relative flex items-center mb-12 ${index % 2 === 0 ? 'justify-start' : 'justify-end'}`}
              >
                <div className={`w-5/12 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8 text-left'}`}>
                  <div className="card">
                    <div className="text-2xl font-bold text-brand-cyan mb-2">{milestone.year}</div>
                    <h3 className="text-xl font-bold text-black mb-3">{milestone.title}</h3>
                    <p className="text-gray-600">{milestone.description}</p>
                  </div>
                </div>
                
                {/* Timeline dot */}
                <div className="absolute left-1/2 transform -translate-x-1/2 w-4 h-4 bg-brand-cyan rounded-full border-4 border-white shadow-lg"></div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="section-padding bg-gray-50">
        <div className="container-narrow text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Join the Quantum Revolution
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Ready to transform your business with quantum-powered intelligence? 
              Let's build the future together.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact" className="btn-primary">
                Get Started
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/case-studies" className="btn-secondary">
                View Case Studies
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}