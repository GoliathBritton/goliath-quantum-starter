'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'
import { 
  Mail, 
  Phone, 
  MapPin, 
  Linkedin, 
  Twitter, 
  Github,
  ExternalLink,
  Shield,
  Zap,
  Crown
} from 'lucide-react'
import { brand, navigation, partners as strategicPartners, businessUnits } from '../lib/brand'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 }
  }

  return (
    <footer className="bg-brand-navy text-white">
      {/* Main Footer Content */}
      <div className="container-quantum py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand & Description */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="lg:col-span-1"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-12 h-12 rounded-lg overflow-hidden bg-white p-1">
                <img 
                  src="/logos/flyfox-logo.png" 
                  alt="FLYFOX AI Logo"
                  className="w-full h-full object-contain"
                />
              </div>
              <div>
                <div className="font-bold text-xl">{brand.name}</div>
                <div className="text-sm text-gray-300">Powered by NQBA</div>
              </div>
            </div>
            <p className="text-gray-300 text-sm mb-6 leading-relaxed">
              {brand.description}
            </p>
            <div className="flex space-x-4">
              <a
                href="https://linkedin.com/company/flyfox-ai"
                className="text-gray-400 hover:text-brand-cyan transition-colors duration-200"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Linkedin className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com/flyfox_ai"
                className="text-gray-400 hover:text-brand-cyan transition-colors duration-200"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="https://github.com/flyfox-ai"
                className="text-gray-400 hover:text-brand-cyan transition-colors duration-200"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="h-5 w-5" />
              </a>
            </div>
          </motion.div>

          {/* Navigation Links */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            viewport={{ once: true }}
          >
            <h3 className="font-semibold text-lg mb-4">Platform</h3>
            <ul className="space-y-3">
              {navigation.main.slice(0, 6).map((item) => (
                <li key={item.path}>
                  <Link
                    href={item.path}
                    className="text-gray-300 hover:text-brand-cyan transition-colors duration-200 text-sm"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Business Units */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
          >
            <h3 className="font-semibold text-lg mb-4">Intelligence Economy</h3>
            <ul className="space-y-3">
              {businessUnits.map((unit) => (
                <li key={unit.name} className="flex items-center space-x-2">
                  <span className="text-lg">{unit.icon}</span>
                  <div>
                    <div className="text-sm font-medium text-white">{unit.name}</div>
                    <div className="text-xs text-gray-400">{unit.focus}</div>
                  </div>
                </li>
              ))}
            </ul>
          </motion.div>

          {/* Contact & Support */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            viewport={{ once: true }}
          >
            <h3 className="font-semibold text-lg mb-4">Contact</h3>
            <ul className="space-y-3">
              <li className="flex items-center space-x-3">
                <Mail className="h-4 w-4 text-brand-cyan flex-shrink-0" />
                <a
                  href="mailto:hello@flyfox.ai"
                  className="text-gray-300 hover:text-brand-cyan transition-colors duration-200 text-sm"
                >
                  hello@flyfox.ai
                </a>
              </li>
              <li className="flex items-center space-x-3">
                <Phone className="h-4 w-4 text-brand-cyan flex-shrink-0" />
                <a
                  href="tel:517-213-8392"
                  className="text-gray-300 hover:text-brand-cyan transition-colors duration-200 text-sm"
                >
                  (517) 213-8392
                </a>
              </li>
              <li className="flex items-start space-x-3">
                <MapPin className="h-4 w-4 text-brand-cyan flex-shrink-0 mt-0.5" />
                <div className="text-gray-300 text-sm">
                  <div>Quantum Computing Center</div>
                  <div>Silicon Valley, CA</div>
                </div>
              </li>
            </ul>
            
            <div className="mt-6">
              <a
                href="https://live.flyfoxai.com/widget/booking/BJV7BainocNCHj2XDtt8"
                className="inline-flex items-center space-x-2 text-sm font-medium text-brand-cyan hover:text-brand-gold transition-colors duration-200"
                target="_blank"
                rel="noopener noreferrer"
              >
                <span>Book a Demo</span>
                <ExternalLink className="h-4 w-4" />
              </a>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Strategic Partners Section */}
      <div className="border-t border-gray-700">
        <div className="container-quantum py-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="text-center mb-6"
          >
            <h3 className="font-semibold text-lg mb-2">Strategic Partners</h3>
            <p className="text-gray-400 text-sm">
              Powered by industry-leading quantum and AI infrastructure
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-7 gap-6 items-center"
          >
            {strategicPartners.map((partner) => (
              <div
                key={partner.name}
                className="flex flex-col items-center space-y-2 group"
              >
                <div className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center group-hover:bg-gray-700 transition-colors duration-200">
                  <span className="text-2xl">{partner.icon}</span>
                </div>
                <div className="text-center">
                  <div className="text-sm font-medium text-white group-hover:text-brand-cyan transition-colors duration-200">
                    {partner.name}
                  </div>
                  <div className="text-xs text-gray-400">{partner.category}</div>
                </div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Bottom Bar */}
      <div className="border-t border-gray-700">
        <div className="container-quantum py-6">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex flex-col md:flex-row items-center space-y-2 md:space-y-0 md:space-x-6">
              <p className="text-gray-400 text-sm">
                © {currentYear} {brand.name}. All rights reserved.
              </p>
              <div className="flex items-center space-x-4 text-xs">
                <Link
                  href="/privacy"
                  className="text-gray-400 hover:text-brand-cyan transition-colors duration-200"
                >
                  Privacy Policy
                </Link>
                <Link
                  href="/terms"
                  className="text-gray-400 hover:text-brand-cyan transition-colors duration-200"
                >
                  Terms of Service
                </Link>
                <Link
                  href="/security"
                  className="text-gray-400 hover:text-brand-cyan transition-colors duration-200"
                >
                  Security
                </Link>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 px-3 py-1 bg-gray-800 rounded-full">
                <Shield className="h-3 w-3 text-green-400" />
                <span className="text-xs font-medium text-gray-300">SOC 2 Compliant</span>
              </div>
              <div className="flex items-center space-x-2 px-3 py-1 bg-gray-800 rounded-full">
                <Zap className="h-3 w-3 text-brand-cyan" />
                <span className="text-xs font-medium text-gray-300">Quantum Ready</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  )
}