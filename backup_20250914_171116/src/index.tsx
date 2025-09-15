// src/index.tsx - Quantum UI Kit Entry Point
import QuantumBadge from "./components/QuantumBadge";
import AgentCard from "./components/AgentCard";
import RoleTooltip from "./components/RoleTooltip";
import "./styles/globals.css";

// Export all Quantum UI Kit components
export {
  QuantumBadge,
  AgentCard,
  RoleTooltip
};

// Demo component showcasing all features
export default function QuantumUIKit() {
  return (
    <div className="min-h-screen bg-gray-950 relative overflow-hidden">
      {/* Quantum Background */}
      <div className="absolute inset-0 bg-quantum min-h-screen w-full opacity-20"></div>
      
      {/* Content */}
      <div className="relative z-10 p-10 text-center">
        <h1 className="text-4xl font-bold text-white mb-8 quantum-glow">
          🚀 Quantum UI Kit - Phase 1
        </h1>
        
        <div className="mb-8">
          <h2 className="text-2xl text-white mb-4">Quantum Badge Component</h2>
          <QuantumBadge />
        </div>
        
        <div className="mb-8">
          <h2 className="text-2xl text-white mb-4">Role Tooltip Component</h2>
          <RoleTooltip 
            label="Quantum Enhanced" 
            roleInsight="Powered by quantum algorithms for superior performance and decision-making capabilities." 
          />
        </div>
        
        <div className="mb-8">
          <h2 className="text-2xl text-white mb-4">Agent Card Component</h2>
          <div className="flex justify-center">
            <AgentCard 
              name="Quantum Digital Agent" 
              role="Autonomous Deal Closer" 
              img="/agents/placeholder.svg" 
              quantum={true} 
            />
          </div>
        </div>
        
        <div className="mt-12">
          <p className="text-gray-300 text-lg">
            ✅ Ready for Next.js + Tailwind deployment<br/>
            ✅ All components tested and integrated<br/>
            ✅ Quantum animations and effects active
          </p>
        </div>
      </div>
    </div>
  );
}