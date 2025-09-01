import React, { useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';

interface PricingTier {
  name: string;
  price: string;
  period: string;
  description: string;
  features: string[];
  cta: string;
  popular?: boolean;
}

const pricingTiers: PricingTier[] = [
  {
    name: "DIY (Self-Service)",
    price: "$997",
    period: "/month",
    description: "Full NQBA platform access with self-implementation",
    features: [
      "Complete NQBA Dashboard Access",
      "Quantum Lead Scoring Engine",
      "Integration Templates (n8n, UiPath, Mendix)",
      "Self-Service Setup Guides",
      "Community Support",
      "Basic Analytics & Reporting"
    ],
    cta: "Start DIY Trial"
  },
  {
    name: "DFY (Done-For-You)",
    price: "$4,997",
    period: "/month",
    description: "Full implementation + management by our quantum experts",
    features: [
      "Everything in DIY",
      "Expert Implementation (7-day setup)",
      "Custom Integration Development",
      "Dedicated Success Manager",
      "Priority Support",
      "Advanced Quantum Analytics",
      "Monthly Strategy Sessions"
    ],
    cta: "Book DFY Strategy Call",
    popular: true
  },
  {
    name: "Enterprise",
    price: "Custom",
    period: "",
    description: "White-label quantum sales platform for your organization",
    features: [
      "Everything in DFY",
      "White-Label Branding",
      "Multi-Tenant Architecture",
      "Custom Quantum Models",
      "API Access & Webhooks",
      "24/7 Dedicated Support",
      "Compliance & Security Audit"
    ],
    cta: "Contact Enterprise Sales"
  }
];

export default function Pricing() {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');

  const handleCTA = (tier: PricingTier) => {
    if (tier.name.includes('DFY')) {
      // DFY: Book strategy call
      window.open('https://calendly.com/flyfox-ai/strategy-call', '_blank');
    } else if (tier.name.includes('Enterprise')) {
      // Enterprise: Contact sales
      window.open('mailto:enterprise@flyfoxai.io?subject=Enterprise%20Inquiry', '_blank');
    } else {
      // DIY: Start trial (redirect to dashboard)
      window.location.href = '/dashboard';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Header />
      
      <div className="container mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold mb-4">
            Choose Your Quantum Sales Acceleration
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            From self-service to fully managed, we scale with your business
          </p>
          
          {/* Billing Toggle */}
          <div className="flex justify-center items-center mb-8">
            <span className={`mr-3 ${billingCycle === 'monthly' ? 'text-white' : 'text-gray-400'}`}>
              Monthly
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'annual' : 'monthly')}
              className="relative inline-flex h-6 w-11 items-center rounded-full bg-blue-600"
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${
                  billingCycle === 'annual' ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
            <span className={`ml-3 ${billingCycle === 'annual' ? 'text-white' : 'text-gray-400'}`}>
              Annual
              <span className="ml-1 text-green-400 text-sm">(Save 20%)</span>
            </span>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {pricingTiers.map((tier, index) => (
            <div
              key={index}
              className={`relative rounded-lg p-8 ${
                tier.popular
                  ? 'bg-gradient-to-b from-blue-600 to-purple-700 ring-2 ring-blue-500'
                  : 'bg-gray-800 border border-gray-700'
              } hover:scale-105 transition-transform duration-200`}
            >
              {tier.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-green-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold mb-2">{tier.name}</h3>
                <p className="text-gray-300 mb-4">{tier.description}</p>
                <div className="text-4xl font-bold">
                  {tier.price}
                  {tier.period && (
                    <span className="text-lg text-gray-300">
                      {billingCycle === 'annual' && tier.price !== 'Custom' 
                        ? `/year` 
                        : tier.period
                      }
                    </span>
                  )}
                </div>
                {billingCycle === 'annual' && tier.price !== 'Custom' && (
                  <p className="text-green-400 text-sm mt-1">
                    Save ${Math.round(parseInt(tier.price.replace('$', '').replace(',', '')) * 12 * 0.2).toLocaleString()}
                  </p>
                )}
              </div>

              <ul className="space-y-3 mb-8">
                {tier.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start">
                    <svg
                      className="w-5 h-5 text-green-400 mr-3 mt-0.5 flex-shrink-0"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span className="text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleCTA(tier)}
                className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
                  tier.popular
                    ? 'bg-white text-blue-600 hover:bg-gray-100'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {tier.cta}
              </button>
            </div>
          ))}
        </div>

        {/* Value Props */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold mb-8">Why Choose FLYFOX AI?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-4xl mb-4">⚡</div>
              <h3 className="text-xl font-semibold mb-2">410x Performance</h3>
              <p className="text-gray-300">
                Dynex quantum acceleration delivers unprecedented speed
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-4xl mb-4">🎯</div>
              <h3 className="text-xl font-semibold mb-2">Quantum Lead Scoring</h3>
              <p className="text-gray-300">
                NQBA-powered predictive analytics for higher conversions
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-4xl mb-4">🔗</div>
              <h3 className="text-xl font-semibold mb-2">Seamless Integration</h3>
              <p className="text-gray-300">
                Plug into existing tools via n8n, UiPath, Mendix adapters
              </p>
            </div>
          </div>
        </div>

        {/* ROI Calculator */}
        <div className="mt-20 bg-gray-800 p-8 rounded-lg max-w-4xl mx-auto">
          <h2 className="text-2xl font-bold mb-6 text-center">ROI Calculator</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">Your Current Metrics</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-300 mb-1">Monthly Leads</label>
                  <input
                    type="number"
                    placeholder="1000"
                    className="w-full p-2 bg-gray-700 border border-gray-600 rounded text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-300 mb-1">Conversion Rate (%)</label>
                  <input
                    type="number"
                    placeholder="2.5"
                    className="w-full p-2 bg-gray-700 border border-gray-600 rounded text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm text-gray-300 mb-1">Average Deal Value ($)</label>
                  <input
                    type="number"
                    placeholder="5000"
                    className="w-full p-2 bg-gray-700 border border-gray-600 rounded text-white"
                  />
                </div>
              </div>
            </div>
            <div>
              <h3 className="text-lg font-semibold mb-4">With FLYFOX AI</h3>
              <div className="space-y-4">
                <div className="flex justify-between">
                  <span>Improved Conversion Rate:</span>
                  <span className="text-green-400">+40%</span>
                </div>
                <div className="flex justify-between">
                  <span>Faster Sales Cycles:</span>
                  <span className="text-green-400">-30%</span>
                </div>
                <div className="flex justify-between">
                  <span>Higher Deal Values:</span>
                  <span className="text-green-400">+25%</span>
                </div>
                <div className="border-t border-gray-600 pt-4">
                  <div className="flex justify-between font-bold">
                    <span>Monthly Revenue Lift:</span>
                    <span className="text-green-400">$87,500</span>
                  </div>
                  <div className="flex justify-between text-sm text-gray-300">
                    <span>Annual ROI:</span>
                    <span>1,750%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* FAQ */}
        <div className="mt-20">
          <h2 className="text-3xl font-bold text-center mb-8">Frequently Asked Questions</h2>
          <div className="max-w-3xl mx-auto space-y-6">
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-2">What's included in the setup fee for DFY?</h3>
              <p className="text-gray-300">
                One-time $9,997 setup includes custom integration development, data migration, 
                team training, and go-live support within 7 business days.
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-2">Can I upgrade from DIY to DFY later?</h3>
              <p className="text-gray-300">
                Absolutely! We offer seamless upgrade paths with prorated pricing and migration assistance.
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <h3 className="text-lg font-semibold mb-2">What quantum computing technology do you use?</h3>
              <p className="text-gray-300">
                We leverage Dynex's neuromorphic quantum computing platform for 410x performance gains 
                over classical systems, with QUBO optimization for complex business problems.
              </p>
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
}
