import React from "react";

const tiers = [
  {
    name: "Starter",
    price: "$149 / mo",
    bullets: ["Portal + 2 agents", "UiPath / n8n recipes", "5k contacts"]
  },
  {
    name: "Growth",
    price: "$699 / mo",
    bullets: ["10 agents", "QSAI-Lite batch scoring", "50k contacts", "Integrations"]
  },
  {
    name: "Enterprise",
    price: "$2,999 / mo",
    bullets: ["50 agents", "Real-time QSAI scoring", "500k contacts", "Premium templates"]
  },
  {
    name: "Division",
    price: "$19,997 / mo",
    bullets: ["100–500 agents", "White-label", "Dedicated Quantum Architect hours"]
  }
];

export default function Pricing() {
  return (
    <div className="max-w-7xl mx-auto p-8">
      <h1 className="text-3xl font-bold mb-6">Pricing — FLYFOX AI • NQBA</h1>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {tiers.map(t => (
          <div key={t.name} className="card">
            <div className="text-lg font-semibold">{t.name}</div>
            <div className="text-2xl font-bold my-3">{t.price}</div>
            <ul className="text-sm space-y-2 mb-4">
              {t.bullets.map(b => <li key={b}>• {b}</li>)}
            </ul>
            <button className="mt-auto px-4 py-2 bg-sigma-purple text-white rounded">Get Started</button>
          </div>
        ))}
      </div>
    </div>
  );
}
      features: [
        'Unlimited partners',
        'Unlimited leads',
        'Full quantum processing power',
        'Custom quantum models',
        'White-label solutions',
        'Dedicated support team',
        'Custom integrations',
        'Advanced security',
        'SLA guarantees',
        'On-premise deployment',
      ],
      limitations: [],
      cta: 'Contact Sales',
      popular: false,
    },
  ]

  const features = [
    {
      category: 'Quantum Processing',
      items: [
        { name: 'Quantum Lead Scoring', starter: true, pro: true, enterprise: true },
        { name: 'Advanced QUBO Optimization', starter: false, pro: true, enterprise: true },
        { name: 'Custom Quantum Models', starter: false, pro: false, enterprise: true },
        { name: 'Quantum Explainability', starter: false, pro: true, enterprise: true },
      ],
    },
    {
      category: 'Analytics & Insights',
      items: [
        { name: 'Real-time Dashboards', starter: true, pro: true, enterprise: true },
        { name: 'Predictive Analytics', starter: false, pro: true, enterprise: true },
        { name: 'Custom Reports', starter: false, pro: true, enterprise: true },
        { name: 'Advanced Visualizations', starter: false, pro: true, enterprise: true },
      ],
    },
    {
      category: 'Integration & Support',
      items: [
        { name: 'API Access', starter: true, pro: true, enterprise: true },
        { name: 'Webhook Support', starter: false, pro: true, enterprise: true },
        { name: 'Custom Integrations', starter: false, pro: false, enterprise: true },
        { name: 'Dedicated Support', starter: false, pro: false, enterprise: true },
      ],
    },
  ]

  return (
    <>
      <Head>
        <title>Pricing - Goliath Quantum</title>
        <meta name="description" content="Choose the perfect quantum-powered plan for your business" />
      </Head>

      <div className="min-h-screen bg-slate-50">
        <Navbar />

        {/* Hero Section */}
        <section className="py-20 bg-gradient-to-br from-slate-50 via-white to-slate-100">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div className="flex justify-center mb-6">
              <Zap className="h-12 w-12 text-quantum-primary quantum-glow" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6">
              Choose Your <span className="gradient-text">Quantum</span> Plan
            </h1>
            <p className="text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
              Unlock the power of quantum computing for your business. 
              Start with a free trial and scale as you grow.
            </p>
            <div className="bg-quantum-primary/10 border border-quantum-primary/20 rounded-xl p-4 inline-block">
              <p className="text-quantum-primary font-semibold">
                🎉 Limited Time: Get 30% off your first 3 months with code QUANTUM30
              </p>
            </div>
          </div>
        </section>

        {/* Pricing Cards */}
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {plans.map((plan, index) => (
                <div
                  key={index}
                  className={`relative bg-white rounded-2xl shadow-lg border-2 transition-all duration-300 hover:shadow-xl ${
                    plan.popular
                      ? 'border-quantum-primary scale-105'
                      : 'border-slate-200 hover:border-quantum-primary/50'
                  }`}
                >
                  {plan.popular && (
                    <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                      <div className="bg-gradient-to-r from-quantum-primary to-quantum-secondary text-white px-6 py-2 rounded-full text-sm font-semibold flex items-center space-x-1">
                        <Star className="h-4 w-4" />
                        <span>Most Popular</span>
                      </div>
                    </div>
                  )}

                  <div className="p-8">
                    <h3 className="text-2xl font-bold text-slate-900 mb-2">{plan.name}</h3>
                    <p className="text-slate-600 mb-6">{plan.description}</p>

                    <div className="mb-6">
                      {plan.price ? (
                        <div className="flex items-baseline">
                          <span className="text-4xl font-bold text-slate-900">${plan.price}</span>
                          <span className="text-slate-600 ml-2">/month</span>
                        </div>
                      ) : (
                        <div className="text-4xl font-bold text-slate-900">Custom</div>
                      )}
                    </div>

                    <Link
                      href={plan.name === 'Enterprise' ? '/contact' : '/sign-in'}
                      className={`w-full py-3 px-6 rounded-xl font-semibold text-center block transition-all duration-300 mb-8 ${
                        plan.popular
                          ? 'btn-quantum text-white shadow-lg hover:shadow-xl'
                          : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                      }`}
                    >
                      {plan.cta}
                    </Link>

                    <div className="space-y-4">
                      <h4 className="font-semibold text-slate-900">What's included:</h4>
                      <ul className="space-y-3">
                        {plan.features.map((feature, featureIndex) => (
                          <li key={featureIndex} className="flex items-start space-x-3">
                            <Check className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                            <span className="text-slate-600">{feature}</span>
                          </li>
                        ))}
                      </ul>

                      {plan.limitations.length > 0 && (
                        <div className="pt-4 border-t border-slate-200">
                          <h4 className="font-semibold text-slate-900 mb-3">Limitations:</h4>
                          <ul className="space-y-2">
                            {plan.limitations.map((limitation, limitIndex) => (
                              <li key={limitIndex} className="text-sm text-slate-500">
                                • {limitation}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Feature Comparison */}
        <section className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-slate-900 mb-4">
                Compare <span className="gradient-text">Features</span>
              </h2>
              <p className="text-xl text-slate-600">
                See exactly what's included in each plan
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-slate-200">
                    <th className="text-left py-4 px-6 font-semibold text-slate-900">Features</th>
                    <th className="text-center py-4 px-6 font-semibold text-slate-900">Starter</th>
                    <th className="text-center py-4 px-6 font-semibold text-slate-900">Professional</th>
                    <th className="text-center py-4 px-6 font-semibold text-slate-900">Enterprise</th>
                  </tr>
                </thead>
                <tbody>
                  {features.map((category, categoryIndex) => (
                    <>
                      <tr key={`category-${categoryIndex}`} className="bg-slate-50">
                        <td colSpan={4} className="py-3 px-6 font-semibold text-slate-900">
                          {category.category}
                        </td>
                      </tr>
                      {category.items.map((item, itemIndex) => (
                        <tr key={`item-${categoryIndex}-${itemIndex}`} className="border-b border-slate-100">
                          <td className="py-3 px-6 text-slate-600">{item.name}</td>
                          <td className="py-3 px-6 text-center">
                            {item.starter ? (
                              <Check className="h-5 w-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-slate-300">—</span>
                            )}
                          </td>
                          <td className="py-3 px-6 text-center">
                            {item.pro ? (
                              <Check className="h-5 w-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-slate-300">—</span>
                            )}
                          </td>
                          <td className="py-3 px-6 text-center">
                            {item.enterprise ? (
                              <Check className="h-5 w-5 text-green-500 mx-auto" />
                            ) : (
                              <span className="text-slate-300">—</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* FAQ Section */}
        <section className="py-16 bg-slate-50">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-slate-900 mb-4">
                Frequently Asked Questions
              </h2>
            </div>

            <div className="space-y-8">
              <div className="bg-white rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-900 mb-3">
                  What is quantum advantage in business intelligence?
                </h3>
                <p className="text-slate-600">
                  Quantum advantage refers to the exponential speedup and optimization capabilities 
                  that quantum computing provides over classical computing for specific problems like 
                  complex optimization, pattern recognition, and predictive modeling.
                </p>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-900 mb-3">
                  How does the free trial work?
                </h3>
                <p className="text-slate-600">
                  Start with a 14-day free trial of our Professional plan. No credit card required. 
                  Experience the full power of quantum-enhanced business intelligence before committing.
                </p>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-900 mb-3">
                  Can I upgrade or downgrade my plan?
                </h3>
                <p className="text-slate-600">
                  Yes, you can change your plan at any time. Upgrades take effect immediately, 
                  while downgrades take effect at the next billing cycle.
                </p>
              </div>

              <div className="bg-white rounded-xl p-6 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-900 mb-3">
                  What kind of support do you provide?
                </h3>
                <p className="text-slate-600">
                  We provide email support for Starter plans, priority support for Professional plans, 
                  and dedicated support teams for Enterprise customers. All plans include comprehensive 
                  documentation and quantum computing resources.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 bg-gradient-to-r from-quantum-primary to-quantum-secondary">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h2 className="text-3xl font-bold text-white mb-6">
              Ready to Experience Quantum Advantage?
            </h2>
            <p className="text-xl text-white/90 mb-8">
              Join thousands of businesses already leveraging quantum computing for unprecedented insights.
            </p>
            <Link
              href="/sign-in"
              className="bg-white text-quantum-primary px-8 py-4 rounded-xl font-semibold text-lg hover:bg-slate-50 transition-all duration-300 shadow-xl hover:shadow-2xl inline-flex items-center space-x-2"
            >
              <span>Start Your Free Trial</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </div>
        </section>

        <Footer />
      </div>
    </>
  )
}