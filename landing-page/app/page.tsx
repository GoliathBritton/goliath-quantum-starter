'use client'

import React, { useState, useEffect } from 'react'
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
import dynamic from 'next/dynamic'
const DiversegyIntegration = dynamic(() => import('./components/DiversegyIntegration'), { ssr: false, loading: () => <div className="loading-placeholder">Loading Integration...</div> })
const AIPRMIntegration = dynamic(() => import('./components/AIPRMIntegration'), { ssr: false, loading: () => <div className="loading-placeholder">Loading Integration...</div> })
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import { FadeIn, SlideUp, ScrollReveal, StaggerContainer, StaggerItem } from './components/animations'

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
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
  }, [])

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
      <Navbar />
      {/* Hero Section */}
      <section className="hero-section relative overflow-hidden min-h-[90vh] flex items-center bg-gradient-to-br from-blue-50 via-white to-purple-50">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          {/* Gradient Background */}
          <FadeIn duration={1.5}>
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-800 via-purple-800 to-blue-900"></div>
          </FadeIn>
          
          {/* Animated Grid */}
          <FadeIn delay={0.3} duration={2}>
            <div className="absolute inset-0 bg-[url('/grid-pattern.svg')] bg-center opacity-15 bg-repeat"></div>
          </FadeIn>
          
          {/* Subtle Glow Effect */}
          <FadeIn delay={0.6} duration={2.5}>
            <div className="absolute inset-0 bg-gradient-radial from-blue-500/10 via-transparent to-transparent"></div>
          </FadeIn>
          
          {/* Additional Animated Elements */}
          
          {/* Floating Particles */}
          <div className="absolute top-0 left-0 w-full h-full">
            {[...Array(20)].map((_, i) => (
              <MotionDiv
                key={`particle-${i}`}
                className="absolute rounded-full bg-white opacity-20"
                style={{
                  width: Math.random() * 8 + 2 + 'px',
                  height: Math.random() * 8 + 2 + 'px',
                  top: Math.random() * 100 + '%',
                  left: Math.random() * 100 + '%',
                }}
                animate={{
                  y: [0, Math.random() * 100 - 50],
                  x: [0, Math.random() * 100 - 50],
                  opacity: [0.2, 0.8, 0.2],
                }}
                transition={{
                  duration: Math.random() * 20 + 10,
                  repeat: Infinity,
                  repeatType: "reverse",
                }}
              />
            ))}
          </div>
          
          {/* Glowing Orbs */}
          <MotionDiv
            className="absolute -top-20 -right-20 w-96 h-96 rounded-full bg-purple-600 opacity-20 blur-3xl"
            animate={{
              scale: [1, 1.2, 1],
              opacity: [0.2, 0.3, 0.2],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              repeatType: "reverse",
            }}
          />
          <MotionDiv
            className="absolute -bottom-40 -left-20 w-96 h-96 rounded-full bg-indigo-600 opacity-20 blur-3xl"
            animate={{
              scale: [1, 1.3, 1],
              opacity: [0.2, 0.3, 0.2],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              repeatType: "reverse",
            }}
          />
        </div>
        
        <div className="container-quantum relative z-10 pt-20 pb-20">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
            {/* Hero Content */}
            <div className="lg:col-span-6">
              <MotionDiv
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  type: "spring",
                  stiffness: 100,
                  damping: 20
                }}
                className="relative"
              >
                {/* Decorative Element */}
                <div className="absolute -left-6 -top-6 w-20 h-20">
                  <MotionDiv
                    className="w-full h-full"
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  >
                    <svg viewBox="0 0 100 100" className="w-full h-full text-indigo-500 opacity-70">
                      <path d="M50 0 L100 50 L50 100 L0 50 Z" fill="none" stroke="currentColor" strokeWidth="2" />
                    </svg>
                  </MotionDiv>
                </div>
                
                <MotionDiv
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.2 }}
                >
                  <div className="inline-block px-4 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-white/90 text-sm font-medium mb-6">
                    Quantum Computing • AI • Enterprise Solutions
                  </div>
                </MotionDiv>
                
                <MotionDiv
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.8, delay: 0.3 }}
                >
                  <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 text-white">
                    <span className="inline-block bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400">
                      {brand.tagline.split('.')[0]}
                    </span>
                    <br />Powered by NQBA
                  </h1>
                </MotionDiv>
                
                <MotionDiv
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.8, delay: 0.5 }}
                >
                  <p className="text-xl text-white/80 mb-8 backdrop-blur-sm bg-white/5 p-4 rounded-lg border border-white/10">
                    {brand.description}
                  </p>
                </MotionDiv>
                
                <MotionDiv
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.7 }}
                  className="flex flex-wrap gap-4"
                >
                  <MotionDiv 
                    whileHover={{ scale: 1.05 }} 
                    whileTap={{ scale: 0.95 }}
                    className="glow-effect"
                  >
                    <LinkComponent href="#demo" className="quantum-btn inline-block">
                      Book a Demo
                      <MotionDiv
                        animate={{ x: [0, 5, 0] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                        className="inline-block"
                      >
                        <ArrowRightIcon className="ml-2 h-5 w-5 inline" />
                      </MotionDiv>
                    </LinkComponent>
                  </MotionDiv>
                  
                  <MotionDiv 
                    whileHover={{ scale: 1.05 }} 
                    whileTap={{ scale: 0.95 }}
                  >
                    <LinkComponent href="#how-it-works" className="btn-secondary">
                      Learn More
                    </LinkComponent>
                  </MotionDiv>
                </MotionDiv>
                
                {/* Trusted By */}
                <MotionDiv
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.8, delay: 1 }}
                  className="mt-12"
                >
                  <p className="text-sm text-white/60 mb-4">Trusted by industry leaders</p>
                  <div className="flex flex-wrap gap-8 items-center">
                    {['IBM', 'Microsoft', 'Google', 'Amazon'].map((company, i) => (
                      <div key={company} className="text-white/40 font-medium">{company}</div>
                    ))}
                  </div>
                </MotionDiv>
              </MotionDiv>
            </div>
            
            {/* 3D Card */}
            <div className="lg:col-span-6 relative">
              <MotionDiv
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ 
                  type: "spring",
                  stiffness: 100,
                  damping: 20,
                  delay: 0.4
                }}
                className="relative"
              >
                {/* Floating Elements */}
                <MotionDiv
                  className="absolute -top-10 -left-10 w-20 h-20 bg-gradient-to-br from-purple-500 to-indigo-500 rounded-lg opacity-70 blur-sm"
                  animate={{
                    y: [0, -20, 0],
                    rotate: [0, 10, 0],
                    scale: [1, 1.05, 1],
                  }}
                  transition={{
                    duration: 6,
                    repeat: Infinity,
                    repeatType: "reverse",
                  }}
                />
                
                <MotionDiv
                  className="absolute -bottom-10 -right-10 w-20 h-20 bg-gradient-to-br from-indigo-500 to-cyan-500 rounded-full opacity-70 blur-sm"
                  animate={{
                    y: [0, 20, 0],
                    rotate: [0, -10, 0],
                    scale: [1, 1.05, 1],
                  }}
                  transition={{
                    duration: 7,
                    repeat: Infinity,
                    repeatType: "reverse",
                  }}
                />
                
                {/* Main 3D Card */}
                <MotionDiv
                  whileHover={{ 
                    rotateY: 5,
                    rotateX: -5,
                    z: 10,
                    scale: 1.02,
                  }}
                  transition={{ type: "spring", stiffness: 400 }}
                  className="card-3d bg-white/10 backdrop-blur-xl p-8 rounded-2xl border border-white/20 shadow-2xl overflow-hidden transform-gpu perspective-1000"
                >
                  <div className="relative aspect-video bg-gradient-to-br from-indigo-900 to-purple-900 rounded-lg mb-6 overflow-hidden">
                    {/* Quantum Visualization */}
                    <div className="absolute inset-0 flex items-center justify-center">
                      <MotionDiv
                        animate={{ rotate: 360 }}
                        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                        className="w-40 h-40"
                      >
                        <svg viewBox="0 0 100 100" className="w-full h-full text-white opacity-30">
                          <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="2" />
                          <circle cx="50" cy="50" r="30" fill="none" stroke="currentColor" strokeWidth="2" />
                          <circle cx="50" cy="50" r="15" fill="none" stroke="currentColor" strokeWidth="2" />
                        </svg>
                      </MotionDiv>
                    </div>
                    
                    {/* Particles */}
                    {[...Array(10)].map((_, i) => (
                      <MotionDiv
                        key={`viz-particle-${i}`}
                        className="absolute w-2 h-2 rounded-full bg-white"
                        style={{
                          top: Math.random() * 100 + '%',
                          left: Math.random() * 100 + '%',
                        }}
                        animate={{
                          scale: [1, 1.5, 1],
                          opacity: [0.4, 0.8, 0.4],
                        }}
                        transition={{
                          duration: Math.random() * 2 + 1,
                          repeat: Infinity,
                          repeatType: "reverse",
                        }}
                      />
                    ))}
                  </div>
                  
                  <h3 className="text-2xl font-bold mb-3 text-white">Quantum-Enhanced Analytics</h3>
                  <p className="text-white/80 mb-6">
                    Process complex data sets exponentially faster with our quantum algorithms, unlocking insights that were previously impossible to discover.
                  </p>
                  
                  <MotionDiv
                    whileHover={{ x: 5 }}
                    className="flex items-center text-indigo-300 group"
                  >
                    <span className="mr-2 group-hover:mr-3 transition-all">Learn more</span>
                    <ArrowRightIcon className="h-5 w-5" />
                  </MotionDiv>
                  
                  {/* Glow Effect */}
                  <div className="absolute inset-0 -z-10 bg-gradient-to-r from-indigo-500/0 via-purple-500/20 to-pink-500/0 opacity-0 group-hover:opacity-100 blur-xl transition-opacity"></div>
                </MotionDiv>
              </MotionDiv>
            </div>
          </div>
        </div>
      </section>

      {/* Intelligence Economy Business Units */}
      <section className="section-padding bg-white border-t border-gray-200 relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute w-full h-full top-0 left-0 overflow-hidden opacity-10 pointer-events-none">
          <div className="absolute w-96 h-96 -top-20 -left-20 rounded-full bg-gradient-to-br from-cyan-400 to-blue-500 blur-3xl"></div>
          <div className="absolute w-96 h-96 -bottom-20 -right-20 rounded-full bg-gradient-to-br from-purple-500 to-indigo-600 blur-3xl"></div>
        </div>
        
        <div className="container-quantum relative z-10">
          <MotionDiv
            initial={{ opacity: 0, y: 40 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ 
              type: "spring",
              stiffness: 100,
              damping: 20
            }}
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
                whileHover={{ scale: 1.05, y: -15, rotateX: 5, rotateY: 5, z: 50 }}
                transition={{ type: "spring", stiffness: 400 }}
                className="card-quantum card-3d group cursor-pointer relative overflow-hidden transform-gpu perspective-1000"
              >
                {/* Decorative corner accent */}
                <div className="absolute top-0 right-0 w-20 h-20 overflow-hidden">
                  <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-indigo-500 to-purple-600 rotate-45 transform origin-top-right"></div>
                </div>
                
                <MotionDiv 
                  className="absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-10 transition-opacity duration-300"
                  style={{ background: `linear-gradient(135deg, ${unit.color}, transparent)` }}
                />
                <MotionDiv 
                  className="flex items-center justify-center w-24 h-24 rounded-xl mb-6 overflow-hidden shadow-lg"
                  whileHover={{ rotate: 5, scale: 1.1, z: 20 }}
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
                <div className="text-sm font-semibold mb-2 transform transition-transform hover:scale-105" style={{ color: unit.color }}>
                  {unit.focus}
                </div>
                <div className="text-sm text-gray-500 transform transition-transform hover:scale-105">
                  {unit.quantumAdvantage}
                </div>
                
                {/* Interactive glow effect on hover */}
                <div className="absolute inset-0 -z-10 bg-gradient-to-r from-indigo-500/0 via-purple-500/0 to-pink-500/0 opacity-0 group-hover:opacity-100 blur-xl transition-opacity rounded-xl"></div>
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

      {/* Features Section */}
      <section className="section-padding bg-gradient-to-b from-gray-900 to-indigo-900 text-white relative overflow-hidden">
        {/* Background decorative elements */}
        <div className="absolute inset-0 overflow-hidden opacity-20 pointer-events-none">
          <div className="absolute top-0 left-0 w-full h-full bg-[url('/grid-pattern.svg')] bg-center"></div>
          <div className="absolute -top-20 -right-20 w-96 h-96 rounded-full bg-indigo-600 opacity-20 blur-3xl"></div>
          <div className="absolute -bottom-40 -left-20 w-96 h-96 rounded-full bg-purple-600 opacity-20 blur-3xl"></div>
        </div>
        
        <div className="container-quantum relative z-10">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16 fade-up-on-scroll"
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300">
              Quantum-Powered Features
            </h2>
            <p className="text-xl text-white/80 max-w-3xl mx-auto">
              Our platform leverages quantum computing to deliver unprecedented capabilities.
            </p>
          </MotionDiv>

          <MotionDiv
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {[
              {
                title: "Quantum Processing",
                description: "Process complex data sets exponentially faster with our quantum algorithms",
                icon: Cpu,
                color: "from-indigo-500 to-purple-600"
              },
              {
                title: "AI Integration",
                description: "Seamlessly integrate with existing AI systems for enhanced intelligence",
                icon: Brain,
                color: "from-purple-500 to-pink-600"
              },
              {
                title: "Enterprise Security",
                description: "Post-quantum cryptography and quantum random number generation",
                icon: Shield,
                color: "from-blue-500 to-indigo-600"
              }
            ].map((feature, index) => (
              <MotionDiv
                key={feature.title}
                variants={fadeInUp}
                whileHover={{ scale: 1.05 }}
                className={`bg-white/10 backdrop-blur-md p-8 rounded-xl border border-white/20 shadow-xl transform-gpu transition-all duration-500 hover:shadow-2xl hover:border-white/30 ${
                  index % 3 === 0 ? 'slide-in-left-on-scroll' : 
                  index % 3 === 2 ? 'slide-in-right-on-scroll' : 
                  'fade-up-on-scroll'
                } stagger-${index % 5 + 1}`}
              >
                <div className={`w-16 h-16 rounded-lg bg-gradient-to-br ${feature.color} flex items-center justify-center mb-6 shadow-lg`}>
                  {feature.icon === Cpu && <CpuIcon className="h-8 w-8 text-white" />}
                  {feature.icon === Brain && <BrainIcon className="h-8 w-8 text-white" />}
                  {feature.icon === Shield && <ShieldIcon className="h-8 w-8 text-white" />}
                </div>
                <h3 className="text-2xl font-bold mb-3 text-white">{feature.title}</h3>
                <p className="text-white/80">{feature.description}</p>
                
                {/* Decorative element */}
                <div className="w-full h-1 mt-6 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-full opacity-50"></div>
              </MotionDiv>
            ))}
          </MotionDiv>
        </div>
      </section>

          {/* AIPRM Integration Section */}
      <AIPRMIntegration />
      
      {/* Trust Metrics Section */}
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
              Trusted by Industry Leaders
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our quantum solutions are delivering measurable results across industries.
            </p>
          </MotionDiv>
          
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
      <Footer />
    </div>
  )
}