import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function SigmaSelect() {
  const [sigmaMetrics, setSigmaMetrics] = useState({
    qei: 0,
    momentum: 0,
    forecast30d: 0,
    conversion: 24.7,
    uptime: 99.9,
    energy: -42.3
  });

  const [isLoading, setIsLoading] = useState(true);

  // Simulate API call for Sigma metrics
  useEffect(() => {
    const fetchMetrics = async () => {
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Simulate QEI calculation
      const cycleTime = 12;
      const throughput = 950;
      const errorRate = 0.02;
      const qei = (throughput / Math.max(cycleTime, 1)) * (1 - Math.min(errorRate, 0.99));
      
      // Simulate momentum calculation
      const history = [520, 610, 720, 900, 1150];
      const last = history[history.length - 1];
      const first = history[0];
      const momentum = ((last - first) / Math.max(first, 1)) * 100;
      
      setSigmaMetrics({
        qei: Math.round(qei * 100) / 100,
        momentum: Math.round(momentum),
        forecast30d: Math.round(momentum * 1.3),
        conversion: 24.7,
        uptime: 99.9,
        energy: -42.3
      });
      
      setIsLoading(false);
    };

    fetchMetrics();
  }, []);

  const pricingTiers = [
    {
      name: "DIY",
      price: "$997/mo",
      description: "Self-service platform with core capabilities",
      features: [
        "Metis agents (up to 10)",
        "Quantum scoring & optimization",
        "Basic Hyperion scaling",
        "SigmaEQ dashboard access",
        "Community support",
        "Basic compliance modules"
      ],
      color: "from-flyfoxSilver-600 to-flyfoxSilver-700",
      cta: "Start DIY",
      popular: false
    },
    {
      name: "DFY",
      price: "$2,997/mo",
      description: "Done-for-you deployment with advanced capabilities",
      features: [
        "Full deployment & setup",
        "Advanced Hyperion scaling",
        "SigmaEQ coaching & training",
        "Up to 50 agents",
        "Priority support",
        "Advanced compliance",
        "Custom integrations",
        "Performance optimization"
      ],
      color: "from-goliathMaize-500 to-goliathMaize-600",
      cta: "Start DFY",
      popular: true
    },
    {
      name: "Enterprise",
      price: "$9,997/mo",
      description: "Full-scale enterprise deployment with custom solutions",
      features: [
        "500+ agents capacity",
        "Custom SigmaEQ development",
        "Priority Dynex access",
        "Dedicated success manager",
        "Custom compliance frameworks",
        "White-label options",
        "API access & custom development",
        "24/7 premium support"
      ],
      color: "from-goliathNavy-600 to-goliathNavy-700",
      cta: "Contact Sales",
      popular: false
    }
  ];

  const sigmaCapabilities = [
    {
      title: "SigmaEQ Engine",
      description: "Quantum-enhanced intelligence engine for sales optimization",
      icon: "🧠",
      features: [
        "Real-time QEI calculation",
        "Momentum scoring & forecasting",
        "Predictive analytics",
        "Performance optimization"
      ]
    },
    {
      title: "Q-Sales Division",
      description: "Self-evolving quantum sales agent system",
      icon: "🤖",
      features: [
        "Autonomous lead generation",
        "Intelligent qualification",
        "Dynamic pricing optimization",
        "Revenue forecasting"
      ]
    },
    {
      title: "Revenue Intelligence",
      description: "AI-powered insights for revenue optimization",
      icon: "📊",
      features: [
        "Conversion rate optimization",
        "Customer lifetime value analysis",
        "Churn prediction & prevention",
        "Market opportunity identification"
      ]
    }
  ];

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-sigma-500 via-sigma-600 to-sigma-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            Sigma Select
          </h1>
          <p className="text-xl md:text-2xl text-sigma-100 max-w-4xl mx-auto leading-relaxed">
            The world's most advanced sales intelligence platform powered by FLYFOX AI's quantum computing 
            and self-learning agents. Transform your sales performance with 410x optimization.
          </p>
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="#pricing" className="bg-white text-sigma-600 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              💰 View Pricing
            </Link>
            <Link href="/contact" className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              📞 Book Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Live Metrics Dashboard */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Live Performance Metrics
            </h2>
            <p className="text-xl text-gray-600">
              Real-time insights powered by SigmaEQ engine and Dynex quantum computing
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-2xl shadow-lg">
              <div className="text-3xl mb-4">📈</div>
              <h3 className="text-xl font-bold mb-2">QEI Score</h3>
              <div className="text-4xl font-bold mb-2">
                {isLoading ? "..." : sigmaMetrics.qei}
              </div>
              <p className="text-blue-100 text-sm">Quantum Efficiency Index</p>
            </div>
            
            <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-2xl shadow-lg">
              <div className="text-3xl mb-4">🚀</div>
              <h3 className="text-xl font-bold mb-2">Momentum</h3>
              <div className="text-4xl font-bold mb-2">
                {isLoading ? "..." : `+${sigmaMetrics.momentum}%`}
              </div>
              <p className="text-green-100 text-sm">Performance momentum</p>
            </div>
            
            <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-2xl shadow-lg">
              <div className="text-3xl mb-4">🔮</div>
              <h3 className="text-xl font-bold mb-2">30-Day Forecast</h3>
              <div className="text-4xl font-bold mb-2">
                {isLoading ? "..." : `+${sigmaMetrics.forecast30d}%`}
              </div>
              <p className="text-purple-100 text-sm">Predicted growth</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-green-600 mb-2">{sigmaMetrics.conversion}%</div>
              <p className="text-gray-600">Conversion Rate</p>
            </div>
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-blue-600 mb-2">{sigmaMetrics.uptime}%</div>
              <p className="text-gray-600">System Uptime</p>
            </div>
            <div className="bg-gray-50 rounded-xl p-6 text-center">
              <div className="text-2xl font-bold text-orange-600 mb-2">{sigmaMetrics.energy}%</div>
              <p className="text-gray-600">Energy Efficiency</p>
            </div>
          </div>
        </div>
      </section>

      {/* Core Capabilities */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Core Capabilities
            </h2>
            <p className="text-xl text-gray-600">
              Powered by FLYFOX AI's quantum computing and self-learning intelligence
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {sigmaCapabilities.map((capability, index) => (
              <div key={index} className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
                <div className="w-20 h-20 bg-gradient-to-br from-sigma-500 to-sigma-600 rounded-2xl flex items-center justify-center text-3xl text-white mx-auto mb-6">
                  {capability.icon}
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-4 text-center">{capability.title}</h3>
                <p className="text-gray-600 mb-6 text-center leading-relaxed">{capability.description}</p>
                <ul className="space-y-3">
                  {capability.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start space-x-2">
                      <span className="text-sigma-500 mt-1">•</span>
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Tiers */}
      <section id="pricing" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Choose Your Path to Success
            </h2>
            <p className="text-xl text-gray-600">
              From self-service to full enterprise deployment, we have the solution for every business
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {pricingTiers.map((tier, index) => (
              <div key={index} className={`relative rounded-2xl p-8 shadow-2xl border-2 ${
                tier.popular 
                  ? 'border-goliathMaize-500 scale-105' 
                  : 'border-gray-200'
              }`}>
                {tier.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-goliathMaize-500 text-white px-4 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">{tier.name}</h3>
                  <p className="text-gray-600 mb-4">{tier.description}</p>
                  <div className="text-4xl font-bold text-gray-900">{tier.price}</div>
                </div>
                
                <ul className="space-y-4 mb-8">
                  {tier.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start space-x-3">
                      <div className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                        <svg className="w-3 h-3 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                        </svg>
                      </div>
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>
                
                <button className={`w-full py-4 px-6 rounded-xl font-semibold text-lg transition-all ${
                  tier.popular
                    ? `bg-gradient-to-r ${tier.color} text-white hover:shadow-lg`
                    : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                }`}>
                  {tier.cta}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Success Stories */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Success Stories
            </h2>
            <p className="text-xl text-gray-600">
              See how businesses are transforming their sales with Sigma Select
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-sigma-500 to-sigma-600 rounded-full flex items-center justify-center text-2xl text-white font-bold">
                  T
                </div>
                <div>
                  <h4 className="text-xl font-bold text-gray-900">TechCorp Solutions</h4>
                  <p className="text-gray-600">B2B Software Company</p>
                </div>
              </div>
              <p className="text-gray-700 mb-4">
                "Sigma Select transformed our sales process. Our QEI score increased from 0.45 to 0.89, 
                and we're seeing 247% revenue growth in just 6 months."
              </p>
              <div className="flex justify-between text-sm text-gray-600">
                <span>QEI: 0.89</span>
                <span>Growth: +247%</span>
                <span>Agents: 25</span>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <div className="flex items-center space-x-4 mb-6">
                <div className="w-16 h-16 bg-gradient-to-br from-goliathMaize-500 to-goliathMaize-600 rounded-full flex items-center justify-center text-2xl text-white font-bold">
                  F
                </div>
                <div>
                  <h4 className="text-xl font-bold text-gray-900">Financial Dynamics</h4>
                  <p className="text-gray-600">Fintech Startup</p>
                </div>
              </div>
              <p className="text-gray-700 mb-4">
                "The quantum-powered forecasting is incredible. We predicted market shifts 3 weeks ahead 
                and adjusted our strategy accordingly, resulting in 89% better conversion rates."
              </p>
              <div className="flex justify-between text-sm text-gray-600">
                <span>QEI: 0.92</span>
                <span>Conversion: +89%</span>
                <span>Agents: 15</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-sigma-500 via-sigma-600 to-sigma-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Transform Your Sales?
          </h2>
          <p className="text-xl text-sigma-100 max-w-3xl mx-auto mb-8">
            Join the quantum revolution in sales intelligence. Experience 410x performance optimization 
            with FLYFOX AI's self-learning agents.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/contact" className="bg-white text-sigma-600 hover:bg-gray-100 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🚀 Start Free Trial
            </Link>
            <Link href="/ecosystem" className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all">
              🔍 Explore Ecosystem
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
