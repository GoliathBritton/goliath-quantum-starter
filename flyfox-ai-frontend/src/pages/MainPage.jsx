import React from 'react';
import { ChevronDown, Search, ArrowRight, Cpu } from 'lucide-react';
import { motion } from 'framer-motion';
import Header from '../components/Header';

const MainPage = () => {
  return (
    <div className="bg-white">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-purple-300 via-indigo-400 to-blue-500 text-white px-4 py-3">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="font-bold">FLYFOX AI INNOVATE</span>
            <span className="text-sm">Global experts in advanced quantum technology, united in one platform. Launching soon.</span>
          </div>
          <button className="bg-blue-400 text-white px-4 py-2 rounded font-semibold text-sm hover:bg-blue-300">
            Sign up now
          </button>
        </div>
      </div>

      {/* Secondary Navigation */}
      <div className="bg-indigo-600 text-white px-4 py-2">
        <div className="max-w-7xl mx-auto flex items-center justify-end space-x-6">
          <div className="flex items-center space-x-1">
            <span>Company</span>
            <ChevronDown className="w-4 h-4" />
          </div>
          <a href="/blog" className="hover:underline">Blog</a>
          <a href="/customer-portal" className="hover:underline">Customer Portal</a>
          <button className="p-1">
            <Search className="w-4 h-4" />
          </button>
          <div className="flex items-center space-x-1">
            <span>En</span>
            <ChevronDown className="w-4 h-4" />
          </div>
        </div>
      </div>

      {/* Main Header */}
      <Header />

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-900 via-blue-800 to-blue-600 text-white relative overflow-hidden">
        <img src="/ai-background.svg" alt="AI Background" className="absolute inset-0 w-full h-full object-cover opacity-20" loading="lazy" />
        <div className="max-w-7xl mx-auto px-4 py-20 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center flex-col lg:flex-row">
            {/* Left Content */}
            <motion.div 
              className="order-2 lg:order-1"
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="text-sm font-medium mb-4 opacity-90">FLYFOX AI Platform</div>
              <motion.h1 
                className="text-5xl font-bold mb-6 leading-tight"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
              >
                Advanced<br />
                neuromorphic computing solutions
              </motion.h1>
              <motion.p 
                className="text-lg mb-8 opacity-90 leading-relaxed"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
              >
                Enable your teams to tackle challenging tasks efficiently using cutting-edge neuromorphic technology. <strong>FLYFOX AI Platform</strong> offers robust tools for optimization, AI development, and simulations, driving breakthroughs in various fields.
              </motion.p>
              <motion.div 
                className="flex items-center space-x-4"
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.6 }}
              >
                <button className="bg-blue-400 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-300">
                  Request demo
                </button>
                <button className="text-blue-400 hover:text-blue-300 flex items-center font-semibold">
                  Explore features
                  <ArrowRight className="w-4 h-4 ml-2" />
                </button>
              </motion.div>
            </motion.div>
            {/* Right Content - Dashboard Image */}
            <div className="order-1 lg:order-2 relative">
              <div className="bg-gradient-to-br from-indigo-700 to-indigo-900 rounded-lg p-6 shadow-2xl">
                {/* Code Editor Interface */}
                <div className="bg-gray-900 rounded-lg p-4 mb-4">
                  <div className="flex items-center space-x-2 mb-3">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <div className="text-green-400 text-sm font-mono space-y-1">
                    <div>import flyfox</div>
                    <div>model = flyfox.BQM()</div>
                    <div>model.add_variable('x')</div>
                    <div>model.add_variable('y')</div>
                    <div>model.set_linear('x', 1)</div>
                    <div>model.set_quadratic('x', 'y', -2)</div>
                    <div>samples = flyfox.sample(model, num_reads=1000)</div>
                  </div>
                </div>

                {/* Test Results Cards */}
                <div className="space-y-3">
                  <div className="bg-white rounded-lg p-3 flex items-center justify-between shadow-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-gray-800 rounded flex items-center justify-center">
                        <Cpu className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-gray-800 font-medium">Quantum Job 01</span>
                    </div>
                    <span className="bg-green-500 text-white px-3 py-1 rounded text-sm font-medium">SUCCESS</span>
                  </div>

                  <div className="bg-white rounded-lg p-3 flex items-center justify-between shadow-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-gray-800 rounded flex items-center justify-center">
                        <Cpu className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-gray-800 font-medium">Quantum Job 02</span>
                    </div>
                    <span className="bg-green-500 text-white px-3 py-1 rounded text-sm font-medium">SUCCESS</span>
                  </div>

                  <div className="bg-white rounded-lg p-3 flex items-center justify-between shadow-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-gray-800 rounded flex items-center justify-center">
                        <Cpu className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-gray-800 font-medium">Quantum Job 03</span>
                    </div>
                    <span className="bg-green-500 text-white px-3 py-1 rounded text-sm font-medium">SUCCESS</span>
                  </div>

                  <div className="bg-white rounded-lg p-3 flex items-center justify-between shadow-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-gray-800 rounded flex items-center justify-center">
                        <Cpu className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-gray-800 font-medium">Quantum Job 04</span>
                    </div>
                    <span className="bg-green-500 text-white px-3 py-1 rounded text-sm font-medium">SUCCESS</span>
                  </div>

                  <div className="bg-white rounded-lg p-3 flex items-center justify-between shadow-lg">
                    <div className="flex items-center space-x-3">
                      <div className="w-8 h-8 bg-gray-800 rounded flex items-center justify-center">
                        <Cpu className="w-4 h-4 text-white" />
                      </div>
                      <span className="text-gray-800 font-medium">Quantum Job 05</span>
                    </div>
                    <span className="bg-green-500 text-white px-3 py-1 rounded text-sm font-medium">SUCCESS</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Background Elements */}
        <div className="absolute top-0 left-0 w-full h-full opacity-10">
          <div className="absolute top-10 left-10 text-6xl font-bold">INDUSTRY SOLUTIONS</div>
          <div className="absolute top-30 left-30 text-4xl">APPLICATION AREAS</div>
          <div className="absolute top-50 right-30 text-4xl">PRODUCT OFFERINGS</div>
          <div className="absolute bottom-50 left-10 text-3xl">Machine Learning</div>
          <div className="absolute bottom-70 right-10 text-3xl">Supply Chain</div>
          <div className="absolute bottom-90 left-50 text-3xl">Modeling</div>
          <div className="absolute top-70 right-50 text-3xl">Banking</div>
          <div className="absolute bottom-10 right-70 text-3xl">Pharma</div>
        </div>
      </section>

      {/* Dynex Section */}
      <section className="bg-gradient-to-r from-indigo-600 to-indigo-800 text-white py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between">
            <h2 className="text-4xl font-bold">FLYFOX AI SDK</h2>
            <button className="bg-indigo-400 text-white px-8 py-3 rounded-lg font-semibold hover:bg-indigo-300">
              Watch webinar
            </button>
          </div>
        </div>
      </section>

      {/* Partners Section */}
      <section className="py-16 bg-neutral">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12 text-dark-blue">Our Brands</h2>
          <div className="flex justify-center space-x-16">
            <img src="/flyfox-logo.svg" alt="Fly Fox AI" className="h-24" />
            <img src="/sigma-logo.svg" alt="Sigma Select" className="h-24" />
            <img src="/goliath-logo.svg" alt="Goliath of All Trade" className="h-24" />
          </div>
        </div>
      </section>

      {/* Bottom Bar */}
      <div className="bg-purple-400 h-4"></div>
    </div>
  );
};

export default MainPage;