// src/pages/quantum-demo.tsx
import QuantumBadge from "../components/QuantumBadge";
import AgentCard from "../components/AgentCard";
import RoleTooltip from "../components/RoleTooltip";
import "../styles/globals.css";

export default function QuantumDemoPage() {
  const sampleAgents = [
    { 
      name: "Quantum Digital Agent", 
      role: "Autonomous Deal Closer", 
      img: "/agents/placeholder.svg", 
      quantum: true 
    },
    { 
      name: "QSAI Calling Agent", 
      role: "Voice AI Sales Specialist", 
      img: "/agents/placeholder.svg", 
      quantum: true 
    },
    { 
      name: "AI Business Agent", 
      role: "SMB Automation Expert", 
      img: "/agents/placeholder.svg" 
    }
  ];

  const roleTooltips = [
    {
      label: "Quantum Enhanced",
      roleInsight: "Powered by quantum algorithms for superior performance and decision-making capabilities."
    },
    {
      label: "AI-Powered",
      roleInsight: "Leverages advanced machine learning models to automate complex business processes."
    },
    {
      label: "Enterprise Ready",
      roleInsight: "Built for scale with enterprise-grade security, compliance, and integration capabilities."
    }
  ];

  return (
    <div className="min-h-screen bg-gray-950 relative overflow-hidden">
      {/* Quantum Background */}
      <div className="absolute inset-0 bg-quantum min-h-screen w-full opacity-30"></div>
      
      {/* Content */}
      <div className="relative z-10 p-10">
        {/* Header Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold text-white mb-6 quantum-glow">
            🚀 Quantum UI Kit Demo
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Experience the future of AI interfaces with our quantum-enhanced components
          </p>
          <div className="flex justify-center">
            <QuantumBadge />
          </div>
        </div>

        {/* Role Tooltips Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">
            Interactive Role Insights
          </h2>
          <div className="flex flex-wrap justify-center gap-4">
            {roleTooltips.map((tooltip, i) => (
              <div key={i} className="quantum-float" style={{ animationDelay: `${i * 0.3}s` }}>
                <RoleTooltip {...tooltip} />
              </div>
            ))}
          </div>
        </div>

        {/* Agent Cards Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">
            Quantum Agent Showcase
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {sampleAgents.map((agent, i) => (
              <div key={i} className="quantum-float" style={{ animationDelay: `${i * 0.2}s` }}>
                <AgentCard {...agent} />
              </div>
            ))}
          </div>
        </div>

        {/* Features Grid */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-white mb-8 text-center">
            Quantum UI Features
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            <div className="bg-gray-900 p-6 rounded-xl quantum-glow">
              <h3 className="text-lg font-semibold text-white mb-2">⚛️ Quantum Badges</h3>
              <p className="text-gray-400 text-sm">Premium visual indicators with gradient animations</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl quantum-glow">
              <h3 className="text-lg font-semibold text-white mb-2">🎯 Interactive Cards</h3>
              <p className="text-gray-400 text-sm">Hover effects and quantum badge reveals</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl quantum-glow">
              <h3 className="text-lg font-semibold text-white mb-2">💡 Smart Tooltips</h3>
              <p className="text-gray-400 text-sm">Contextual insights with elegant animations</p>
            </div>
            <div className="bg-gray-900 p-6 rounded-xl quantum-glow">
              <h3 className="text-lg font-semibold text-white mb-2">🌊 Quantum Flow</h3>
              <p className="text-gray-400 text-sm">Living background animations and effects</p>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <button className="px-12 py-6 bg-gradient-to-r from-violet-600 to-teal-400 text-white font-bold text-xl rounded-2xl hover:scale-105 transition-transform quantum-pulse shadow-2xl">
            Deploy Quantum UI Kit
          </button>
          <p className="text-gray-400 mt-4">
            Ready for Next.js + Tailwind integration
          </p>
        </div>
      </div>
    </div>
  );
}