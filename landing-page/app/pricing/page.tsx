'use client';

import { useState } from 'react';
import { Check, Zap, Crown, Building } from 'lucide-react';

const PricingPage = () => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'annual'>('monthly');

  const plans = [
    {
      name: 'Starter',
      icon: <Zap className="w-6 h-6" />,
      price: { monthly: 99, annual: 990 },
      description: 'Perfect for small teams getting started with quantum computing',
      features: [
        '1,000 quantum computations/month',
        'Basic QUBO optimization',
        'Email support',
        'Single user access',
        'API documentation',
        'Community forum access'
      ],
      cta: 'Start Free Trial',
      popular: false,
      color: 'from-blue-500 to-blue-600'
    },
    {
      name: 'Professional',
      icon: <Crown className="w-6 h-6" />,
      price: { monthly: 499, annual: 4990 },
      description: 'Advanced quantum algorithms for growing businesses',
      features: [
        '10,000 quantum computations/month',
        'Advanced quantum algorithms',
        'Priority support (24/7)',
        'Team collaboration (5 users)',
        'Full API access',
        'Custom integrations',
        'Performance analytics',
        'White-label options'
      ],
      cta: 'Start Free Trial',
      popular: true,
      color: 'from-purple-500 to-purple-600'
    },
    {
      name: 'Enterprise',
      icon: <Building className="w-6 h-6" />,
      price: { monthly: 2999, annual: 29990 },
      description: 'Unlimited quantum power for large organizations',
      features: [
        'Unlimited quantum computations',
        'Custom quantum algorithms',
        'Dedicated support manager',
        'Unlimited team members',
        'On-premise deployment',
        'SLA guarantees',
        'Advanced security features',
        'Custom training sessions'
      ],
      cta: 'Contact Sales',
      popular: false,
      color: 'from-gold-500 to-gold-600'
    }
  ];

  const handleGetStarted = (planName: string) => {
    if (planName === 'Enterprise') {
      window.open('mailto:sales@nqba.ai?subject=Enterprise Plan Inquiry', '_blank');
    } else {
      // Redirect to signup/trial page
      window.open('https://app.nqba.ai/signup?plan=' + planName.toLowerCase(), '_blank');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="container mx-auto px-6 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-white mb-6">
            Choose Your <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Quantum Advantage</span>
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Unlock the power of quantum computing for your business. Start with a free trial and scale as you grow.
          </p>
        </div>

        {/* Billing Toggle */}
        <div className="flex justify-center mb-12">
          <div className="bg-slate-800 p-1 rounded-lg">
            <button
              onClick={() => setBillingCycle('monthly')}
              className={`px-6 py-2 rounded-md transition-all ${
                billingCycle === 'monthly'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Monthly
            </button>
            <button
              onClick={() => setBillingCycle('annual')}
              className={`px-6 py-2 rounded-md transition-all ${
                billingCycle === 'annual'
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Annual <span className="text-green-400 text-sm ml-1">(Save 17%)</span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
          {plans.map((plan, index) => (
            <div
              key={plan.name}
              className={`relative bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 border ${
                plan.popular
                  ? 'border-purple-500 ring-2 ring-purple-500/20'
                  : 'border-slate-700'
              } hover:border-slate-600 transition-all duration-300 hover:transform hover:scale-105`}
            >
              {plan.popular && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <span className="bg-gradient-to-r from-purple-500 to-blue-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                    Most Popular
                  </span>
                </div>
              )}

              <div className="text-center mb-8">
                <div className={`inline-flex p-3 rounded-lg bg-gradient-to-r ${plan.color} mb-4`}>
                  {plan.icon}
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                <p className="text-gray-400 mb-6">{plan.description}</p>
                
                <div className="mb-6">
                  <span className="text-4xl font-bold text-white">
                    ${billingCycle === 'monthly' ? plan.price.monthly : plan.price.annual}
                  </span>
                  <span className="text-gray-400 ml-2">
                    /{billingCycle === 'monthly' ? 'month' : 'year'}
                  </span>
                </div>
              </div>

              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-start">
                    <Check className="w-5 h-5 text-green-400 mr-3 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>

              <button
                onClick={() => handleGetStarted(plan.name)}
                className={`w-full py-3 px-6 rounded-lg font-semibold transition-all duration-300 ${
                  plan.popular
                    ? 'bg-gradient-to-r from-purple-500 to-blue-500 text-white hover:from-purple-600 hover:to-blue-600'
                    : 'bg-slate-700 text-white hover:bg-slate-600'
                } hover:transform hover:scale-105`}
              >
                {plan.cta}
              </button>
            </div>
          ))}
        </div>

        {/* Enterprise Features */}
        <div className="mt-20 text-center">
          <h2 className="text-3xl font-bold text-white mb-8">Enterprise Features</h2>
          <div className="grid md:grid-cols-4 gap-6 max-w-4xl mx-auto">
            {[
              { title: 'Custom Algorithms', desc: 'Tailored quantum solutions' },
              { title: 'On-Premise Deploy', desc: 'Your infrastructure, our platform' },
              { title: 'Dedicated Support', desc: '24/7 expert assistance' },
              { title: 'SLA Guarantees', desc: '99.9% uptime commitment' }
            ].map((feature, index) => (
              <div key={index} className="bg-slate-800/30 p-6 rounded-lg">
                <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-20 text-center bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-2xl p-12">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Transform Your Business with Quantum Computing?
          </h2>
          <p className="text-xl text-gray-300 mb-8">
            Join leading companies already using NQBA to solve complex optimization problems.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => handleGetStarted('Professional')}
              className="bg-gradient-to-r from-purple-500 to-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:from-purple-600 hover:to-blue-600 transition-all duration-300"
            >
              Start Free Trial
            </button>
            <button
              onClick={() => window.open('mailto:sales@nqba.ai?subject=Demo Request', '_blank')}
              className="bg-slate-700 text-white px-8 py-3 rounded-lg font-semibold hover:bg-slate-600 transition-all duration-300"
            >
              Schedule Demo
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PricingPage;