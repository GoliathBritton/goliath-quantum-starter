'use client'

import { motion } from 'framer-motion'
import { 
  Crown, 
  Star, 
  Globe, 
  Shield, 
  Zap, 
  Users, 
  ArrowRight, 
  CheckCircle, 
  ExternalLink,
  Cpu,
  Brain,
  Network,
  Target
} from 'lucide-react'
import { brand, partners, pricingTiers } from '../../lib/brand'
import Link from 'next/link'

export default function PartnersPage() {
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

  const getTierIcon = (tier: string) => {
    switch (tier) {
      case 'core': return Crown
      case 'strategic': return Star
      case 'ecosystem': return Globe
      default: return Network
    }
  }

  const getTierColor = (tier: string) => {
    switch (tier) {
      case 'core': return 'text-brand-gold'
      case 'strategic': return 'text-brand-cyan'
      case 'ecosystem': return 'text-black'
      default: return 'text-gray-600'
    }
  }

  const getTierBadgeColor = (tier: string) => {
    switch (tier) {
      case 'core': return 'bg-brand-gold text-black'
      case 'strategic': return 'bg-brand-cyan text-black'
      case 'ecosystem': return 'bg-white border border-gray-200 text-black'
      default: return 'bg-gray-100 text-gray-600'
    }
  }

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <section className="section-padding bg-white">
        <div className="container-quantum text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-5xl md:text-7xl font-bold text-black mb-6">
              Partner with the
              <span className="block text-gradient-cyan">
                Intelligence Economy
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-4xl mx-auto">
              Join our quantum-native ecosystem and unlock new revenue streams through NQBA Core integration.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="#partner-tiers" className="btn-primary">
                Explore Partnership
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="#white-label" className="btn-secondary">
                White-Label Solutions
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Partner Ecosystem */}
      <section className="section-padding bg-white border-t border-gray-200">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Strategic Partner Ecosystem
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our three-tier partnership model ensures optimal integration and mutual success.
            </p>
          </motion.div>

          {/* Partner Tiers */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            {['core', 'strategic', 'ecosystem'].map((tier) => {
              const tierPartners = partners.filter(p => p.tier === tier)
              const TierIcon = getTierIcon(tier)
              
              return (
                <motion.div
                  key={tier}
                  variants={fadeInUp}
                  initial="initial"
                  whileInView="animate"
                  viewport={{ once: true }}
                  className="card border-2 hover:shadow-lg transition-all duration-200"
                >
                  <div className="text-center mb-6">
                    <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full mb-4 ${getTierBadgeColor(tier)}`}>
                      <TierIcon className="h-8 w-8" />
                    </div>
                    <h3 className="text-2xl font-bold text-black mb-2 capitalize">{tier} Partners</h3>
                    <p className="text-gray-600 text-sm">
                      {tier === 'core' && 'Foundational quantum computing infrastructure'}
                      {tier === 'strategic' && 'Key technology and platform integrations'}
                      {tier === 'ecosystem' && 'Workflow automation and business applications'}
                    </p>
                  </div>
                  
                  <div className="space-y-3">
                    {tierPartners.map((partner) => (
                      <div key={partner.name} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg bg-white">
                        <div>
                          <div className="font-semibold text-black">{partner.name}</div>
                          <div className="text-xs text-gray-600 capitalize">{partner.type}</div>
                        </div>
                        <div className={`w-3 h-3 rounded-full ${tier === 'core' ? 'bg-brand-gold' : tier === 'strategic' ? 'bg-brand-cyan' : 'bg-gray-400'}`}></div>
                      </div>
                    ))}
                  </div>
                </motion.div>
              )
            })}
          </div>

          {/* Partner Details */}
          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-2 gap-8"
          >
            {partners.map((partner) => {
              const TierIcon = getTierIcon(partner.tier)
              
              return (
                <motion.div
                  key={partner.name}
                  variants={fadeInUp}
                  className="card hover:shadow-lg transition-shadow duration-200"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-xl font-semibold text-black mb-1">{partner.name}</h3>
                      <div className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getTierBadgeColor(partner.tier)}`}>
                        <TierIcon className="h-3 w-3 mr-1" />
                        {partner.tier}
                      </div>
                    </div>
                    <div className="text-xs text-gray-500 capitalize bg-gray-100 px-2 py-1 rounded">
                      {partner.type}
                    </div>
                  </div>
                  
                  <p className="text-gray-600 text-sm mb-4">{partner.description}</p>
                  
                  <div className="border-t border-gray-200 pt-4">
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
                      Integration
                    </div>
                    <p className="text-sm text-gray-600">{partner.integration}</p>
                  </div>
                </motion.div>
              )
            })}
          </motion.div>
        </div>
      </section>

      {/* Partnership Tiers & Pricing */}
      <section id="partner-tiers" className="section-padding bg-white border-t border-gray-200">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Partnership Tiers
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Choose the partnership level that aligns with your business goals and technical requirements.
            </p>
          </motion.div>

          <motion.div
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
          >
            {pricingTiers.map((tier, index) => (
              <motion.div
                key={tier.name}
                variants={fadeInUp}
                className={`card border-2 hover:shadow-lg transition-all duration-200 ${
                  tier.whiteLabel ? 'border-brand-gold bg-gradient-to-br from-white to-yellow-50' : 'border-gray-200'
                }`}
              >
                <div className="text-center mb-6">
                  {tier.whiteLabel && (
                    <div className="inline-flex items-center px-3 py-1 bg-brand-gold text-black text-xs font-semibold rounded-full mb-4">
                      <Crown className="h-3 w-3 mr-1" />
                      White-Label Ready
                    </div>
                  )}
                  <h3 className="text-2xl font-bold text-black mb-2">{tier.name}</h3>
                  <p className="text-gray-600 text-sm mb-4">{tier.description}</p>
                  <div className="text-3xl font-bold text-black">{tier.price}</div>
                </div>
                
                <ul className="space-y-3 mb-8">
                  {tier.features.map((feature) => (
                    <li key={feature} className="flex items-center text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-3 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
                
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">Quantum Access</span>
                    <div className={`w-3 h-3 rounded-full ${tier.quantumAccess ? 'bg-green-500' : 'bg-gray-300'}`}></div>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-600">White-Label</span>
                    <div className={`w-3 h-3 rounded-full ${tier.whiteLabel ? 'bg-brand-gold' : 'bg-gray-300'}`}></div>
                  </div>
                </div>
                
                <div className="mt-8">
                  <Link 
                    href={tier.whiteLabel ? "#white-label" : "/contact"}
                    className={tier.whiteLabel ? "btn-gold w-full text-center" : "btn-primary w-full text-center"}
                  >
                    {tier.whiteLabel ? 'Contact Sales' : 'Get Started'}
                  </Link>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* White-Label Capabilities */}
      <section id="white-label" className="section-padding bg-white border-t border-gray-200">
        <div className="container-quantum">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              White-Label Solutions
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Deploy NQBA Core under your brand with full customization and revenue sharing.
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
                title: "Custom Branding",
                description: "Full UI/UX customization with your brand colors, logos, and messaging",
                icon: Crown,
                features: ["Custom color schemes", "Logo integration", "Brand messaging", "Domain mapping"]
              },
              {
                title: "Dedicated Resources",
                description: "Isolated quantum computing resources and dedicated support team",
                icon: Shield,
                features: ["Private quantum nodes", "Dedicated support", "SLA guarantees", "Priority access"]
              },
              {
                title: "Revenue Sharing",
                description: "Transparent revenue sharing model with detailed analytics and reporting",
                icon: Target,
                features: ["Revenue analytics", "Usage tracking", "Billing integration", "Partner dashboard"]
              },
              {
                title: "Custom Logic",
                description: "Implement your business rules and workflows within the NQBA framework",
                icon: Brain,
                features: ["Custom algorithms", "Business rules", "Workflow automation", "API extensions"]
              }
            ].map((capability) => (
              <motion.div
                key={capability.title}
                variants={fadeInUp}
                className="card hover:shadow-lg transition-shadow duration-200"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-lg bg-brand-gold mb-4">
                  <capability.icon className="h-6 w-6 text-black" />
                </div>
                <h3 className="text-xl font-semibold text-black mb-3">{capability.title}</h3>
                <p className="text-gray-600 text-sm mb-4">{capability.description}</p>
                <ul className="space-y-2">
                  {capability.features.map((feature) => (
                    <li key={feature} className="flex items-center text-sm text-gray-600">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding bg-white border-t border-gray-200">
        <div className="container-narrow text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-black mb-6">
              Ready to Partner with Us?
            </h2>
            <p className="text-xl text-gray-600 mb-8">
              Join the quantum-native ecosystem and unlock new possibilities for your business.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a
                href="mailto:partners@flyfox.ai?subject=Partnership%20Inquiry&body=Hi,%20I'm%20interested%20in%20exploring%20a%20partnership%20with%20FLYFOX%20AI."
                className="btn-primary"
              >
                Contact Partnership Team
                <ArrowRight className="ml-2 h-5 w-5" />
              </a>
              <Link href="/resources" className="btn-secondary">
                Technical Documentation
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  )
}