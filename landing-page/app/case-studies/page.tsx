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
  ShoppingCart,
  ArrowRight,
  Target,
  TrendingUp,
  Users,
  Clock,
  CheckCircle,
  Star,
  BarChart3,
  Award,
  Download,
  ExternalLink,
  Calendar,
  MapPin
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

export default function CaseStudiesPage() {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedCaseStudy, setSelectedCaseStudy] = useState(null)

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

  const categories = [
    { id: 'all', name: 'All Industries', count: 12 },
    { id: 'financial', name: 'Financial Services', count: 4 },
    { id: 'manufacturing', name: 'Manufacturing', count: 3 },
    { id: 'healthcare', name: 'Healthcare', count: 2 },
    { id: 'logistics', name: 'Logistics', count: 2 },
    { id: 'energy', name: 'Energy', count: 1 }
  ]

  const caseStudies = [
    {
      id: 'global-bank-risk',
      title: 'Global Bank Transforms Risk Assessment with Quantum Computing',
      client: 'Fortune 500 International Bank',
      industry: 'financial',
      location: 'New York, USA',
      duration: '8 months',
      teamSize: '12 specialists',
      icon: Banknote,
      color: 'bg-blue-500',
      featured: true,
      challenge: 'Manual risk assessment processes taking 2-3 weeks per portfolio, leading to delayed decisions and missed opportunities in volatile markets.',
      solution: 'Implemented NQBA Core platform with quantum-enhanced risk modeling, real-time portfolio optimization, and automated compliance reporting.',
      results: [
        '85% reduction in risk assessment time (from 3 weeks to 2 days)',
        '$500M in prevented losses through early risk detection',
        '340% improvement in fraud detection accuracy',
        '60% faster regulatory compliance reporting'
      ],
      metrics: {
        timeReduction: '85%',
        costSavings: '$500M',
        accuracyImprovement: '340%',
        roiAchieved: '450%'
      },
      technologies: ['NQBA Core', 'Dynex Quantum', 'Risk Analytics AI', 'Compliance Automation'],
      testimonial: {
        quote: "The quantum advantage in risk assessment has transformed our decision-making speed and accuracy. We're now able to respond to market changes in real-time.",
        author: "Chief Risk Officer",
        company: "Fortune 500 International Bank"
      }
    },
    {
      id: 'automotive-supply-chain',
      title: 'Automotive Giant Optimizes Global Supply Chain',
      client: 'Leading Automotive Manufacturer',
      industry: 'manufacturing',
      location: 'Detroit, USA',
      duration: '6 months',
      teamSize: '8 specialists',
      icon: Factory,
      color: 'bg-orange-500',
      featured: true,
      challenge: 'Complex global supply chain with 500+ suppliers causing delays, excess inventory, and $2B in annual inefficiencies.',
      solution: 'Deployed NQBA quantum supply chain optimization with predictive analytics, real-time supplier monitoring, and automated procurement.',
      results: [
        '25% reduction in supply chain costs ($500M annual savings)',
        '40% faster delivery times to customers',
        '60% reduction in excess inventory',
        '90% improvement in supplier performance prediction'
      ],
      metrics: {
        costReduction: '25%',
        deliveryImprovement: '40%',
        inventoryOptimization: '60%',
        predictionAccuracy: '90%'
      },
      technologies: ['NQBA Core', 'Supply Chain AI', 'Predictive Analytics', 'IoT Integration'],
      testimonial: {
        quote: "NQBA's quantum optimization has revolutionized our supply chain. We've achieved cost savings we never thought possible.",
        author: "VP of Supply Chain",
        company: "Leading Automotive Manufacturer"
      }
    },
    {
      id: 'pharma-drug-discovery',
      title: 'Pharmaceutical Company Accelerates Drug Discovery',
      client: 'Global Pharmaceutical Leader',
      industry: 'healthcare',
      location: 'Basel, Switzerland',
      duration: '12 months',
      teamSize: '15 specialists',
      icon: Heart,
      color: 'bg-red-500',
      featured: true,
      challenge: 'Traditional drug discovery taking 10-15 years with 90% failure rate, costing billions in R&D with uncertain outcomes.',
      solution: 'Implemented NQBA quantum molecular simulation, AI-powered compound analysis, and predictive clinical trial optimization.',
      results: [
        '60% faster drug discovery timeline (from 12 years to 5 years)',
        '$800M reduction in R&D costs',
        '450% improvement in compound success prediction',
        '40% more efficient clinical trials'
      ],
      metrics: {
        timeAcceleration: '60%',
        costReduction: '$800M',
        predictionImprovement: '450%',
        trialEfficiency: '40%'
      },
      technologies: ['NQBA Core', 'Quantum Molecular Simulation', 'AI Drug Discovery', 'Clinical Trial AI'],
      testimonial: {
        quote: "The quantum advantage in molecular simulation has transformed our approach to drug discovery. We're bringing life-saving treatments to market faster than ever.",
        author: "Head of R&D",
        company: "Global Pharmaceutical Leader"
      }
    },
    {
      id: 'logistics-route-optimization',
      title: 'Logistics Provider Revolutionizes Delivery Network',
      client: 'International Logistics Company',
      industry: 'logistics',
      location: 'Memphis, USA',
      duration: '4 months',
      teamSize: '6 specialists',
      icon: Truck,
      color: 'bg-green-500',
      featured: false,
      challenge: 'Inefficient route planning across 50,000 daily deliveries resulting in high fuel costs, delayed deliveries, and customer dissatisfaction.',
      solution: 'Deployed NQBA quantum route optimization with real-time traffic integration, dynamic rerouting, and predictive demand modeling.',
      results: [
        '30% reduction in delivery times',
        '25% decrease in fuel consumption',
        '320% improvement in route efficiency',
        '40% increase in customer satisfaction'
      ],
      metrics: {
        deliveryImprovement: '30%',
        fuelSavings: '25%',
        routeEfficiency: '320%',
        customerSatisfaction: '40%'
      },
      technologies: ['NQBA Core', 'Quantum Route Optimization', 'Real-time Analytics', 'Predictive Modeling'],
      testimonial: {
        quote: "NQBA's quantum route optimization has given us a competitive edge. Our delivery network is now the most efficient in the industry.",
        author: "Operations Director",
        company: "International Logistics Company"
      }
    },
    {
      id: 'energy-grid-optimization',
      title: 'Utility Company Optimizes Smart Grid with Quantum',
      client: 'Major Electric Utility',
      industry: 'energy',
      location: 'California, USA',
      duration: '10 months',
      teamSize: '10 specialists',
      icon: Zap,
      color: 'bg-yellow-500',
      featured: false,
      challenge: 'Complex grid management with renewable energy integration causing instability, waste, and $400M in annual inefficiencies.',
      solution: 'Implemented NQBA quantum grid optimization with renewable forecasting, load balancing, and automated demand response.',
      results: [
        '35% improvement in grid efficiency',
        '380% better renewable energy integration',
        '28% reduction in energy waste',
        '$400M in annual operational savings'
      ],
      metrics: {
        gridEfficiency: '35%',
        renewableIntegration: '380%',
        wasteReduction: '28%',
        costSavings: '$400M'
      },
      technologies: ['NQBA Core', 'Quantum Grid Optimization', 'Renewable Forecasting', 'Smart Grid AI'],
      testimonial: {
        quote: "The quantum optimization has transformed our grid operations. We're now leading the industry in renewable energy integration.",
        author: "Chief Technology Officer",
        company: "Major Electric Utility"
      }
    },
    {
      id: 'retail-demand-forecasting',
      title: 'E-commerce Platform Perfects Demand Prediction',
      client: 'Global E-commerce Leader',
      industry: 'retail',
      location: 'Seattle, USA',
      duration: '5 months',
      teamSize: '7 specialists',
      icon: ShoppingCart,
      color: 'bg-purple-500',
      featured: false,
      challenge: 'Inaccurate demand forecasting leading to $1B in excess inventory and frequent stockouts affecting customer experience.',
      solution: 'Deployed NQBA quantum demand prediction with customer behavior analysis, seasonal modeling, and dynamic inventory optimization.',
      results: [
        '30% reduction in inventory costs',
        '290% improvement in forecast accuracy',
        '45% decrease in stockouts',
        '35% increase in customer satisfaction'
      ],
      metrics: {
        inventoryReduction: '30%',
        forecastAccuracy: '290%',
        stockoutReduction: '45%',
        customerSatisfaction: '35%'
      },
      technologies: ['NQBA Core', 'Quantum Demand Prediction', 'Customer Analytics', 'Inventory AI'],
      testimonial: {
        quote: "NQBA's quantum demand forecasting has revolutionized our inventory management. We now predict customer needs with unprecedented accuracy.",
        author: "VP of Operations",
        company: "Global E-commerce Leader"
      }
    }
  ]

  const filteredCaseStudies = selectedCategory === 'all' 
    ? caseStudies 
    : caseStudies.filter(study => study.industry === selectedCategory)

  const featuredCaseStudies = caseStudies.filter(study => study.featured)

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
              <span className="text-gradient-cyan">Success</span> Stories
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Real-world quantum transformations delivering measurable business impact 
              across industries worldwide.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#case-studies" className="btn-primary">
                Explore Case Studies
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/contact" className="btn-secondary">
                Discuss Your Project
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Impact Overview */}
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
              Quantum Impact at Scale
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our clients achieve transformational results through quantum-powered business intelligence.
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
                metric: "$12.0B+",
                label: "Total Client Savings",
                description: "Across all implementations",
                icon: TrendingUp
              },
              {
                metric: "340%",
                label: "Average Improvement",
                description: "In key performance metrics",
                icon: Target
              },
              {
                metric: "206+",
                label: "Successful Projects",
                description: "Delivered globally",
                icon: Award
              },
              {
                metric: "98%",
                label: "Client Satisfaction",
                description: "Would recommend NQBA",
                icon: Star
              }
            ].map((stat) => (
              <motion.div
                key={stat.metric}
                variants={fadeInUp}
                className="card text-center group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-brand-cyan rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                  <stat.icon className="h-8 w-8 text-white" />
                </div>
                <div className="text-3xl md:text-4xl font-bold text-black mb-2">
                  {stat.metric}
                </div>
                <div className="font-medium text-black mb-1">{stat.label}</div>
                <div className="text-sm text-gray-500">{stat.description}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Featured Case Studies */}
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
              Featured Success Stories
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Dive deep into our most impactful quantum transformations.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="space-y-12"
          >
            {featuredCaseStudies.map((study, index) => {
              const Icon = study.icon
              return (
                <motion.div
                  key={study.id}
                  variants={fadeInUp}
                  className={`grid grid-cols-1 lg:grid-cols-2 gap-12 items-center ${
                    index % 2 === 1 ? 'lg:grid-flow-col-dense' : ''
                  }`}
                >
                  {/* Content */}
                  <div className={index % 2 === 1 ? 'lg:col-start-2' : ''}>
                    <div className="flex items-center space-x-3 mb-4">
                      <div className={`w-12 h-12 ${study.color} rounded-lg flex items-center justify-center`}>
                        <Icon className="h-6 w-6 text-white" />
                      </div>
                      <div>
                        <div className="text-sm font-medium text-brand-cyan">{study.client}</div>
                        <div className="text-xs text-gray-500">{study.location}</div>
                      </div>
                    </div>
                    <h3 className="text-2xl md:text-3xl font-bold text-black mb-4">
                      {study.title}
                    </h3>
                    <p className="text-gray-600 mb-6 leading-relaxed">
                      {study.challenge}
                    </p>
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      {Object.entries(study.metrics).slice(0, 4).map(([key, value]) => (
                        <div key={key} className="text-center">
                          <div className="text-2xl font-bold text-brand-cyan">{value}</div>
                          <div className="text-xs text-gray-500 capitalize">
                            {key.replace(/([A-Z])/g, ' $1').trim()}
                          </div>
                        </div>
                      ))}
                    </div>
                    <Link
                      href={`#${study.id}`}
                      className="inline-flex items-center text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200"
                    >
                      Read Full Case Study
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </Link>
                  </div>

                  {/* Visual/Stats */}
                  <div className={index % 2 === 1 ? 'lg:col-start-1' : ''}>
                    <div className="card bg-white">
                      <div className="text-center mb-6">
                        <div className={`w-20 h-20 ${study.color} rounded-full flex items-center justify-center mx-auto mb-4`}>
                          <Icon className="h-10 w-10 text-white" />
                        </div>
                        <h4 className="text-lg font-bold text-black">Key Results</h4>
                      </div>
                      <div className="space-y-4">
                        {study.results.slice(0, 3).map((result, idx) => (
                          <div key={idx} className="flex items-start space-x-3">
                            <CheckCircle className="h-5 w-5 text-brand-cyan mt-0.5 flex-shrink-0" />
                            <span className="text-sm text-gray-700">{result}</span>
                          </div>
                        ))}
                      </div>
                      <div className="mt-6 pt-6 border-t border-gray-200">
                        <div className="flex items-center justify-between text-sm text-gray-500">
                          <div className="flex items-center space-x-2">
                            <Clock className="h-4 w-4" />
                            <span>{study.duration}</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            <Users className="h-4 w-4" />
                            <span>{study.teamSize}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* All Case Studies */}
      <section id="case-studies" className="section-padding">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              All Case Studies
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Explore our complete portfolio of quantum transformation success stories.
            </p>
          </motion.div>

          {/* Category Filter */}
          <div className="flex flex-wrap gap-2 justify-center mb-12">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setSelectedCategory(category.id)}
                className={`px-4 py-2 rounded-lg transition-colors duration-200 ${
                  selectedCategory === category.id
                    ? 'bg-brand-cyan text-white'
                    : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
                }`}
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>

          {/* Case Studies Grid */}
          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {filteredCaseStudies.map((study) => {
              const Icon = study.icon
              return (
                <motion.div
                  key={study.id}
                  variants={fadeInUp}
                  className="card group hover:shadow-lg transition-shadow duration-200"
                >
                  {study.featured && (
                    <div className="absolute top-4 right-4">
                      <Star className="h-5 w-5 text-brand-gold fill-current" />
                    </div>
                  )}
                  <div className="flex items-center space-x-3 mb-4">
                    <div className={`w-12 h-12 ${study.color} rounded-lg flex items-center justify-center`}>
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <div className="text-sm font-medium text-brand-cyan">{study.client}</div>
                      <div className="text-xs text-gray-500">{study.location}</div>
                    </div>
                  </div>
                  <h3 className="text-lg font-bold text-black mb-3 group-hover:text-brand-cyan transition-colors duration-200">
                    {study.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                    {study.challenge.substring(0, 120)}...
                  </p>
                  <div className="grid grid-cols-2 gap-3 mb-4">
                    {Object.entries(study.metrics).slice(0, 2).map(([key, value]) => (
                      <div key={key} className="text-center">
                        <div className="text-lg font-bold text-brand-cyan">{value}</div>
                        <div className="text-xs text-gray-500 capitalize">
                          {key.replace(/([A-Z])/g, ' $1').trim()}
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="flex items-center justify-between text-xs text-gray-500 mb-4">
                    <div className="flex items-center space-x-2">
                      <Clock className="h-3 w-3" />
                      <span>{study.duration}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Users className="h-3 w-3" />
                      <span>{study.teamSize}</span>
                    </div>
                  </div>
                  <button className="w-full text-left text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200">
                    Read Case Study
                    <ArrowRight className="inline ml-2 h-4 w-4" />
                  </button>
                </motion.div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* Testimonials */}
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
              What Our Clients Say
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Hear directly from leaders who have transformed their organizations with quantum intelligence.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
          >
            {featuredCaseStudies.map((study) => (
              <motion.div
                key={study.id}
                variants={fadeInUp}
                className="card bg-white border-l-4 border-brand-cyan"
              >
                <div className="flex items-center space-x-1 mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="h-4 w-4 text-brand-gold fill-current" />
                  ))}
                </div>
                <blockquote className="text-gray-700 mb-6 leading-relaxed italic">
                  "{study.testimonial.quote}"
                </blockquote>
                <div className="border-t border-gray-200 pt-4">
                  <div className="font-semibold text-black">{study.testimonial.author}</div>
                  <div className="text-sm text-gray-500">{study.testimonial.company}</div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="section-padding">
        <div className="container-narrow text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Ready to Write Your Success Story?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join the quantum revolution and transform your business with measurable results.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/contact" className="btn-primary">
                Start Your Transformation
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
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