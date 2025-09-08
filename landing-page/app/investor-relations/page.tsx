'use client'

import { motion } from 'framer-motion'
import { 
  TrendingUp, 
  DollarSign, 
  Users, 
  Globe, 
  Calendar, 
  Download, 
  ExternalLink, 
  ArrowRight,
  BarChart3,
  PieChart,
  Target,
  Award,
  Building,
  Briefcase
} from 'lucide-react'
import Link from 'next/link'
import { BUSINESS_UNITS, STRATEGIC_PARTNERS } from '@/lib/brand'

export default function InvestorRelationsPage() {
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

  const financialHighlights = [
    {
      metric: "Revenue Growth",
      value: "340%",
      period: "YoY 2024",
      trend: "up",
      icon: TrendingUp
    },
    {
      metric: "Enterprise Clients",
      value: "150+",
      period: "Active",
      trend: "up",
      icon: Building
    },
    {
      metric: "Quantum Transactions",
      value: "2.4M",
      period: "Monthly",
      trend: "up",
      icon: Target
    },
    {
      metric: "Market Valuation",
      value: "$1.2B",
      period: "Series C",
      trend: "up",
      icon: DollarSign
    }
  ]

  const businessUnits = [
    {
      name: "FLYFOX AI",
      description: "Core quantum business intelligence platform",
      revenue: "$45M ARR",
      growth: "+280%",
      marketShare: "Leading position in quantum BI"
    },
    {
      name: "Goliath of All Trade",
      description: "Capital, Energy, and Insurance optimization",
      revenue: "$78M ARR",
      growth: "+420%",
      marketShare: "#1 in quantum financial optimization"
    },
    {
      name: "Sigma Select",
      description: "Elite training and certification programs",
      revenue: "$12M ARR",
      growth: "+190%",
      marketShare: "Premium quantum education leader"
    }
  ]

  const milestones = [
    {
      date: "Q4 2024",
      title: "Series C Funding",
      description: "$150M Series C led by Quantum Ventures, achieving $1.2B valuation",
      type: "funding"
    },
    {
      date: "Q3 2024",
      title: "Dynex Partnership",
      description: "Strategic partnership with Dynex for quantum computing infrastructure",
      type: "partnership"
    },
    {
      date: "Q2 2024",
      title: "Enterprise Milestone",
      description: "Reached 150+ enterprise clients across Fortune 500 companies",
      type: "business"
    },
    {
      date: "Q1 2024",
      title: "NQBA Platform Launch",
      description: "Launched NQBA Core platform with 5-layer quantum architecture",
      type: "product"
    },
    {
      date: "Q4 2023",
      title: "Series B Completion",
      description: "$75M Series B funding round with strategic investors",
      type: "funding"
    },
    {
      date: "Q2 2023",
      title: "Quantum High Council",
      description: "Established Quantum High Council governance framework",
      type: "governance"
    }
  ]

  const reports = [
    {
      title: "Q4 2024 Earnings Report",
      date: "March 15, 2025",
      type: "Quarterly Report",
      size: "2.4 MB",
      format: "PDF"
    },
    {
      title: "Annual Report 2024",
      date: "February 28, 2025",
      type: "Annual Report",
      size: "8.7 MB",
      format: "PDF"
    },
    {
      title: "Quantum Market Analysis",
      date: "January 20, 2025",
      type: "Market Research",
      size: "3.1 MB",
      format: "PDF"
    },
    {
      title: "ESG Impact Report 2024",
      date: "December 15, 2024",
      type: "Sustainability",
      size: "4.2 MB",
      format: "PDF"
    }
  ]

  const upcomingEvents = [
    {
      date: "April 15, 2025",
      time: "2:00 PM EST",
      title: "Q1 2025 Earnings Call",
      type: "Earnings Call",
      location: "Virtual"
    },
    {
      date: "May 20, 2025",
      time: "10:00 AM EST",
      title: "Quantum Computing Summit",
      type: "Conference",
      location: "San Francisco, CA"
    },
    {
      date: "June 10, 2025",
      time: "1:00 PM EST",
      title: "Annual Shareholder Meeting",
      type: "Shareholder Meeting",
      location: "New York, NY"
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
              <span className="text-gradient-cyan">Investor</span> Relations
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Leading the quantum revolution in business intelligence with transparent 
              governance and exceptional growth.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#financials" className="btn-primary">
                View Financials
                <BarChart3 className="ml-2 h-5 w-5" />
              </Link>
              <Link href="#reports" className="btn-secondary">
                Download Reports
                <Download className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Financial Highlights */}
      <section id="financials" className="section-padding">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Financial Highlights
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Strong financial performance driven by quantum innovation and market leadership.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-16"
          >
            {financialHighlights.map((highlight) => (
              <motion.div
                key={highlight.metric}
                variants={fadeInUp}
                className="card text-center group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="w-16 h-16 bg-brand-cyan rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
                  <highlight.icon className="h-8 w-8 text-white" />
                </div>
                <div className="text-3xl md:text-4xl font-bold text-black mb-2">
                  {highlight.value}
                </div>
                <div className="text-sm text-gray-500 mb-1">{highlight.period}</div>
                <div className="font-medium text-black">{highlight.metric}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Business Units Performance */}
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
              Business Unit Performance
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our diversified portfolio of quantum business intelligence solutions.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8"
          >
            {businessUnits.map((unit) => (
              <motion.div
                key={unit.name}
                variants={fadeInUp}
                className="card group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-black group-hover:text-brand-cyan transition-colors duration-200">
                    {unit.name}
                  </h3>
                  <div className="text-2xl font-bold text-brand-cyan">
                    {unit.growth}
                  </div>
                </div>
                <p className="text-gray-600 mb-4 leading-relaxed">{unit.description}</p>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Annual Recurring Revenue</span>
                    <span className="font-semibold text-black">{unit.revenue}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">Market Position</span>
                    <span className="font-semibold text-black">{unit.marketShare}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Company Milestones */}
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
              Company Milestones
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Key achievements in our journey to quantum business intelligence leadership.
            </p>
          </motion.div>

          <div className="max-w-4xl mx-auto">
            <div className="relative">
              {/* Timeline line */}
              <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-brand-cyan"></div>
              
              <motion.div
                variants={staggerContainer}
                initial="initial"
                whileInView="animate"
                viewport={{ once: true }}
                className="space-y-8"
              >
                {milestones.map((milestone, index) => (
                  <motion.div
                    key={index}
                    variants={fadeInUp}
                    className="relative flex items-start space-x-6"
                  >
                    <div className="w-16 h-16 bg-brand-cyan rounded-full flex items-center justify-center text-white font-bold text-sm z-10">
                      {milestone.date.split(' ')[0]}
                    </div>
                    <div className="flex-1 card">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="text-lg font-bold text-black">{milestone.title}</h3>
                        <span className="text-sm text-gray-500">{milestone.date}</span>
                      </div>
                      <p className="text-gray-600 leading-relaxed">{milestone.description}</p>
                    </div>
                  </motion.div>
                ))}
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* Reports & Documents */}
      <section id="reports" className="section-padding bg-gray-50">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Reports & Documents
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Access our latest financial reports, market analysis, and corporate documents.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {reports.map((report) => (
              <motion.div
                key={report.title}
                variants={fadeInUp}
                className="card group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="w-12 h-12 bg-brand-cyan rounded-lg flex items-center justify-center">
                      <Download className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-black group-hover:text-brand-cyan transition-colors duration-200">
                        {report.title}
                      </h3>
                      <div className="text-sm text-gray-500">{report.type}</div>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                  <span>{report.date}</span>
                  <span>{report.format} • {report.size}</span>
                </div>
                <button className="w-full btn-secondary text-sm">
                  Download Report
                  <Download className="ml-2 h-4 w-4" />
                </button>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Upcoming Events */}
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
              Upcoming Events
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Join us for earnings calls, investor meetings, and industry conferences.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="max-w-4xl mx-auto space-y-6"
          >
            {upcomingEvents.map((event, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="card group hover:shadow-lg transition-shadow duration-200"
              >
                <div className="flex flex-col md:flex-row md:items-center md:justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <Calendar className="h-5 w-5 text-brand-cyan" />
                      <span className="text-sm font-medium text-brand-cyan">{event.type}</span>
                    </div>
                    <h3 className="text-lg font-bold text-black mb-2 group-hover:text-brand-cyan transition-colors duration-200">
                      {event.title}
                    </h3>
                    <div className="flex flex-col sm:flex-row sm:items-center sm:space-x-6 text-sm text-gray-600">
                      <div className="flex items-center space-x-2">
                        <Calendar className="h-4 w-4" />
                        <span>{event.date} at {event.time}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Globe className="h-4 w-4" />
                        <span>{event.location}</span>
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 md:mt-0">
                    <button className="btn-primary">
                      Register
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Contact Investor Relations */}
      <section className="section-padding bg-gray-50">
        <div className="container-narrow text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Investor Relations Contact
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Have questions about our financial performance or investment opportunities?
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="mailto:investors@flyfox.ai" className="btn-primary">
                Contact IR Team
                <ExternalLink className="ml-2 h-5 w-5" />
              </Link>
              <a href="https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8" className="btn-secondary" target="_blank" rel="noopener noreferrer">
                Schedule Meeting
              </a>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}