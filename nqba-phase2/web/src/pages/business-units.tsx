import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function BusinessUnits() {
  const [totalRevenue, setTotalRevenue] = useState(10100000);
  const [totalClients, setTotalClients] = useState(312);
  const [activeAgents, setActiveAgents] = useState(247);
  const [quantumJobs, setQuantumJobs] = useState(89);

  useEffect(() => {
    // Simulate real-time business updates
    const interval = setInterval(() => {
      setTotalRevenue(prev => prev + Math.floor(Math.random() * 100000));
      setTotalClients(prev => prev + Math.floor(Math.random() * 2));
      setActiveAgents(prev => prev + Math.floor(Math.random() * 3) - 1);
      setQuantumJobs(prev => prev + Math.floor(Math.random() * 5));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const businessUnits = [
    {
      name: "FLYFOX AI",
      description: "Quantum-powered AI platform and business automation",
      icon: "🦊",
      color: "from-orange-500 to-red-500",
      revenue: 1200000,
      clients: 47,
      status: "Operational",
      features: ["AI Platform", "Business Automation", "Quantum Computing", "Self-Learning Agents"],
      metrics: [
        { label: "Platform Revenue", value: "$1.2M", color: "text-orange-600" },
        { label: "Active Clients", value: "47", color: "text-red-600" },
        { label: "AI Agents", value: "247", color: "text-pink-600" },
        { label: "Quantum Jobs", value: "89", color: "text-purple-600" }
      ]
    },
    {
      name: "Goliath Capital",
      description: "Quantum-enhanced financial services and investment management",
      icon: "🏛️",
      color: "from-green-500 to-emerald-500",
      revenue: 89000000,
      clients: 23,
      status: "Operational",
      features: ["Portfolio Management", "Risk Assessment", "Quantum Optimization", "AI Analysis"],
      metrics: [
        { label: "Portfolio Value", value: "$89M", color: "text-green-600" },
        { label: "Active Investments", value: "47", color: "text-emerald-600" },
        { label: "Annual ROI", value: "+23.7%", color: "text-teal-600" },
        { label: "Quantum Optimizations", value: "156", color: "text-cyan-600" }
      ]
    },
    {
      name: "Sigma Select",
      description: "AI-powered lead generation and sales optimization",
      icon: "Σ",
      color: "from-blue-500 to-cyan-500",
      revenue: 0,
      clients: 242,
      status: "Operational",
      features: ["Lead Generation", "AI Scoring", "Campaign Management", "Predictive Analytics"],
      metrics: [
        { label: "Leads Generated", value: "2,847", color: "text-blue-600" },
        { label: "Conversion Rate", value: "18.3%", color: "text-cyan-600" },
        { label: "Active Campaigns", value: "23", color: "text-indigo-600" },
        { label: "AI Optimizations", value: "89", color: "text-sky-600" }
      ]
    }
  ];

  const ecosystemMetrics = [
    { label: "Total Revenue", value: formatCurrency(totalRevenue), icon: "💰", color: "from-green-500 to-emerald-500" },
    { label: "Total Clients", value: totalClients.toLocaleString(), icon: "👥", color: "from-blue-500 to-cyan-500" },
    { label: "Active Agents", value: activeAgents.toLocaleString(), icon: "🤖", color: "from-purple-500 to-pink-500" },
    { label: "Quantum Jobs", value: quantumJobs.toLocaleString(), icon: "⚛️", color: "from-orange-500 to-red-500" }
  ];

  return (
    <>
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-gray-900 via-blue-900 to-indigo-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Business Units
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
              Comprehensive ecosystem of quantum-powered business solutions.
              From AI platforms to financial services, we're transforming industries with 410x performance boost.
            </p>
            
            {/* Ecosystem Status Badges */}
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <div className="flex items-center space-x-2 bg-green-500/20 backdrop-blur-sm border border-green-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>Total Revenue: {formatCurrency(totalRevenue)}</span>
              </div>
              <div className="flex items-center space-x-2 bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span>Total Clients: {totalClients}</span>
              </div>
              <div className="flex items-center space-x-2 bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                <span>AI Agents: {activeAgents}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Ecosystem Overview */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Ecosystem Overview</h2>
            <p className="text-xl text-gray-600">Integrated business units working together for maximum impact</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {ecosystemMetrics.map((metric, index) => (
              <div key={index} className="text-center">
                <div className={`w-20 h-20 bg-gradient-to-br ${metric.color} rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-4`}>
                  {metric.icon}
                </div>
                <div className="text-3xl font-bold text-gray-900 mb-2">{metric.value}</div>
                <p className="text-gray-600">{metric.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Business Units Grid */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Our Business Units</h2>
            <p className="text-xl text-gray-600">Specialized solutions for different industry needs</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {businessUnits.map((unit, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
                {/* Header */}
                <div className={`bg-gradient-to-br ${unit.color} text-white p-8 text-center`}>
                  <div className="text-6xl mb-4">{unit.icon}</div>
                  <h3 className="text-3xl font-bold mb-2">{unit.name}</h3>
                  <p className="text-white/90">{unit.description}</p>
                </div>

                {/* Content */}
                <div className="p-8">
                  {/* Status */}
                  <div className="flex items-center justify-between mb-6">
                    <span className="text-sm text-gray-600">Status</span>
                    <span className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                      {unit.status}
                    </span>
                  </div>

                  {/* Key Features */}
                  <div className="mb-6">
                    <h4 className="font-semibold text-gray-900 mb-3">Key Features</h4>
                    <div className="grid grid-cols-2 gap-2">
                      {unit.features.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center space-x-2">
                          <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                          <span className="text-sm text-gray-600">{feature}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Metrics */}
                  <div className="grid grid-cols-2 gap-4 mb-6">
                    {unit.metrics.map((metric, metricIndex) => (
                      <div key={metricIndex} className="text-center p-3 bg-gray-50 rounded-lg">
                        <p className="text-xs text-gray-600 mb-1">{metric.label}</p>
                        <p className={`font-bold ${metric.color}`}>{metric.value}</p>
                      </div>
                    ))}
                  </div>

                  {/* Action Button */}
                  <Link 
                    href={`/${unit.name.toLowerCase().replace(' ', '-')}`}
                    className={`block w-full text-center py-3 px-4 rounded-xl font-semibold transition-all duration-200 ${
                      unit.name === "FLYFOX AI" 
                        ? "bg-gradient-to-r from-orange-500 to-red-500 text-white hover:from-orange-600 hover:to-red-600"
                        : unit.name === "Goliath Capital"
                        ? "bg-gradient-to-r from-green-500 to-emerald-500 text-white hover:from-green-600 hover:to-emerald-600"
                        : "bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:from-blue-600 hover:to-cyan-600"
                    }`}
                  >
                    Manage {unit.name} →
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Integration Benefits */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Integration Benefits</h2>
            <p className="text-xl text-gray-600">How our business units work together for maximum value</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6">🔄</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Seamless Integration</h3>
              <p className="text-gray-600">
                All business units share the same NQBA core, enabling seamless data flow and cross-platform optimization
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6">⚡</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Quantum Performance</h3>
              <p className="text-gray-600">
                Shared quantum computing resources provide 410x performance boost across all business units
              </p>
            </div>

            <div className="text-center">
              <div className="w-20 h-20 bg-gradient-to-br from-green-500 to-emerald-500 rounded-2xl flex items-center justify-center text-white text-3xl mx-auto mb-6">🧠</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Shared Intelligence</h3>
              <p className="text-gray-600">
                AI agents and learning systems share insights across business units for continuous improvement
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Performance Comparison */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Performance Comparison</h2>
            <p className="text-xl text-gray-600">How our integrated approach outperforms traditional solutions</p>
          </div>

          <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-6">Traditional Approach</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span className="text-red-800">Siloed systems with limited integration</span>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span className="text-red-800">Manual data transfer between platforms</span>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span className="text-red-800">Limited scalability and performance</span>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-red-50 rounded-lg">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <span className="text-red-800">High operational costs</span>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-2xl font-bold text-gray-900 mb-6">FLYFOX AI Ecosystem</h3>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-800">Integrated NQBA core with seamless data flow</span>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-800">Automated cross-platform optimization</span>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-800">410x quantum performance boost</span>
                  </div>
                  <div className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <span className="text-green-800">Reduced operational costs by 73%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-gray-900 to-blue-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Experience the Power of Integration?</h2>
          <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
            Discover how our integrated business units can transform your operations with quantum-powered performance
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform-dashboard" className="bg-white text-gray-900 px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
              Access Platform Dashboard
            </Link>
            <Link href="/contact" className="bg-blue-600 text-white px-8 py-4 rounded-xl font-semibold hover:bg-blue-700 transition-colors">
              Schedule Consultation
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
