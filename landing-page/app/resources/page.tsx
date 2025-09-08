'use client'

import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Download, 
  ExternalLink, 
  FileText, 
  Video, 
  Code, 
  Users, 
  Calendar,
  ArrowRight,
  Star,
  Clock,
  Tag,
  Search,
  Filter
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'

export default function ResourcesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')

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
    { id: 'all', name: 'All Resources', count: 24 },
    { id: 'documentation', name: 'Documentation', count: 8 },
    { id: 'tutorials', name: 'Tutorials', count: 6 },
    { id: 'case-studies', name: 'Case Studies', count: 4 },
    { id: 'whitepapers', name: 'Whitepapers', count: 3 },
    { id: 'webinars', name: 'Webinars', count: 3 }
  ]

  const featuredResources = [
    {
      title: "QUBO Recipe Builder",
      description: "Interactive tool for creating quantum optimization recipes with visual drag-and-drop interface.",
      type: "Interactive Tool",
      category: "documentation",
      link: "/resources/recipes",
      featured: true,
      icon: Code,
      tags: ["Quantum", "QUBO", "Interactive", "Builder"]
    },
    {
      title: "NQBA Architecture Guide",
      description: "Complete guide to implementing the 5-layer quantum-native business architecture.",
      type: "Documentation",
      category: "documentation",
      link: "/resources/nqba-architecture",
      featured: true,
      icon: BookOpen,
      tags: ["Architecture", "NQBA", "Implementation"]
    },
    {
      title: "Quantum Business Intelligence Whitepaper",
      description: "Deep dive into quantum-powered business intelligence and its enterprise applications.",
      type: "Whitepaper",
      category: "whitepapers",
      link: "/resources/quantum-bi-whitepaper",
      featured: true,
      icon: FileText,
      tags: ["Quantum", "Business Intelligence", "Enterprise"]
    }
  ]

  const resources = [
    {
      title: "Getting Started with NQBA Core",
      description: "Step-by-step tutorial for setting up your first quantum business pipeline.",
      type: "Tutorial",
      category: "tutorials",
      duration: "15 min",
      difficulty: "Beginner",
      icon: Video,
      tags: ["Getting Started", "Tutorial", "NQBA"]
    },
    {
      title: "Quantum Optimization for Supply Chain",
      description: "Case study: How Goliath of All Trade optimized global supply chains with quantum computing.",
      type: "Case Study",
      category: "case-studies",
      duration: "8 min read",
      difficulty: "Intermediate",
      icon: FileText,
      tags: ["Supply Chain", "Optimization", "Case Study"]
    },
    {
      title: "API Reference Documentation",
      description: "Complete API documentation for NQBA Core platform integration.",
      type: "Documentation",
      category: "documentation",
      duration: "Reference",
      difficulty: "Advanced",
      icon: Code,
      tags: ["API", "Documentation", "Integration"]
    },
    {
      title: "Quantum Ethics and Compliance",
      description: "Understanding ethical AI and compliance requirements in quantum business applications.",
      type: "Whitepaper",
      category: "whitepapers",
      duration: "12 min read",
      difficulty: "Intermediate",
      icon: FileText,
      tags: ["Ethics", "Compliance", "AI"]
    },
    {
      title: "Building Your First AI Agent",
      description: "Hands-on tutorial for creating and deploying AI agents with NQBA Core.",
      type: "Tutorial",
      category: "tutorials",
      duration: "25 min",
      difficulty: "Intermediate",
      icon: Video,
      tags: ["AI Agents", "Tutorial", "Development"]
    },
    {
      title: "Sigma Select Lead Scoring Demo",
      description: "Live webinar demonstrating quantum-powered lead scoring for elite training programs.",
      type: "Webinar",
      category: "webinars",
      duration: "45 min",
      difficulty: "Beginner",
      icon: Video,
      tags: ["Lead Scoring", "Demo", "Sigma Select"]
    },
    {
      title: "Enterprise Security Best Practices",
      description: "Comprehensive guide to securing quantum business intelligence deployments.",
      type: "Documentation",
      category: "documentation",
      duration: "20 min read",
      difficulty: "Advanced",
      icon: BookOpen,
      tags: ["Security", "Enterprise", "Best Practices"]
    },
    {
      title: "Financial Services Quantum Transformation",
      description: "Case study: How a Fortune 500 bank transformed risk assessment with quantum computing.",
      type: "Case Study",
      category: "case-studies",
      duration: "10 min read",
      difficulty: "Intermediate",
      icon: FileText,
      tags: ["Financial Services", "Risk Assessment", "Transformation"]
    }
  ]

  const filteredResources = resources.filter(resource => {
    const matchesSearch = resource.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         resource.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         resource.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
    const matchesCategory = selectedCategory === 'all' || resource.category === selectedCategory
    return matchesSearch && matchesCategory
  })

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return 'bg-green-100 text-green-800'
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800'
      case 'Advanced': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
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
              <span className="text-gradient-cyan">Quantum</span> Resources
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Everything you need to master quantum business intelligence, from tutorials 
              to enterprise implementation guides.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/resources/recipes" className="btn-primary">
                Try QUBO Builder
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="#documentation" className="btn-secondary">
                Browse Documentation
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Featured Resources */}
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
              Featured Resources
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Start your quantum journey with our most popular and essential resources.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {featuredResources.map((resource) => (
              <motion.div
                key={resource.title}
                variants={fadeInUp}
                className="card-quantum group relative overflow-hidden"
              >
                <div className="absolute top-4 right-4">
                  <Star className="h-5 w-5 text-brand-gold fill-current" />
                </div>
                <div className="flex items-center space-x-3 mb-4">
                  <div className="w-12 h-12 bg-brand-cyan rounded-lg flex items-center justify-center">
                    <resource.icon className="h-6 w-6 text-white" />
                  </div>
                  <div>
                    <div className="text-sm font-medium text-brand-cyan">{resource.type}</div>
                  </div>
                </div>
                <h3 className="text-xl font-bold text-black mb-3 group-hover:text-brand-cyan transition-colors duration-200">
                  {resource.title}
                </h3>
                <p className="text-gray-600 mb-4 leading-relaxed">{resource.description}</p>
                <div className="flex flex-wrap gap-2 mb-6">
                  {resource.tags.map((tag) => (
                    <span key={tag} className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
                      {tag}
                    </span>
                  ))}
                </div>
                <Link
                  href={resource.link}
                  className="inline-flex items-center text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200"
                >
                  Access Resource
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Resource Library */}
      <section id="documentation" className="section-padding bg-gray-50">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Resource Library
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive collection of documentation, tutorials, and case studies.
            </p>
          </motion.div>

          {/* Search and Filter */}
          <div className="mb-12">
            <div className="flex flex-col lg:flex-row gap-6">
              {/* Search */}
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search resources..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent"
                  />
                </div>
              </div>

              {/* Category Filter */}
              <div className="lg:w-64">
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent"
                >
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name} ({category.count})
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Resource Grid */}
          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          >
            {filteredResources.map((resource) => (
              <motion.div
                key={resource.title}
                variants={fadeInUp}
                className="card group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2">
                    <resource.icon className="h-5 w-5 text-brand-cyan" />
                    <span className="text-sm font-medium text-brand-cyan">{resource.type}</span>
                  </div>
                  <span className={`text-xs px-2 py-1 rounded-full ${getDifficultyColor(resource.difficulty)}`}>
                    {resource.difficulty}
                  </span>
                </div>
                
                <h3 className="text-lg font-semibold text-black mb-2 group-hover:text-brand-cyan transition-colors duration-200">
                  {resource.title}
                </h3>
                
                <p className="text-gray-600 text-sm mb-4 leading-relaxed">
                  {resource.description}
                </p>
                
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-2 text-sm text-gray-500">
                    <Clock className="h-4 w-4" />
                    <span>{resource.duration}</span>
                  </div>
                </div>
                
                <div className="flex flex-wrap gap-1 mb-4">
                  {resource.tags.slice(0, 3).map((tag) => (
                    <span key={tag} className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
                      {tag}
                    </span>
                  ))}
                  {resource.tags.length > 3 && (
                    <span className="text-xs px-2 py-1 bg-gray-100 text-gray-600 rounded-full">
                      +{resource.tags.length - 3}
                    </span>
                  )}
                </div>
                
                <button className="w-full text-left text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200">
                  Access Resource
                  <ArrowRight className="inline ml-2 h-4 w-4" />
                </button>
              </motion.div>
            ))}
          </motion.div>

          {filteredResources.length === 0 && (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Search className="h-12 w-12 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">No resources found</h3>
              <p className="text-gray-600">Try adjusting your search terms or category filter.</p>
            </div>
          )}
        </div>
      </section>

      {/* Community & Support */}
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
              Community & Support
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Join our growing community of quantum business intelligence practitioners.
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
                title: "Developer Community",
                description: "Connect with other developers building quantum business applications.",
                icon: Users,
                link: "https://community.flyfox.ai",
                linkText: "Join Community"
              },
              {
                title: "Weekly Office Hours",
                description: "Get direct support from our quantum architects every Tuesday at 2 PM EST.",
                icon: Calendar,
                link: "/resources/office-hours",
                linkText: "Schedule Session"
              },
              {
                title: "Technical Support",
                description: "24/7 technical support for enterprise customers with SLA guarantees.",
                icon: ExternalLink,
                link: "/contact",
                linkText: "Contact Support"
              }
            ].map((item) => (
              <motion.div
                key={item.title}
                variants={fadeInUp}
                className="card text-center group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-brand-cyan rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                  <item.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-black mb-4">{item.title}</h3>
                <p className="text-gray-600 mb-6 leading-relaxed">{item.description}</p>
                <Link
                  href={item.link}
                  className="inline-flex items-center text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200"
                >
                  {item.linkText}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
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
              Ready to Build?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Start building quantum-powered business intelligence with our interactive QUBO Recipe Builder.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/resources/recipes" className="btn-primary">
                Launch QUBO Builder
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/contact" className="btn-secondary">
                Get Expert Help
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}