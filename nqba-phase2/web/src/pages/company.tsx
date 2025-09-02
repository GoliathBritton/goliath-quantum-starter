import Link from "next/link";
import Header from "../components/Header";
import Footer from "../components/Footer";

export default function Company() {
  const caseStudies = [
    {
      title: "Quantum Advantage in Financial Services",
      company: "Global Investment Bank",
      industry: "Financial Services",
      challenge: "Portfolio optimization with 10,000+ assets taking 8 hours to compute",
      solution: "FLYFOX AI QUBO optimization with Dynex quantum backend",
      results: [
        "410x performance improvement",
        "Portfolio optimization in 70 seconds vs 8 hours",
        "$2.3M annual cost savings",
        "Real-time risk assessment capabilities"
      ],
      metrics: {
        performance: "410x",
        timeReduction: "99.8%",
        costSavings: "$2.3M",
        accuracy: "99.9%"
      }
    },
    {
      title: "AI Agent Workforce Transformation",
      company: "Manufacturing Conglomerate",
      industry: "Manufacturing",
      challenge: "Manual quality control processes causing 15% defect rate and production delays",
      solution: "FLYFOX AI autonomous agents with computer vision and predictive analytics",
      results: [
        "Defect rate reduced to 2.1%",
        "Production efficiency increased by 34%",
        "Quality control costs reduced by 67%",
        "24/7 automated monitoring"
      ],
      metrics: {
        performance: "34%",
        timeReduction: "67%",
        costSavings: "$1.8M",
        accuracy: "97.9%"
      }
    },
    {
      title: "NQBA Architecture Implementation",
      company: "Healthcare Technology Provider",
      industry: "Healthcare",
      challenge: "Complex patient data processing requiring HIPAA compliance and real-time analysis",
      solution: "FLYFOX AI NQBA core with quantum-enhanced machine learning",
      results: [
        "Patient diagnosis accuracy improved by 28%",
        "Processing time reduced from 24 hours to 15 minutes",
        "HIPAA compliance automated and auditable",
        "Real-time patient monitoring enabled"
      ],
      metrics: {
        performance: "96x",
        timeReduction: "96.3%",
        costSavings: "$3.1M",
        accuracy: "28%"
      }
    }
  ];

  const partners = [
    {
      name: "NVIDIA",
      logo: "🟢",
      category: "Technology Partner",
      description: "GPU acceleration and quantum computing optimization",
      benefits: ["CUDA integration", "Quantum advantage", "Performance optimization"]
    },
    {
      name: "Dynex",
      logo: "⚛️",
      category: "Quantum Partner",
      description: "Quantum computing backend and QUBO optimization",
      benefits: ["QUBO solver", "Quantum advantage", "Real-time processing"]
    },
    {
      name: "n8n",
      logo: "🔗",
      category: "Automation Partner",
      description: "Workflow automation and process orchestration",
      benefits: ["No-code automation", "API integration", "Scalable workflows"]
    },
    {
      name: "UiPath",
      logo: "🤖",
      category: "RPA Partner",
      description: "Robotic process automation and intelligent automation",
      benefits: ["RPA + AI", "Cognitive automation", "Process optimization"]
    },
    {
      name: "Mendix",
      logo: "🏗️",
      category: "Low-Code Partner",
      description: "Rapid application development and AI integration",
      benefits: ["Low-code AI", "Rapid development", "Scalable applications"]
    },
    {
      name: "Prismatic",
      logo: "🔌",
      category: "Integration Partner",
      description: "Enterprise integration and API management",
      benefits: ["Enterprise integration", "API management", "Custom connectors"]
    }
  ];

  const team = [
    {
      name: "Dr. Quantum Architect",
      role: "Chief Quantum Officer",
      expertise: "Quantum Computing, QUBO Optimization, NQBA Architecture",
      background: "PhD in Quantum Physics, 15+ years in quantum computing research",
      achievements: ["410x performance multiplier", "NQBA core design", "Quantum advantage protocols"]
    },
    {
      name: "AI Strategy Director",
      role: "Chief AI Officer",
      expertise: "Machine Learning, Autonomous Agents, MCP Integration",
      background: "MS in AI/ML, 12+ years in enterprise AI implementation",
      achievements: ["Self-learning agents", "MCP orchestration", "Agent workforce optimization"]
    },
    {
      name: "Business Transformation Lead",
      role: "Chief Business Officer",
      expertise: "Process Automation, Business Intelligence, ROI Optimization",
      background: "MBA in Business Strategy, 18+ years in business transformation",
      achievements: ["1150% ROI", "Business automation", "Process optimization"]
    }
  ];

  return (
    <>
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            FLYFOX AI Company
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 max-w-4xl mx-auto leading-relaxed">
            We're building the intelligent economy where quantum computing meets autonomous intelligence 
            to create unprecedented business value and performance.
          </p>
          
          <div className="mt-8 flex flex-col sm:flex-row gap-4 justify-center">
            <a 
              href="#case-studies"
              className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              📊 View Case Studies
            </a>
            <a 
              href="#partners"
              className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              🤝 Our Partners
            </a>
          </div>
        </div>
      </section>

      {/* Company Overview */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                Building the Intelligent Economy
              </h2>
              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                FLYFOX AI is not just a platform—it's a complete transformation of how businesses operate. 
                We combine quantum computing, autonomous AI agents, and neuromorphic architecture to deliver 
                unprecedented performance and business value.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700">410x performance multiplier over classical computing</span>
                </div>
                
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700">Self-learning AI agents that become industry experts</span>
                </div>
                
                <div className="flex items-center space-x-3">
                  <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <span className="text-gray-700">NQBA architecture for automated business decisions</span>
                </div>
              </div>
            </div>
            
            <div className="bg-gradient-to-br from-cyan-50 to-purple-50 rounded-2xl p-8 border border-cyan-200">
              <h3 className="text-2xl font-bold text-gray-900 mb-6">Our Mission</h3>
              <p className="text-gray-700 mb-6 leading-relaxed">
                To democratize quantum computing and AI, making enterprise-grade performance accessible 
                to businesses of all sizes while maintaining the highest standards of security and compliance.
              </p>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span className="text-gray-700">Performance Multiplier</span>
                  <span className="text-2xl font-bold text-cyan-600">410x</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span className="text-gray-700">ROI for Clients</span>
                  <span className="text-2xl font-bold text-purple-600">1150%</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-white rounded-lg">
                  <span className="text-gray-700">Uptime</span>
                  <span className="text-2xl font-bold text-green-600">99.9%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Case Studies Section */}
      <section id="case-studies" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Real Results, Real Impact
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              See how FLYFOX AI is transforming businesses across industries with quantum computing 
              and autonomous AI agents.
            </p>
          </div>
          
          <div className="space-y-8">
            {caseStudies.map((study, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                  <div className="lg:col-span-2">
                    <div className="flex items-center space-x-3 mb-4">
                      <span className="text-sm font-medium text-gray-500">{study.industry}</span>
                      <span className="w-2 h-2 bg-gray-300 rounded-full"></span>
                      <span className="text-sm font-medium text-gray-500">{study.company}</span>
                    </div>
                    
                    <h3 className="text-2xl font-bold text-gray-900 mb-4">{study.title}</h3>
                    
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">The Challenge</h4>
                        <p className="text-gray-600">{study.challenge}</p>
                      </div>
                      
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">Our Solution</h4>
                        <p className="text-gray-600">{study.solution}</p>
                      </div>
                      
                      <div>
                        <h4 className="font-semibold text-gray-900 mb-2">Results</h4>
                        <ul className="space-y-2">
                          {study.results.map((result, resultIndex) => (
                            <li key={resultIndex} className="flex items-start space-x-2">
                              <span className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></span>
                              <span className="text-gray-700">{result}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                  
                  <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl p-6">
                    <h4 className="text-lg font-bold text-gray-900 mb-4 text-center">Impact Metrics</h4>
                    <div className="space-y-4">
                      <div className="text-center">
                        <div className="text-3xl font-bold text-cyan-600">{study.metrics.performance}</div>
                        <div className="text-sm text-gray-600">Performance Improvement</div>
                      </div>
                      
                      <div className="text-center">
                        <div className="text-3xl font-bold text-purple-600">{study.metrics.timeReduction}</div>
                        <div className="text-sm text-gray-600">Time Reduction</div>
                      </div>
                      
                      <div className="text-center">
                        <div className="text-3xl font-bold text-green-600">{study.metrics.costSavings}</div>
                        <div className="text-sm text-gray-600">Annual Savings</div>
                      </div>
                      
                      <div className="text-center">
                        <div className="text-3xl font-bold text-orange-600">{study.metrics.accuracy}</div>
                        <div className="text-sm text-gray-600">Accuracy Improvement</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Partners Section */}
      <section id="partners" className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Strategic Partnerships
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              We collaborate with industry leaders to deliver the most advanced quantum computing 
              and AI solutions to our clients.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {partners.map((partner, index) => (
              <div key={index} className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl p-8 border border-gray-200 hover:shadow-xl transition-all transform hover:scale-105">
                <div className="text-center mb-6">
                  <div className="w-20 h-20 bg-white rounded-2xl flex items-center justify-center text-4xl mx-auto mb-4 shadow-lg">
                    {partner.logo}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">{partner.name}</h3>
                  <span className="inline-block bg-cyan-100 text-cyan-800 px-3 py-1 rounded-full text-sm font-medium mt-2">
                    {partner.category}
                  </span>
                </div>
                
                <p className="text-gray-600 mb-6 text-center">{partner.description}</p>
                
                <div className="space-y-2">
                  {partner.benefits.map((benefit, benefitIndex) => (
                    <div key={benefitIndex} className="flex items-center space-x-2">
                      <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                      <span className="text-sm text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Leadership Team
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Meet the experts driving innovation in quantum computing and AI at FLYFOX AI.
            </p>
          </div>
          
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {team.map((member, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-xl p-8 border border-gray-200 hover:shadow-2xl transition-all transform hover:scale-105">
                <div className="text-center mb-6">
                  <div className="w-24 h-24 bg-gradient-to-br from-cyan-500 to-purple-600 rounded-full flex items-center justify-center text-white text-3xl font-bold mx-auto mb-4">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">{member.name}</h3>
                  <p className="text-lg text-cyan-600 font-semibold">{member.role}</p>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Expertise</h4>
                    <p className="text-gray-600 text-sm">{member.expertise}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Background</h4>
                    <p className="text-gray-600 text-sm">{member.background}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Key Achievements</h4>
                    <ul className="space-y-1">
                      {member.achievements.map((achievement, achievementIndex) => (
                        <li key={achievementIndex} className="flex items-start space-x-2">
                          <span className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></span>
                          <span className="text-gray-700 text-sm">{achievement}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-20 bg-gradient-to-br from-flyfox-950 via-goliath-950 to-goliathNavy-950 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Join the companies already experiencing 410x performance improvements and 1150% ROI 
            with FLYFOX AI's quantum computing and AI solutions.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
            <Link 
              href="/contact"
              className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              📞 Schedule a Demo
            </Link>
            <Link 
              href="/pricing"
              className="border border-white/30 text-white hover:bg-white/10 px-8 py-4 rounded-xl font-semibold text-lg transition-all transform hover:scale-105"
            >
              💰 View Pricing
            </Link>
          </div>
          
          <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-6 max-w-2xl mx-auto">
            <p className="text-cyan-300 text-sm">
              <strong>Case Study:</strong> See how we helped a global investment bank achieve 
              410x performance improvement in portfolio optimization. 
              <Link href="#case-studies" className="text-purple-300 hover:text-purple-200 underline ml-1">
                Read the full story →
              </Link>
            </p>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
