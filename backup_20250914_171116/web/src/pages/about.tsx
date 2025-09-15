import React from 'react';
import Head from 'next/head';
import { Users, Target, Award, Zap, Brain, Shield, Globe, TrendingUp } from 'lucide-react';

const About = () => {
  const stats = [
    { label: 'Quantum Computations', value: '1M+', icon: Zap },
    { label: 'Enterprise Clients', value: '500+', icon: Users },
    { label: 'Countries Served', value: '25+', icon: Globe },
    { label: 'Success Rate', value: '99.9%', icon: Award }
  ];

  const team = [
    {
      name: 'Dr. Sarah Chen',
      role: 'Chief Quantum Officer',
      bio: 'Leading quantum computing research with 15+ years in quantum algorithms and business optimization.',
      image: '/api/placeholder/150/150'
    },
    {
      name: 'Marcus Rodriguez',
      role: 'Head of AI Strategy',
      bio: 'Former Google AI researcher specializing in large language models and enterprise AI deployment.',
      image: '/api/placeholder/150/150'
    },
    {
      name: 'Dr. Aisha Patel',
      role: 'Director of Business Intelligence',
      bio: 'Expert in quantum-enhanced analytics with a PhD in Applied Mathematics from MIT.',
      image: '/api/placeholder/150/150'
    },
    {
      name: 'James Thompson',
      role: 'VP of Enterprise Solutions',
      bio: '20+ years in enterprise software, leading digital transformation for Fortune 500 companies.',
      image: '/api/placeholder/150/150'
    }
  ];

  const values = [
    {
      icon: Brain,
      title: 'Innovation First',
      description: 'We push the boundaries of what\'s possible with quantum computing and AI to solve real business problems.'
    },
    {
      icon: Shield,
      title: 'Trust & Security',
      description: 'Enterprise-grade security and compliance are built into every solution we deliver.'
    },
    {
      icon: Users,
      title: 'Customer Success',
      description: 'Your success is our success. We partner with you every step of your quantum transformation journey.'
    },
    {
      icon: TrendingUp,
      title: 'Measurable Impact',
      description: 'Every solution delivers quantifiable business value with transparent ROI tracking.'
    }
  ];

  return (
    <>
      <Head>
        <title>About Us - Goliath QUANTUM</title>
        <meta name="description" content="Learn about Goliath QUANTUM's mission to democratize quantum intelligence for enterprise transformation. Meet our team and discover our values." />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
        {/* Hero Section */}
        <section className="relative py-20 px-4">
          <div className="max-w-6xl mx-auto text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6">
              <span className="text-white">About </span>
              <span className="text-gradient-gold">Goliath QUANTUM</span>
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-4xl mx-auto">
              We're pioneering the future of business intelligence through quantum computing, 
              making advanced quantum algorithms accessible to enterprises worldwide.
            </p>
          </div>
        </section>

        {/* Mission Section */}
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              <div>
                <h2 className="text-4xl font-bold text-white mb-6">
                  Our <span className="text-gradient-gold">Mission</span>
                </h2>
                <p className="text-lg text-gray-300 mb-6">
                  To democratize quantum intelligence and empower businesses to solve their most complex 
                  optimization challenges through cutting-edge quantum computing solutions.
                </p>
                <p className="text-lg text-gray-300 mb-8">
                  We believe that quantum computing shouldn't be limited to research labs. Every business 
                  deserves access to quantum-powered insights that can transform their operations, 
                  increase efficiency, and drive unprecedented growth.
                </p>
                <div className="flex items-center space-x-4">
                  <Target className="w-8 h-8 text-goliath-gold" />
                  <span className="text-white font-semibold">Quantum Intelligence for Everyone</span>
                </div>
              </div>
              <div className="relative">
                <div className="card-quantum p-8">
                  <h3 className="text-2xl font-bold text-white mb-4">Our Vision</h3>
                  <p className="text-gray-300 mb-6">
                    A world where every business decision is optimized by quantum intelligence, 
                    creating unprecedented efficiency and innovation across all industries.
                  </p>
                  <div className="quantum-glow w-full h-2 rounded-full"></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16 px-4 bg-black bg-opacity-50">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-white text-center mb-12">
              Quantum Impact <span className="text-gradient-gold">By Numbers</span>
            </h2>
            <div className="grid md:grid-cols-4 gap-8">
              {stats.map((stat, index) => {
                const IconComponent = stat.icon;
                return (
                  <div key={index} className="text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-goliath-gold to-yellow-400 rounded-full flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="w-8 h-8 text-gray-900" />
                    </div>
                    <div className="text-3xl font-bold text-white mb-2">{stat.value}</div>
                    <div className="text-gray-300">{stat.label}</div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-white text-center mb-12">
              Meet Our <span className="text-gradient-gold">Quantum Team</span>
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {team.map((member, index) => (
                <div key={index} className="card-quantum text-center">
                  <div className="w-24 h-24 bg-gradient-to-r from-goliath-gold to-yellow-400 rounded-full mx-auto mb-4 flex items-center justify-center">
                    <Users className="w-12 h-12 text-gray-900" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">{member.name}</h3>
                  <p className="text-goliath-gold font-semibold mb-3">{member.role}</p>
                  <p className="text-gray-300 text-sm">{member.bio}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Values Section */}
        <section className="py-16 px-4 bg-black bg-opacity-50">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-white text-center mb-12">
              Our <span className="text-gradient-gold">Core Values</span>
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
              {values.map((value, index) => {
                const IconComponent = value.icon;
                return (
                  <div key={index} className="card-quantum text-center">
                    <div className="w-16 h-16 bg-gradient-to-r from-sigma-purple to-purple-400 rounded-full flex items-center justify-center mx-auto mb-4">
                      <IconComponent className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-xl font-bold text-white mb-3">{value.title}</h3>
                    <p className="text-gray-300 text-sm">{value.description}</p>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Technology Section */}
        <section className="py-16 px-4">
          <div className="max-w-6xl mx-auto">
            <div className="card-quantum">
              <h2 className="text-4xl font-bold text-white text-center mb-8">
                Powered by <span className="text-gradient-gold">Quantum Technology</span>
              </h2>
              <div className="grid md:grid-cols-3 gap-8">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-cyan-500 to-blue-400 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Zap className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">DYNEX Integration</h3>
                  <p className="text-gray-300">
                    Direct integration with DYNEX quantum computing platform for real-time QUBO optimization.
                  </p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Brain className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">AI-Quantum Hybrid</h3>
                  <p className="text-gray-300">
                    Combining classical AI with quantum algorithms for unprecedented problem-solving capabilities.
                  </p>
                </div>
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-400 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Shield className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">Enterprise Security</h3>
                  <p className="text-gray-300">
                    Post-quantum cryptography and enterprise-grade security for all quantum computations.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-16 px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Join the <span className="text-gradient-gold">Quantum Revolution?</span>
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Let's discuss how quantum intelligence can transform your business operations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <a href="/contact" className="btn-primary">
                Contact Our Team
              </a>
              <a href="/dashboard" className="btn-secondary">
                Explore Platform
              </a>
            </div>
          </div>
        </section>
      </div>
    </>
  );
};

export default About;