import { useState, useEffect } from "react";
import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function GoliathCapital() {
  const [portfolioValue, setPortfolioValue] = useState(89000000);
  const [roi, setRoi] = useState(23.7);
  const [activeInvestments, setActiveInvestments] = useState(47);
  const [quantumOptimizations, setQuantumOptimizations] = useState(156);

  useEffect(() => {
    // Simulate real-time portfolio updates
    const interval = setInterval(() => {
      setPortfolioValue(prev => prev + Math.floor(Math.random() * 100000 - 50000));
      setRoi(prev => Math.max(20, Math.min(30, prev + (Math.random() - 0.5) * 0.2)));
      setQuantumOptimizations(prev => prev + Math.floor(Math.random() * 3));
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

  const investmentCategories = [
    { name: "Quantum Tech", allocation: 35, color: "from-blue-500 to-cyan-500", icon: "⚛️" },
    { name: "AI & ML", allocation: 28, color: "from-purple-500 to-pink-500", icon: "🤖" },
    { name: "Fintech", allocation: 22, color: "from-green-500 to-emerald-500", icon: "💳" },
    { name: "Energy", allocation: 15, color: "from-orange-500 to-red-500", icon: "⚡" }
  ];

  const recentTransactions = [
    { id: "TXN_001", type: "Investment", amount: "$2.5M", company: "QuantumFlow Systems", status: "Completed", time: "2 hours ago" },
    { id: "TXN_002", type: "Divestment", amount: "$1.8M", company: "Legacy Tech Corp", status: "Processing", time: "1 day ago" },
    { id: "TXN_003", type: "Investment", amount: "$3.2M", company: "AI Nexus Labs", status: "Completed", time: "3 days ago" },
    { id: "TXN_004", type: "Dividend", amount: "$450K", company: "SmartGrid Energy", status: "Completed", time: "1 week ago" }
  ];

  const quantumAlgorithms = [
    { name: "Portfolio Optimization", status: "Active", efficiency: "99.7%", icon: "📊" },
    { name: "Risk Assessment", status: "Active", efficiency: "98.9%", icon: "⚠️" },
    { name: "Market Prediction", status: "Active", efficiency: "97.3%", icon: "🔮" },
    { name: "Arbitrage Detection", status: "Active", efficiency: "99.1%", icon: "💱" }
  ];

  return (
    <>
      <Header />

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-green-900 via-emerald-800 to-teal-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <div className="text-6xl md:text-7xl mb-6">🏛️</div>
            <h1 className="text-5xl md:text-6xl font-bold mb-6">
              Goliath Capital
            </h1>
            <p className="text-xl md:text-2xl text-green-200 max-w-4xl mx-auto leading-relaxed">
              Quantum-enhanced financial services and investment management.
              Leveraging 410x performance boost for superior portfolio optimization and risk management.
            </p>
            
            {/* Status Badges */}
            <div className="flex flex-wrap justify-center gap-4 mt-8">
              <div className="flex items-center space-x-2 bg-green-500/20 backdrop-blur-sm border border-green-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span>Portfolio: {formatCurrency(portfolioValue)}</span>
              </div>
              <div className="flex items-center space-x-2 bg-blue-500/20 backdrop-blur-sm border border-blue-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span>ROI: +{roi.toFixed(1)}%</span>
              </div>
              <div className="flex items-center space-x-2 bg-purple-500/20 backdrop-blur-sm border border-purple-500/30 px-4 py-2 rounded-full">
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                <span>Quantum Optimizations: {quantumOptimizations}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Key Metrics */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-green-600 mb-2">{formatCurrency(portfolioValue)}</div>
              <p className="text-gray-600">Total Portfolio Value</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-600 mb-2">+{roi.toFixed(1)}%</div>
              <p className="text-gray-600">Annual ROI</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-600 mb-2">{activeInvestments}</div>
              <p className="text-gray-600">Active Investments</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-orange-600 mb-2">{quantumOptimizations}</div>
              <p className="text-gray-600">Quantum Optimizations</p>
            </div>
          </div>
        </div>
      </section>

      {/* Portfolio Overview */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Portfolio Overview</h2>
            <p className="text-xl text-gray-600">Quantum-powered investment strategies for maximum returns</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            {/* Investment Categories */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Investment Allocation</h3>
              <div className="space-y-6">
                {investmentCategories.map((category, index) => (
                  <div key={index} className="flex items-center space-x-4">
                    <div className={`w-16 h-16 bg-gradient-to-br ${category.color} rounded-xl flex items-center justify-center text-white text-2xl`}>
                      {category.icon}
                    </div>
                    <div className="flex-1">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-semibold text-gray-900">{category.name}</span>
                        <span className="text-lg font-bold text-gray-700">{category.allocation}%</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div 
                          className={`bg-gradient-to-r ${category.color} h-3 rounded-full transition-all duration-1000`}
                          style={{ width: `${category.allocation}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Transactions */}
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Recent Transactions</h3>
              <div className="space-y-4">
                {recentTransactions.map((txn) => (
                  <div key={txn.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${
                        txn.status === 'Completed' ? 'bg-green-500' : 'bg-yellow-500'
                      }`}></div>
                      <div>
                        <p className="font-semibold text-gray-900">{txn.company}</p>
                        <p className="text-sm text-gray-600">{txn.type} • {txn.time}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-gray-900">{txn.amount}</p>
                      <p className={`text-xs ${
                        txn.status === 'Completed' ? 'text-green-600' : 'text-yellow-600'
                      }`}>
                        {txn.status}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Quantum Computing Integration */}
      <section className="py-16 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Quantum Computing Integration</h2>
            <p className="text-xl text-gray-600">Leveraging Dynex quantum computing for 410x performance boost</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
            {quantumAlgorithms.map((algo, index) => (
              <div key={index} className="bg-gradient-to-br from-purple-500 to-pink-500 text-white p-6 rounded-xl text-center">
                <div className="text-4xl mb-4">{algo.icon}</div>
                <h3 className="text-xl font-bold mb-2">{algo.name}</h3>
                <p className="text-purple-100 mb-3">{algo.status}</p>
                <div className="text-2xl font-bold">{algo.efficiency}</div>
              </div>
            ))}
          </div>

          {/* Quantum Performance Metrics */}
          <div className="bg-gradient-to-r from-gray-900 to-gray-800 text-white rounded-2xl p-8">
            <h3 className="text-2xl font-bold mb-6 text-center">Quantum Performance Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <div className="text-4xl font-bold text-green-400 mb-2">410x</div>
                <p className="text-gray-300">Performance Boost</p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-400 mb-2">99.9%</div>
                <p className="text-gray-300">Optimization Accuracy</p>
              </div>
              <div className="text-center">
                <div className="text-4xl font-bold text-purple-400 mb-2">24/7</div>
                <p className="text-gray-300">Continuous Operation</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Investment Strategies */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Investment Strategies</h2>
            <p className="text-xl text-gray-600">AI-powered strategies that adapt to market conditions</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🧠</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">AI-Driven Analysis</h3>
              <p className="text-gray-600 mb-6">
                Machine learning algorithms analyze market patterns and identify optimal investment opportunities
              </p>
              <div className="bg-green-100 text-green-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">⚛️</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Quantum Optimization</h3>
              <p className="text-gray-600 mb-6">
                Quantum algorithms optimize portfolio allocation for maximum returns and minimal risk
              </p>
              <div className="bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>

            <div className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200 text-center">
              <div className="text-5xl mb-6">🔄</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-4">Dynamic Rebalancing</h3>
              <p className="text-gray-600 mb-6">
                Continuous portfolio rebalancing based on real-time market data and AI predictions
              </p>
              <div className="bg-purple-100 text-purple-800 px-4 py-2 rounded-full text-sm font-semibold">
                Active
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-r from-green-600 to-emerald-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl font-bold mb-6">Ready to Experience Quantum Finance?</h2>
          <p className="text-xl text-green-100 mb-8 max-w-3xl mx-auto">
            Join the future of investment management with Goliath Capital's quantum-enhanced strategies
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/platform-dashboard" className="bg-white text-green-600 px-8 py-4 rounded-xl font-semibold hover:bg-gray-100 transition-colors">
              Access Platform Dashboard
            </Link>
            <Link href="/contact" className="bg-green-700 text-white px-8 py-4 rounded-xl font-semibold hover:bg-green-800 transition-colors">
              Schedule Consultation
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
