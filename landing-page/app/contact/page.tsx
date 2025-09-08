'use client'

import { motion } from 'framer-motion'
import { 
  Mail, 
  Phone, 
  MapPin, 
  Clock, 
  Send, 
  ArrowRight, 
  Building2, 
  Users, 
  Zap, 
  Shield, 
  Globe, 
  Calendar,
  MessageSquare,
  CheckCircle,
  Star,
  Linkedin,
  Twitter,
  Youtube,
  Github
} from 'lucide-react'
import Link from 'next/link'
import { useState } from 'react'
import { businessUnits, strategicPartners } from '@/lib/brand'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    company: '',
    role: '',
    businessUnit: '',
    inquiryType: '',
    projectTimeline: '',
    budget: '',
    message: '',
    newsletter: false
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

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

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)
    
    // Simulate form submission
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    setIsSubmitting(false)
    setIsSubmitted(true)
  }

  const inquiryTypes = [
    { value: 'quantum-consulting', label: 'Quantum Computing Consulting' },
    { value: 'nqba-implementation', label: 'NQBA Platform Implementation' },
    { value: 'ai-integration', label: 'AI/ML Integration Services' },
    { value: 'partnership', label: 'Strategic Partnership' },
    { value: 'investment', label: 'Investment Opportunities' },
    { value: 'media', label: 'Media & Press Inquiries' },
    { value: 'support', label: 'Technical Support' },
    { value: 'other', label: 'Other' }
  ]

  const projectTimelines = [
    { value: 'immediate', label: 'Immediate (< 1 month)' },
    { value: 'short-term', label: 'Short-term (1-3 months)' },
    { value: 'medium-term', label: 'Medium-term (3-6 months)' },
    { value: 'long-term', label: 'Long-term (6+ months)' },
    { value: 'planning', label: 'Planning Phase' }
  ]

  const budgetRanges = [
    { value: 'under-100k', label: 'Under $100K' },
    { value: '100k-500k', label: '$100K - $500K' },
    { value: '500k-1m', label: '$500K - $1M' },
    { value: '1m-5m', label: '$1M - $5M' },
    { value: 'over-5m', label: 'Over $5M' },
    { value: 'discuss', label: 'Prefer to Discuss' }
  ]

  const offices = [
    {
      name: 'Global Headquarters',
      location: 'New York, USA',
      address: '1 World Trade Center\nSuite 8500\nNew York, NY 10007',
      phone: '(517) 213-8392',
      email: 'john.britton@goliathomniedge.com',
      timezone: 'EST (UTC-5)',
      hours: 'Mon-Fri: 9:00 AM - 6:00 PM'
    },
    {
      name: 'Quantum Research Center',
      location: 'Palo Alto, USA',
      address: '3000 Sand Hill Road\nBuilding 4, Suite 150\nMenlo Park, CA 94025',
      phone: '+1 (555) 234-5678',
      email: 'research@flyfoxai.com',
      timezone: 'PST (UTC-8)',
      hours: 'Mon-Fri: 8:00 AM - 7:00 PM'
    },
    {
      name: 'European Operations',
      location: 'London, UK',
      address: '1 Canada Square\nLevel 42\nLondon E14 5AB',
      phone: '+44 20 7946 0958',
      email: 'europe@flyfoxai.com',
      timezone: 'GMT (UTC+0)',
      hours: 'Mon-Fri: 9:00 AM - 5:00 PM'
    },
    {
      name: 'Asia-Pacific Hub',
      location: 'Singapore',
      address: '1 Raffles Place\n#40-02 One Raffles Place\nSingapore 048616',
      phone: '+65 6532 4567',
      email: 'apac@flyfoxai.com',
      timezone: 'SGT (UTC+8)',
      hours: 'Mon-Fri: 9:00 AM - 6:00 PM'
    }
  ]

  const socialLinks = [
    { icon: Linkedin, href: 'https://linkedin.com/company/flyfox-ai', label: 'LinkedIn' },
    { icon: Twitter, href: 'https://twitter.com/flyfoxai', label: 'Twitter' },
    { icon: Youtube, href: 'https://youtube.com/@flyfoxai', label: 'YouTube' },
    { icon: Github, href: 'https://github.com/flyfox-ai', label: 'GitHub' }
  ]

  if (isSubmitted) {
    return (
      <div className="bg-white min-h-screen flex items-center justify-center">
        <div className="container-narrow text-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8 }}
          >
            <div className="w-20 h-20 bg-brand-cyan rounded-full flex items-center justify-center mx-auto mb-8">
              <CheckCircle className="h-10 w-10 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Thank You!
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Your message has been received. Our quantum intelligence team will review your inquiry and respond within 24 hours.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/" className="btn-primary">
                Return Home
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/resources" className="btn-secondary">
                Explore Resources
              </Link>
            </div>
          </motion.div>
        </div>
      </div>
    )
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
              <span className="text-gradient-cyan">Connect</span> with Us
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Ready to transform your business with quantum intelligence? 
              Let's discuss your quantum transformation journey.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#contact-form" className="btn-primary">
                Start Conversation
                <MessageSquare className="ml-2 h-5 w-5" />
              </Link>
              <Link href="#offices" className="btn-secondary">
                Find Our Offices
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Quick Contact Options */}
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
              Get in Touch
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Multiple ways to connect with our quantum intelligence experts.
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
                icon: MessageSquare,
                title: 'Start a Conversation',
                description: 'Fill out our contact form for detailed inquiries',
                action: 'Contact Form',
                href: '#contact-form',
                color: 'bg-brand-cyan'
              },
              {
                icon: Calendar,
                title: 'Schedule a Demo',
                description: 'Book a personalized NQBA platform demonstration',
                action: 'Book Demo',
                href: 'https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8',
                color: 'bg-brand-gold'
              },
              {
                icon: Phone,
                title: 'Speak with Expert',
                description: 'Direct line to our quantum consulting team',
                action: 'Call Now',
                href: 'tel:517-213-8392',
                color: 'bg-brand-navy'
              },
              {
                icon: Mail,
                title: 'Email Us',
                description: 'Send us your questions and requirements',
                action: 'Send Email',
                href: 'mailto:contact@flyfoxai.com',
                color: 'bg-gray-600'
              }
            ].map((option) => (
              <motion.div
                key={option.title}
                variants={fadeInUp}
                className="card text-center group hover:shadow-lg transition-shadow duration-200"
              >
                <div className={`w-16 h-16 ${option.color} rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200`}>
                  <option.icon className="h-8 w-8 text-white" />
                </div>
                <h3 className="text-xl font-bold text-black mb-3">{option.title}</h3>
                <p className="text-gray-600 mb-6">{option.description}</p>
                <Link
                  href={option.href}
                  className="inline-flex items-center text-brand-cyan font-medium hover:text-brand-gold transition-colors duration-200"
                >
                  {option.action}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Contact Form */}
      <section id="contact-form" className="section-padding bg-gray-50">
        <div className="container-quantum">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">
            {/* Form */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-black mb-6">
                Tell Us About Your Project
              </h2>
              <p className="text-gray-600 mb-8">
                Share your quantum transformation goals and we'll connect you with the right experts.
              </p>

              <form onSubmit={handleSubmit} className="space-y-6">
                {/* Personal Information */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-black mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                      placeholder="John"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-black mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                      placeholder="Doe"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-black mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                    placeholder="john.britton@goliathomniedge.com"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-black mb-2">
                      Company *
                    </label>
                    <input
                      type="text"
                      name="company"
                      value={formData.company}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                      placeholder="Your Company"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-black mb-2">
                      Role *
                    </label>
                    <input
                      type="text"
                      name="role"
                      value={formData.role}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                      placeholder="Chief Technology Officer"
                    />
                  </div>
                </div>

                {/* Business Interest */}
                <div>
                  <label className="block text-sm font-medium text-black mb-2">
                    Business Unit of Interest
                  </label>
                  <select
                    name="businessUnit"
                    value={formData.businessUnit}
                    onChange={handleInputChange}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                  >
                    <option value="">Select a business unit</option>
                    {businessUnits.map((unit) => (
                      <option key={unit.id} value={unit.id}>
                        {unit.name} - {unit.description}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-black mb-2">
                    Inquiry Type *
                  </label>
                  <select
                    name="inquiryType"
                    value={formData.inquiryType}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                  >
                    <option value="">Select inquiry type</option>
                    {inquiryTypes.map((type) => (
                      <option key={type.value} value={type.value}>
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-black mb-2">
                      Project Timeline
                    </label>
                    <select
                      name="projectTimeline"
                      value={formData.projectTimeline}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                    >
                      <option value="">Select timeline</option>
                      {projectTimelines.map((timeline) => (
                        <option key={timeline.value} value={timeline.value}>
                          {timeline.label}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-black mb-2">
                      Budget Range
                    </label>
                    <select
                      name="budget"
                      value={formData.budget}
                      onChange={handleInputChange}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200"
                    >
                      <option value="">Select budget range</option>
                      {budgetRanges.map((range) => (
                        <option key={range.value} value={range.value}>
                          {range.label}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-black mb-2">
                    Project Details *
                  </label>
                  <textarea
                    name="message"
                    value={formData.message}
                    onChange={handleInputChange}
                    required
                    rows={6}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-cyan focus:border-transparent transition-colors duration-200 resize-none"
                    placeholder="Tell us about your quantum transformation goals, current challenges, and how we can help..."
                  />
                </div>

                <div className="flex items-start space-x-3">
                  <input
                    type="checkbox"
                    name="newsletter"
                    checked={formData.newsletter}
                    onChange={handleInputChange}
                    className="mt-1 h-4 w-4 text-brand-cyan focus:ring-brand-cyan border-gray-300 rounded"
                  />
                  <label className="text-sm text-gray-600">
                    Subscribe to our newsletter for quantum computing insights and NQBA platform updates
                  </label>
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isSubmitting ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                      Sending Message...
                    </>
                  ) : (
                    <>
                      Send Message
                      <Send className="ml-2 h-5 w-5" />
                    </>
                  )}
                </button>
              </form>
            </motion.div>

            {/* Contact Information */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              viewport={{ once: true }}
              className="space-y-8"
            >
              <div>
                <h3 className="text-2xl font-bold text-black mb-6">Why Choose FLYFOX AI?</h3>
                <div className="space-y-4">
                  {[
                    {
                      icon: Zap,
                      title: 'Quantum Advantage',
                      description: 'Leverage true quantum computing power for exponential performance gains'
                    },
                    {
                      icon: Shield,
                      title: 'Enterprise Security',
                      description: 'Bank-grade security with quantum-resistant encryption protocols'
                    },
                    {
                      icon: Users,
                      title: 'Expert Team',
                      description: 'World-class quantum scientists and AI engineers at your service'
                    },
                    {
                      icon: Globe,
                      title: 'Global Reach',
                      description: 'Offices worldwide with 24/7 support for enterprise clients'
                    }
                  ].map((benefit) => (
                    <div key={benefit.title} className="flex items-start space-x-4">
                      <div className="w-10 h-10 bg-brand-cyan rounded-lg flex items-center justify-center flex-shrink-0">
                        <benefit.icon className="h-5 w-5 text-white" />
                      </div>
                      <div>
                        <h4 className="font-semibold text-black mb-1">{benefit.title}</h4>
                        <p className="text-gray-600 text-sm">{benefit.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card bg-white">
                <h4 className="text-lg font-bold text-black mb-4">Strategic Partners</h4>
                <div className="grid grid-cols-2 gap-4">
                  {strategicPartners.slice(0, 6).map((partner) => (
                    <div key={partner.name} className="text-center">
                      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-2">
                        <span className="text-xs font-bold text-gray-600">
                          {partner.name.substring(0, 2).toUpperCase()}
                        </span>
                      </div>
                      <div className="text-xs text-gray-600">{partner.name}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card bg-white">
                <h4 className="text-lg font-bold text-black mb-4">Follow Us</h4>
                <div className="flex space-x-4">
                  {socialLinks.map((social) => (
                    <Link
                      key={social.label}
                      href={social.href}
                      className="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center hover:bg-brand-cyan hover:text-white transition-colors duration-200"
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      <social.icon className="h-5 w-5" />
                    </Link>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Office Locations */}
      <section id="offices" className="section-padding">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Global Presence
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Connect with our quantum intelligence experts across four continents.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          >
            {offices.map((office) => (
              <motion.div
                key={office.name}
                variants={fadeInUp}
                className="card group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-12 h-12 bg-brand-cyan rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200">
                  <Building2 className="h-6 w-6 text-white" />
                </div>
                <h3 className="text-lg font-bold text-black mb-2">{office.name}</h3>
                <div className="text-brand-cyan font-medium mb-4">{office.location}</div>
                
                <div className="space-y-3 text-sm text-gray-600">
                  <div className="flex items-start space-x-2">
                    <MapPin className="h-4 w-4 mt-0.5 flex-shrink-0" />
                    <div className="whitespace-pre-line">{office.address}</div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Phone className="h-4 w-4 flex-shrink-0" />
                    <Link href={`tel:${office.phone}`} className="hover:text-brand-cyan transition-colors duration-200">
                      {office.phone}
                    </Link>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4 flex-shrink-0" />
                    <Link href={`mailto:${office.email}`} className="hover:text-brand-cyan transition-colors duration-200">
                      {office.email}
                    </Link>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4 flex-shrink-0" />
                    <div>
                      <div>{office.hours}</div>
                      <div className="text-xs text-gray-500">{office.timezone}</div>
                    </div>
                  </div>
                </div>
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
              Ready to Transform Your Business?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join the quantum revolution and unlock exponential business growth.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/resources/recipes" className="btn-primary">
                Try QUBO Builder
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/case-studies" className="btn-secondary">
                View Success Stories
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}