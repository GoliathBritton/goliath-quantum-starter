'use client'

import { motion } from 'framer-motion'
import { 
  Building2, 
  Banknote, 
  Factory, 
  Truck, 
  Shield, 
  Zap, 
  Heart, 
  GraduationCap, 
  ShoppingCart, 
  Plane, 
  ArrowRight,
  Target,
  TrendingUp,
  Users,
  Clock,
  CheckCircle,
  Star,
  BarChart3,
  Globe
} from 'lucide-react'
import Link from 'next/link'
import React, { useState } from 'react'

// Type assertions for components
const MotionDiv = motion.div as any
const MotionSection = motion.section as any
const LinkComponent = Link as any

// Type assertions for Lucide icons
const Building2Icon = Building2 as any
const BanknoteIcon = Banknote as any
const FactoryIcon = Factory as any
const TruckIcon = Truck as any
const ShieldIcon = Shield as any
const ZapIcon = Zap as any
const HeartIcon = Heart as any
const GraduationCapIcon = GraduationCap as any
const ShoppingCartIcon = ShoppingCart as any
const PlaneIcon = Plane as any
const ArrowRightIcon = ArrowRight as any
const TargetIcon = Target as any
const TrendingUpIcon = TrendingUp as any
const UsersIcon = Users as any
const ClockIcon = Clock as any
const CheckCircleIcon = CheckCircle as any
const StarIcon = Star as any
const BarChart3Icon = BarChart3 as any
const GlobeIcon = Globe as any

export default function IndustriesPage() {
  const [selectedIndustry, setSelectedIndustry] = useState('financial-services')

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

  const industries = [
    {
      id: 'financial-services',
      name: 'Financial Services',
      icon: BanknoteIcon,
      description: 'Quantum-powered risk assessment, portfolio optimization, and fraud detection',
      color: 'bg-blue-500',
      stats: {
        clients: '45+',
        improvement: '340%',
        savings: '$2.4B'
      },
      useCases: [
        'Real-time risk assessment and portfolio optimization',
        'Quantum-enhanced fraud detection and prevention',
        'Algorithmic trading with quantum advantage',
        'Credit scoring and loan approval automation',
        'Regulatory compliance and stress testing'
      ],
      benefits: [
        'Reduce risk assessment time by 85%',
        'Improve fraud detection accuracy by 340%',
        'Optimize portfolios with quantum algorithms',
        'Automate compliance reporting'
      ],
      caseStudy: {
        client: 'Fortune 500 Bank',
        challenge: 'Manual risk assessment taking weeks',
        solution: 'NQBA quantum risk modeling',
        result: '85% faster risk assessment, $500M in prevented losses'
      }
    },
    {
      id: 'manufacturing',
      name: 'Manufacturing',
      icon: FactoryIcon,
      description: 'Supply chain optimization, predictive maintenance, and quality control',
      color: 'bg-orange-500',
      stats: {
        clients: '32+',
        improvement: '280%',
        savings: '$1.8B'
      },
      useCases: [
        'Supply chain optimization and logistics planning',
        'Predictive maintenance and equipment monitoring',
        'Quality control and defect prediction',
        'Production scheduling and resource allocation',
        'Energy consumption optimization'
      ],
      benefits: [
        'Reduce supply chain costs by 25%',
        'Prevent 90% of equipment failures',
        'Improve quality control accuracy by 280%',
        'Optimize energy consumption by 35%'
      ],
      caseStudy: {
        client: 'Global Automotive Manufacturer',
        challenge: 'Complex supply chain inefficiencies',
        solution: 'NQBA quantum supply chain optimization',
        result: '25% cost reduction, 40% faster delivery times'
      }
    },
    {
      id: 'healthcare',
      name: 'Healthcare',
      icon: HeartIcon,
      description: 'Drug discovery, treatment optimization, and patient outcome prediction',
      color: 'bg-red-500',
      stats: {
        clients: '28+',
        improvement: '450%',
        savings: '$3.2B'
      },
      useCases: [
        'Drug discovery and molecular simulation',
        'Treatment plan optimization and personalization',
        'Medical imaging analysis and diagnosis',
        'Clinical trial optimization and patient matching',
        'Healthcare resource allocation and scheduling'
      ],
      benefits: [
        'Accelerate drug discovery by 60%',
        'Improve treatment outcomes by 450%',
        'Reduce clinical trial costs by 40%',
        'Optimize resource allocation by 35%'
      ],
      caseStudy: {
        client: 'Leading Pharmaceutical Company',
        challenge: 'Slow drug discovery process',
        solution: 'NQBA quantum molecular simulation',
        result: '60% faster discovery, $800M in R&D savings'
      }
    },
    {
      id: 'logistics',
      name: 'Logistics & Transportation',
      icon: TruckIcon,
      description: 'Route optimization, fleet management, and demand forecasting',
      color: 'bg-green-500',
      stats: {
        clients: '38+',
        improvement: '320%',
        savings: '$2.1B'
      },
      useCases: [
        'Route optimization and delivery planning',
        'Fleet management and vehicle scheduling',
        'Demand forecasting and inventory optimization',
        'Warehouse automation and space utilization',
        'Last-mile delivery optimization'
      ],
      benefits: [
        'Reduce delivery times by 30%',
        'Optimize routes with 320% efficiency',
        'Lower fuel costs by 25%',
        'Improve customer satisfaction by 40%'
      ],
      caseStudy: {
        client: 'Global Logistics Provider',
        challenge: 'Inefficient route planning and high fuel costs',
        solution: 'NQBA quantum route optimization',
        result: '30% faster deliveries, 25% fuel cost reduction'
      }
    },
    {
      id: 'energy',
      name: 'Energy & Utilities',
      icon: ZapIcon,
      description: 'Grid optimization, renewable energy management, and demand prediction',
      color: 'bg-yellow-500',
      stats: {
        clients: '22+',
        improvement: '380%',
        savings: '$1.6B'
      },
      useCases: [
        'Smart grid optimization and load balancing',
        'Renewable energy forecasting and integration',
        'Energy trading and market optimization',
        'Predictive maintenance for power infrastructure',
        'Carbon footprint optimization and ESG reporting'
      ],
      benefits: [
        'Improve grid efficiency by 35%',
        'Optimize renewable integration by 380%',
        'Reduce energy waste by 28%',
        'Enhance grid reliability by 45%'
      ],
      caseStudy: {
        client: 'Major Utility Company',
        challenge: 'Complex renewable energy integration',
        solution: 'NQBA quantum grid optimization',
        result: '35% efficiency improvement, $400M in savings'
      }
    },
    {
      id: 'retail',
      name: 'Retail & E-commerce',
      icon: ShoppingCartIcon,
      description: 'Demand forecasting, inventory optimization, and personalized recommendations',
      color: 'bg-purple-500',
      stats: {
        clients: '41+',
        improvement: '290%',
        savings: '$1.9B'
      },
      useCases: [
        'Demand forecasting and inventory management',
        'Personalized product recommendations',
        'Price optimization and dynamic pricing',
        'Supply chain and logistics optimization',
        'Customer behavior analysis and segmentation'
      ],
      benefits: [
        'Reduce inventory costs by 30%',
        'Improve recommendation accuracy by 290%',
        'Optimize pricing strategies by 25%',
        'Increase customer satisfaction by 35%'
      ],
      caseStudy: {
        client: 'Global E-commerce Platform',
        challenge: 'Inaccurate demand forecasting leading to stockouts',
        solution: 'NQBA quantum demand prediction',
        result: '30% inventory cost reduction, 290% forecast accuracy'
      }
    }
  ]

  const selectedIndustryData = industries.find(ind => ind.id === selectedIndustry) || industries[0]

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
              <span className="text-gradient-cyan">Industry</span> Solutions
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Quantum-powered business intelligence transforming industries with 
              unprecedented optimization and insights.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <LinkComponent href="#industries" className="btn-primary">
                Explore Solutions
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </LinkComponent>
              <LinkComponent href="/case-studies" className="btn-secondary">
                View Case Studies
              </LinkComponent>
            </div>
          </MotionDiv>
        </div>
      </section>

      {/* Industry Overview */}
      <section className="section-padding">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Quantum Advantage Across Industries
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our NQBA platform delivers measurable quantum advantages across diverse industry verticals.
            </p>
          </MotionDiv>

          <MotionDiv
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {industries.map((industry) => {
              const Icon = industry.icon
              return (
                <MotionDiv
                  key={industry.id}
                  variants={fadeInUp}
                  className="card group hover:shadow-lg transition-shadow duration-200 cursor-pointer"
                  onClick={() => setSelectedIndustry(industry.id)}
                >
                  <div className="flex items-center space-x-3 mb-4">
                    <div className={`w-12 h-12 ${industry.color} rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-black group-hover:text-brand-cyan transition-colors duration-200">
                      {industry.name}
                    </h3>
                  </div>
                  <p className="text-gray-600 mb-6 leading-relaxed">{industry.description}</p>
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-brand-cyan">{industry.stats.clients}</div>
                      <div className="text-xs text-gray-500">Clients</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-brand-gold">{industry.stats.improvement}</div>
                      <div className="text-xs text-gray-500">Improvement</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-brand-navy">{industry.stats.savings}</div>
                      <div className="text-xs text-gray-500">Savings</div>
                    </div>
                  </div>
                </MotionDiv>
              )
            })}
          </MotionDiv>
        </div>
      </section>

      {/* Detailed Industry View */}
      <section id="industries" className="section-padding bg-gray-50">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="mb-12"
          >
            <div className="flex flex-wrap gap-2 justify-center mb-8">
              {industries.map((industry) => {
                const Icon = industry.icon
                return (
                  <button
                    key={industry.id}
                    onClick={() => setSelectedIndustry(industry.id)}
                    className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors duration-200 ${
                      selectedIndustry === industry.id
                        ? 'bg-brand-cyan text-white'
                        : 'bg-white text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span className="text-sm font-medium">{industry.name}</span>
                  </button>
                )
              })}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
              {/* Use Cases */}
              <div>
                <h3 className="text-2xl font-bold text-black mb-6 flex items-center">
                  <TargetIcon className="mr-3 h-6 w-6 text-brand-cyan" />
                  Use Cases
                </h3>
                <div className="space-y-4">
                  {selectedIndustryData.useCases.map((useCase, index) => (
                    <MotionDiv
                      key={index}
                      initial={{ opacity: 0, x: -20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                      viewport={{ once: true }}
                      className="flex items-start space-x-3"
                    >
                      <CheckCircleIcon className="h-5 w-5 text-brand-cyan mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{useCase}</span>
                    </MotionDiv>
                  ))}
                </div>
              </div>

              {/* Benefits */}
              <div>
                <h3 className="text-2xl font-bold text-black mb-6 flex items-center">
                  <TrendingUpIcon className="mr-3 h-6 w-6 text-brand-gold" />
                  Key Benefits
                </h3>
                <div className="space-y-4">
                  {selectedIndustryData.benefits.map((benefit, index) => (
                    <MotionDiv
                      key={index}
                      initial={{ opacity: 0, x: 20 }}
                      whileInView={{ opacity: 1, x: 0 }}
                      transition={{ duration: 0.5, delay: index * 0.1 }}
                      viewport={{ once: true }}
                      className="flex items-start space-x-3"
                    >
                      <StarIcon className="h-5 w-5 text-brand-gold mt-0.5 flex-shrink-0" />
                      <span className="text-gray-700">{benefit}</span>
                    </MotionDiv>
                  ))}
                </div>
              </div>
            </div>
          </MotionDiv>

          {/* Case Study Highlight */}
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="card bg-white border-l-4 border-brand-cyan"
          >
            <div className="flex items-center space-x-3 mb-6">
              <BarChart3Icon className="h-6 w-6 text-brand-cyan" />
              <h3 className="text-xl font-bold text-black">Success Story</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <h4 className="font-semibold text-black mb-2">Challenge</h4>
                <p className="text-gray-600 text-sm">{selectedIndustryData.caseStudy.challenge}</p>
              </div>
              <div>
                <h4 className="font-semibold text-black mb-2">Solution</h4>
                <p className="text-gray-600 text-sm">{selectedIndustryData.caseStudy.solution}</p>
              </div>
              <div>
                <h4 className="font-semibold text-black mb-2">Result</h4>
                <p className="text-gray-600 text-sm">{selectedIndustryData.caseStudy.result}</p>
              </div>
            </div>
            <div className="mt-6 pt-6 border-t border-gray-200">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-500">Client: {selectedIndustryData.caseStudy.client}</span>
                <LinkComponent href="/case-studies" className="text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200">
                  Read Full Case Study
                  <ArrowRightIcon className="inline ml-2 h-4 w-4" />
                </LinkComponent>
              </div>
            </div>
          </MotionDiv>
        </div>
      </section>

      {/* Industry Stats */}
      <section className="section-padding">
        <div className="container-quantum">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Global Impact
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Delivering quantum advantages to organizations worldwide across all major industries.
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
                metric: "206+",
                label: "Enterprise Clients",
                description: "Across all industries",
                icon: Building2Icon
              },
              {
                metric: "$12.0B",
                label: "Total Savings",
                description: "Generated for clients",
                icon: TrendingUpIcon
              },
              {
                metric: "340%",
                label: "Avg Improvement",
                description: "In key metrics",
                icon: TargetIcon
              },
              {
                metric: "45",
                label: "Countries",
                description: "Global presence",
                icon: GlobeIcon
              }
            ].map((stat) => (
              <MotionDiv
                key={stat.metric}
                variants={fadeInUp}
                className="card text-center group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-brand-cyan rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                  {React.createElement(stat.icon, { className: "h-8 w-8 text-white" }) as JSX.Element}
                </div>
                <div className="text-3xl md:text-4xl font-bold text-black mb-2">
                  {stat.metric}
                </div>
                <div className="font-medium text-black mb-1">{stat.label}</div>
                <div className="text-sm text-gray-500">{stat.description}</div>
              </MotionDiv>
            ))}
          </MotionDiv>
        </div>
      </section>

      {/* Call to Action */}
      <section className="section-padding bg-gray-50">
        <div className="container-narrow text-center">
          <MotionDiv
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Ready to Transform Your Industry?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Discover how quantum business intelligence can revolutionize your operations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8" className="btn-primary" target="_blank" rel="noopener noreferrer">
                Schedule Consultation
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </a>
              <LinkComponent href="/resources/recipes" className="btn-secondary">
                Try QUBO Builder
              </LinkComponent>
            </div>
          </MotionDiv>
        </div>
      </section>
    </div>
  )
}