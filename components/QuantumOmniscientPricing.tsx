import React, { useState } from 'react';
import { motion } from 'framer-motion';

interface PricingTier {
  name: string;
  price: string;
  originalPrice?: string;
  description: string;
  features: string[];
  highlight?: boolean;
  premium?: boolean;
  quantum?: boolean;
  cta: string;
  badge?: string;
}

const pricingTiers: PricingTier[] = [
  {
    name: "Core Intelligence",
    price: "$297",
    originalPrice: "$49",
    description: "Essential quantum-enhanced business intelligence",
    features: [
      "Basic NQBA Framework Access",
      "Standard qdLLM Processing",
      "5 Quantum Queries/month",
      "Email Support",
      "Basic Analytics Dashboard",
      "Standard API Access"
    ],
    cta: "Start Your Quantum Journey",
    badge: "600% Value Increase"
  },
  {
    name: "Premium Omniscient",
    price: "$897",
    originalPrice: "$149",
    description: "Advanced quantum foresight with predictive capabilities",
    features: [
      "Full NQBA Framework",
      "Advanced qdLLM + QNLP",
      "50 Quantum Queries/month",
      "Priority Support",
      "Advanced Analytics + Insights",
      "Custom Workflow Builder",
      "Quantum Attention Mechanisms",
      "Real-time Decision Support"
    ],
    highlight: true,
    cta: "Unlock Quantum Advantage",
    badge: "Most Popular"
  },
  {
    name: "Elite Quantum",
    price: "$2,997",
    originalPrice: "$499",
    description: "Enterprise-grade quantum intelligence with unlimited access",
    features: [
      "Complete Quantum Suite",
      "Unlimited Quantum Queries",
      "Dedicated Quantum Consultant",
      "Custom Model Training",
      "White-label Solutions",
      "Advanced Governance & Compliance",
      "Multi-tenant Architecture",
      "24/7 Premium Support",
      "Custom Integrations"
    ],
    premium: true,
    cta: "Dominate Your Market",
    badge: "Enterprise Ready"
  },
  {
    name: "Quantum Omniscient™ Black-Box",
    price: "$9,997",
    originalPrice: "$1,666",
    description: "The ultimate quantum foresight engine - mystical, powerful, inevitable",
    features: [
      "Quantum Black-Box™ Access",
      "Prophetic Market Predictions",
      "Auto-execution Agents",
      "Quantum Coherence Optimization",
      "Dynex Neuromorphic Computing",
      "Unlimited Everything",
      "Personal Quantum Oracle",
      "Reality Simulation Engine",
      "Quantum Entanglement Analytics",
      "The Singularity Chamber Access"
    ],
    quantum: true,
    cta: "Transcend Reality",
    badge: "Quantum Supremacy"
  }
];

const QuantumOmniscientPricing: React.FC = () => {
  const [selectedTier, setSelectedTier] = useState<string>('Premium Omniscient');
  const [isAnnual, setIsAnnual] = useState(true);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const cardVariants = {
    hidden: { y: 50, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 100
      }
    }
  };

  const getCardClassName = (tier: PricingTier) => {
    let baseClass = "relative p-8 rounded-2xl border transition-all duration-300 hover:scale-105 ";
    
    if (tier.quantum) {
      return baseClass + "bg-gradient-to-br from-purple-900 via-black to-indigo-900 border-purple-500 shadow-2xl shadow-purple-500/50";
    } else if (tier.premium) {
      return baseClass + "bg-gradient-to-br from-gray-900 to-black border-gold-500 shadow-xl shadow-gold-500/30";
    } else if (tier.highlight) {
      return baseClass + "bg-gradient-to-br from-blue-900 to-indigo-900 border-blue-500 shadow-xl shadow-blue-500/30";
    } else {
      return baseClass + "bg-gradient-to-br from-gray-800 to-gray-900 border-gray-600 shadow-lg";
    }
  };

  return (
    <div className="min-h-screen bg-black text-white py-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div 
          className="text-center mb-16"
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-purple-400 via-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Quantum Omniscient™ Pricing
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Quantum foresight for an intelligent economy. Choose your level of quantum supremacy.
          </p>
          
          {/* Annual/Monthly Toggle */}
          <div className="flex items-center justify-center space-x-4 mb-8">
            <span className={`text-lg ${!isAnnual ? 'text-white' : 'text-gray-400'}`}>Monthly</span>
            <button
              onClick={() => setIsAnnual(!isAnnual)}
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-purple-600 transition-colors focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  isAnnual ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`text-lg ${isAnnual ? 'text-white' : 'text-gray-400'}`}>Annual</span>
            <span className="text-sm text-green-400 font-semibold">Save 20%</span>
          </div>
        </motion.div>

        {/* Pricing Cards */}
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {pricingTiers.map((tier, index) => (
            <motion.div
              key={tier.name}
              variants={cardVariants}
              className={getCardClassName(tier)}
              onClick={() => setSelectedTier(tier.name)}
            >
              {/* Badge */}
              {tier.badge && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className={`px-4 py-2 rounded-full text-sm font-bold ${
                    tier.quantum ? 'bg-purple-500 text-white' :
                    tier.premium ? 'bg-yellow-500 text-black' :
                    tier.highlight ? 'bg-blue-500 text-white' :
                    'bg-green-500 text-white'
                  }`}>
                    {tier.badge}
                  </span>
                </div>
              )}

              {/* Tier Name */}
              <h3 className={`text-2xl font-bold mb-4 ${
                tier.quantum ? 'text-purple-300' :
                tier.premium ? 'text-yellow-300' :
                tier.highlight ? 'text-blue-300' :
                'text-white'
              }`}>
                {tier.name}
              </h3>

              {/* Price */}
              <div className="mb-6">
                <div className="flex items-baseline space-x-2">
                  <span className="text-4xl font-bold text-white">{tier.price}</span>
                  <span className="text-lg text-gray-400">/month</span>
                </div>
                {tier.originalPrice && (
                  <div className="flex items-center space-x-2 mt-2">
                    <span className="text-lg text-gray-500 line-through">{tier.originalPrice}</span>
                    <span className="text-green-400 font-semibold text-sm">600% Premium Value</span>
                  </div>
                )}
              </div>

              {/* Description */}
              <p className="text-gray-300 mb-6">{tier.description}</p>

              {/* Features */}
              <ul className="space-y-3 mb-8">
                {tier.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start space-x-3">
                    <svg className={`w-5 h-5 mt-0.5 flex-shrink-0 ${
                      tier.quantum ? 'text-purple-400' :
                      tier.premium ? 'text-yellow-400' :
                      tier.highlight ? 'text-blue-400' :
                      'text-green-400'
                    }`} fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                    <span className="text-gray-300 text-sm">{feature}</span>
                  </li>
                ))}
              </ul>

              {/* CTA Button */}
              <button className={`w-full py-3 px-6 rounded-lg font-semibold transition-all duration-300 ${
                tier.quantum ? 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white shadow-lg shadow-purple-500/50' :
                tier.premium ? 'bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-black shadow-lg shadow-yellow-500/50' :
                tier.highlight ? 'bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white shadow-lg shadow-blue-500/50' :
                'bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white'
              }`}>
                {tier.cta}
              </button>
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom CTA */}
        <motion.div 
          className="text-center mt-16"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          <p className="text-gray-400 mb-6">
            All plans include our quantum-safe guarantee and mystique-driven results.
          </p>
          <div className="flex justify-center space-x-4">
            <button className="px-8 py-3 bg-transparent border border-purple-500 text-purple-400 rounded-lg hover:bg-purple-500 hover:text-white transition-all duration-300">
              Schedule Demo
            </button>
            <button className="px-8 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-all duration-300">
              Start Free Trial
            </button>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default QuantumOmniscientPricing;