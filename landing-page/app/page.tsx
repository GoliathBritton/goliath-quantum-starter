'use client'

import React, { useState } from 'react'
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
  Cpu,
  Crown
} from 'lucide-react'
import { brand, businessUnits, nqbaLayers, trustMetrics } from '../lib/brand'
import Link from 'next/link'

// Type assertions for motion components
const MotionDiv = motion.div as any
const MotionSection = motion.section as any
const MotionLi = motion.li as any
const LinkComponent = Link as any

// Type assertions for Lucide icons
const BrainIcon = Brain as any
const ZapIcon = Zap as any
const ShieldIcon = Shield as any
const TrendingUpIcon = TrendingUp as any
const UsersIcon = Users as any
const MessageSquareIcon = MessageSquare as any
const PhoneIcon = Phone as any
const UserIcon = User as any
const ArrowRightIcon = ArrowRight as any
const CheckCircleIcon = CheckCircle as any
const StarIcon = Star as any
const BarChart3Icon = BarChart3 as any
const GlobeIcon = Globe as any
const LockIcon = Lock as any
const CpuIcon = Cpu as any
const CrownIcon = Crown as any

export default function HomePage() {
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

  const scaleOnHover = {
    whileHover: { scale: 1.05 },
    transition: { type: "spring", stiffness: 300 }
  }

  const floatingAnimation = {
    animate: {
      y: [-10, 10, -10],
      transition: {
        duration: 6,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  }

  const logoMap = {
    'FLYFOX AI': '/logos/flyfox-logo.png',
    'Goliath of All Trade': '/logos/goliath-logo.png',
    'Sigma Select': '/logos/sigma-logo.png'
  }

  const iconMap = {
    'FLYFOX AI': BrainIcon,
    'Goliath of All Trade': ZapIcon,
    'Sigma Select': StarIcon
  }

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="hero-gradient section-padding">
        <div className="container-quantum text-center">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-black mb-6">
              {brand.tagline.split('.')[0]}.
              <span className="block text-gradient-cyan">
                Powered by NQBA.
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              {brand.description}
            </p>
            <MotionDiv 
              className="flex flex-col sm:flex-row gap-4 justify-center"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
            >
              <MotionDiv whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <LinkComponent href="#demo" className="btn-primary">
                  Book a Demo
                  <MotionDiv
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 1.5, repeat: Infinity }}
                  >
                    <ArrowRightIcon className="ml-2 h-5 w-5" />
                  </MotionDiv>
                </LinkComponent>
              </MotionDiv>
              <MotionDiv whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                <LinkComponent href="#how-it-works" className="btn-secondary">
                  Learn More
                </LinkComponent>
              </MotionDiv>
            </MotionDiv>
          </MotionDiv>
        </div>
      </section>

      {/* Intelligence Economy Business Units */}
      <section className="section-padding bg-white border-t border-gray-200">
        <div className="container-quantum">
          <MotionDiv
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
              Three quantum-powered business units working in harmony to optimize every aspect of modern business.
            </p>
          </MotionDiv>

          <MotionDiv
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {businessUnits.map((unit, index) => (
              <MotionDiv
                key={unit.name}
                variants={fadeInUp}
                whileHover={{ scale: 1.02, y: -8 }}
                className="card-quantum group cursor-pointer relative overflow-hidden"
              >
                <MotionDiv 
                  className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-5 transition-opacity duration-300"
                  style={{ background: `linear-gradient(135deg, ${unit.color}, transparent)` }}
                />
                <MotionDiv 
                  className="flex items-center justify-center w-24 h-24 rounded-xl mb-6 overflow-hidden"
                  whileHover={{ rotate: 5, scale: 1.1 }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  {logoMap[unit.name] ? (
                    <img 
                      src={logoMap[unit.name]} 
                      alt={`${unit.name} Logo`}
                      className="w-full h-full object-contain"
                    />
                  ) : (
                    <div className="w-16 h-16 rounded-full bg-gradient-to-br from-brand-cyan to-brand-gold flex items-center justify-center">
                      {unit.name === 'FLYFOX AI' && <BrainIcon className="h-8 w-8 text-white" />}
                      {unit.name === 'Goliath of All Trade' && <ZapIcon className="h-8 w-8 text-white" />}
                      {unit.name === 'Sigma Select' && <StarIcon className="h-8 w-8 text-white" />}
                    </div>
                  )}
                </MotionDiv>
                <h3 className="text-2xl font-bold text-black mb-3 group-hover:text-brand-cyan transition-colors duration-200">{unit.name}</h3>
                <p className="text-gray-600 mb-4">{unit.description}</p>
                <div className="text-sm font-semibold mb-2" style={{ color: unit.color }}>
                  {unit.focus}
                </div>
                <div className="text-sm text-gray-500">
                  {unit.quantumAdvantage}
                </div>
              </MotionDiv>
            ))}
          </MotionDiv>
        </div>
      </section>

      {/* NQBA 5-Layer Architecture */}
      <section id="how-it-works" className="section-padding">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              How NQBA Works
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our 5-layer architecture ensures every decision is governed, traceable, and optimized for business outcomes.
            </p>
          </MotionDiv>

          <MotionDiv
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-5 gap-6"
          >
            {nqbaLayers.map((layer, index) => (
              <MotionDiv
                key={layer.name}
                variants={fadeInUp}
                whileHover={{ y: -5 }}
                className="text-center group relative"
              >
                <MotionDiv 
                  className="inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 shadow-lg"
                  style={{ backgroundColor: layer.color }}
                  whileHover={{ 
                    scale: 1.15, 
                    rotate: 10,
                    boxShadow: `0 10px 30px ${layer.color}40`
                  }}
                  transition={{ type: "spring", stiffness: 300 }}
                >
                  <span className="text-2xl">{layer.icon}</span>
                </MotionDiv>
                <h3 className="text-xl font-semibold text-black mb-2 group-hover:text-brand-cyan transition-colors duration-200">{layer.name}</h3>
                <p className="text-gray-600 text-sm">{layer.description}</p>
                {index < nqbaLayers.length - 1 && (
                  <MotionDiv 
                    className="hidden md:block absolute top-8 -right-3 transform"
                    animate={{ x: [0, 5, 0] }}
                    transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                  >
                    <ArrowRightIcon className="h-6 w-6 text-brand-cyan" />
                  </MotionDiv>
                )}
              </MotionDiv>
            ))}
          </MotionDiv>
        </div>
      </section>

      {/* AI Agents & Business Intelligence */}
      <section id="agents" className="section-padding bg-white border-t border-gray-200">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              AI Agents & Business Intelligence
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              From chatbots to digital humans, every agent is powered by NQBA's quantum-native decision engine.
            </p>
          </MotionDiv>

          <MotionDiv
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
              <MotionDiv
                key={agent.title}
                variants={fadeInUp}
                whileHover={{ scale: 1.03, y: -5 }}
                className="bg-white rounded-xl p-6 border border-gray-200 hover:border-brand-cyan transition-all duration-300 shadow-sm hover:shadow-xl group"
              >
                <MotionDiv 
                  className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-brand-cyan mb-4"
                  whileHover={{ rotate: 360, scale: 1.1 }}
                  transition={{ duration: 0.6 }}
                >
                  {agent.title === "Digital Humans" && <UserIcon className="h-6 w-6 text-white" />}
                  {agent.title === "Voice Agents" && <PhoneIcon className="h-6 w-6 text-white" />}
                  {agent.title === "Chatbots" && <MessageSquareIcon className="h-6 w-6 text-white" />}
                  {agent.title === "Business Agents" && <BarChart3Icon className="h-6 w-6 text-white" />}
                </MotionDiv>
                <h3 className="text-xl font-semibold text-black mb-3 group-hover:text-brand-cyan transition-colors duration-200">{agent.title}</h3>
                <p className="text-gray-600 text-sm mb-4">{agent.description}</p>
                <ul className="space-y-2">
                  {agent.features.map((feature, idx) => (
                    <MotionLi 
                      key={feature} 
                      className="flex items-center text-sm text-gray-600"
                      initial={{ opacity: 0, x: -10 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      transition={{ delay: idx * 0.1 }}
                    >
                      <CheckCircleIcon className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {feature}
                    </MotionLi>
                  ))}
                </ul>
              </MotionDiv>
            ))}
          </MotionDiv>
        </div>
      </section>

      {/* Trust & Compliance */}
      <section id="trust" className="section-padding">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Trust & Compliance
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Built for enterprise with immutable audit trails and quantum-grade security.
            </p>
          </MotionDiv>

          <MotionDiv
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16"
          >
            {[
              {
                title: "LTC Provenance",
                description: "Living Technical Codex provides immutable, hash-chained audit trails for every decision",
                icon: Shield,
                color: "bg-quantum-emerald"
              },
              {
                title: "Quantum Security",
                description: "Post-quantum cryptography and quantum random number generation for future-proof security",
                icon: Lock,
                color: "bg-quantum-blue"
              },
              {
                title: "Compliance Ready",
                description: "GDPR, HIPAA, SOX compliance with automated validation and audit logging",
                icon: CheckCircle,
                color: "bg-quantum-purple"
              }
            ].map((trust) => (
              <MotionDiv
                key={trust.title}
                variants={fadeInUp}
                className="text-center"
              >
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full ${trust.color} mb-4`}>
                  {trust.title === "Quantum Security" && <LockIcon className="h-8 w-8 text-white" />}
                  {trust.title === "Global Compliance" && <GlobeIcon className="h-8 w-8 text-white" />}
                  {trust.title === "Regulatory Adherence" && <CheckCircleIcon className="h-8 w-8 text-white" />}
                </div>
                <h3 className="text-xl font-semibold text-black mb-3">{trust.title}</h3>
                <p className="text-gray-600">{trust.description}</p>
              </MotionDiv>
            ))}
          </MotionDiv>

          {/* Trust Metrics */}
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8"
          >
            {trustMetrics.map((metric, index) => (
              <MotionDiv 
                key={metric.label} 
                className="text-center group cursor-pointer"
                whileHover={{ scale: 1.05, y: -5 }}
                animate={{
                  y: [0, -5, 0],
                  transition: {
                    duration: 3 + index * 0.5,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }
                }}
              >
                <MotionDiv 
                  className="text-4xl mb-2 group-hover:scale-110 transition-transform duration-200"
                  whileHover={{ rotate: [0, -10, 10, 0] }}
                  transition={{ duration: 0.5 }}
                >
                  {metric.icon}
                </MotionDiv>
                <div className="text-2xl font-bold text-black mb-1 group-hover:text-brand-cyan transition-colors duration-200">{metric.value}</div>
                <div className="text-sm text-gray-600">{metric.label}</div>
              </MotionDiv>
            ))}
          </MotionDiv>
        </div>
      </section>

      {/* Call to Action */}
      <section id="demo" className="section-padding bg-white border-t border-gray-200">
        <div className="container-narrow text-center">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Ready to Experience the Future?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              See NQBA Core in action with our Sigma Select lead scoring demo. 
              Experience quantum-powered business intelligence with immutable audit trails.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8"
                className="btn-primary"
              >
                Book Your Demo
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </a>
              <LinkComponent href="/resources" className="btn-secondary">
                Explore Resources
              </LinkComponent>
            </div>
          </MotionDiv>
        </div>
      </section>
    </div>
  )
}