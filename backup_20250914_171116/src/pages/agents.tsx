// src/pages/agents.tsx
import AgentCard from "../components/AgentCard";
import "../styles/globals.css";

export default function AgentsPage() {
  const agents = [
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
    },
    { 
      name: "Digital Human", 
      role: "Customer Engagement Avatar", 
      img: "/agents/placeholder.svg", 
      quantum: true 
    },
    { 
      name: "Sigma Select Agent", 
      role: "Premium Investment Advisor", 
      img: "/agents/placeholder.svg", 
      quantum: true 
    },
    { 
      name: "Goliath Energy Agent", 
      role: "Energy Trading Specialist", 
      img: "/agents/placeholder.svg", 
      quantum: true 
    },
    { 
      name: "FLYFOX AI Agent", 
      role: "Marketing Automation Expert", 
      img: "/agents/placeholder.svg", 
      quantum: true 
    },
    { 
      name: "SFG Insurance Agent", 
      role: "Risk Assessment Specialist", 
      img: "/agents/placeholder.svg" 
    }
  ];

  return (
    <div className="min-h-screen bg-gray-950 relative overflow-hidden">
      {/* Quantum Background */}
      <div className="absolute inset-0 bg-quantum min-h-screen w-full opacity-20"></div>
      
      {/* Content */}
      <div className="relative z-10 p-10">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-4 quantum-glow">
            ⚡ Agent Marketplace
          </h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Discover our quantum-enhanced AI agents designed to revolutionize your business operations
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 max-w-7xl mx-auto">
          {agents.map((agent, i) => (
            <div key={i} className="quantum-float" style={{ animationDelay: `${i * 0.2}s` }}>
              <AgentCard {...agent} />
            </div>
          ))}
        </div>
        
        {/* Call to Action */}
        <div className="text-center mt-16">
          <button className="px-8 py-4 bg-gradient-to-r from-violet-600 to-teal-400 text-white font-bold rounded-xl hover:scale-105 transition-transform quantum-pulse">
            Deploy Your Quantum Agent Suite
          </button>
        </div>
      </div>
    </div>
  );
}