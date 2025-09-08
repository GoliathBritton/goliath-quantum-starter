'use client'

import { motion } from 'framer-motion'
import { 
  ArrowRight, 
  Building2, 
  Users, 
  Zap, 
  Shield, 
  BarChart3,
  CheckCircle,
  Clock,
  Target,
  TrendingUp
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

export default function PipelinePage() {
  const [activeStep, setActiveStep] = useState(0)

  const pipelineSteps = [
    {
      title: 'Discovery & Assessment',
      description: 'Analyze your current business processes and identify quantum optimization opportunities',
      duration: '1-2 weeks',
      deliverables: ['Business Process Audit', 'Quantum Readiness Assessment', 'ROI Projections']
    },
    {
      title: 'NQBA Architecture Design',
      description: 'Design custom quantum-native architecture tailored to your business requirements',
      duration: '2-3 weeks',
      deliverables: ['System Architecture Blueprint', 'Integration Roadmap', 'Security Framework']
    },
    {
      title: 'Pilot Implementation',
      description: 'Deploy NQBA Core with selected business units for proof of concept',
      duration: '4-6 weeks',
      deliverables: ['Pilot Deployment', 'Performance Metrics', 'User Training']
    },
    {
      title: 'Full Deployment',
      description: 'Scale quantum intelligence across your entire organization',
      duration: '8-12 weeks',
      deliverables: ['Enterprise Deployment', 'Advanced AI Agents', 'Ongoing Support']
    }
  ]

  const fadeInUp = {
    initial: { opacity: 0, y: 60 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

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
              <span className="text-gradient-cyan">Pipeline</span> Builder
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Transform your business with our proven quantum intelligence implementation methodology.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact" className="btn-primary">
                Start Your Journey
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/case-studies" className="btn-secondary">
                View Success Stories
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Implementation Pipeline */}
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
              Implementation Pipeline
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our structured approach ensures successful quantum transformation with measurable business outcomes.
            </p>
          </motion.div>

          <div className="space-y-8">
            {pipelineSteps.map((step, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
                className={`card-quantum p-8 cursor-pointer transition-all duration-300 ${
                  activeStep === index ? 'ring-2 ring-brand-cyan' : ''
                }`}
                onClick={() => setActiveStep(index)}
              >
                <div className="flex items-start space-x-6">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center text-white font-bold ${
                    activeStep === index ? 'bg-brand-cyan' : 'bg-gray-400'
                  }`}>
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-black mb-2">{step.title}</h3>
                    <p className="text-gray-600 mb-4">{step.description}</p>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="flex items-center space-x-2">
                        <Clock className="h-5 w-5 text-brand-cyan" />
                        <span className="text-sm font-medium">{step.duration}</span>
                      </div>
                      <div className="md:col-span-2">
                        <div className="text-sm font-medium text-black mb-2">Key Deliverables:</div>
                        <div className="flex flex-wrap gap-2">
                          {step.deliverables.map((deliverable, idx) => (
                            <span
                              key={idx}
                              className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-xs"
                            >
                              {deliverable}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
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
              Ready to Build Your Pipeline?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Let's discuss your quantum transformation journey and create a custom implementation plan.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8" className="btn-primary" target="_blank" rel="noopener noreferrer">
                Schedule Consultation
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
              <Link href="/resources" className="btn-secondary">
                Download Resources
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}