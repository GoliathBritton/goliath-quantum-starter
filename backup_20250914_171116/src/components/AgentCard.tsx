// src/components/AgentCard.tsx
import QuantumBadge from "./QuantumBadge";

interface AgentCardProps {
  name: string;
  role: string;
  img: string;
  quantum?: boolean;
}

export default function AgentCard({ name, role, img, quantum }: AgentCardProps) {
  return (
    <div className="relative group bg-gray-900 rounded-2xl p-4 transition-transform hover:scale-105 shadow-xl">
      <img src={img} alt={name} className="w-16 h-16 mx-auto rounded-full" />
      <h3 className="mt-3 text-lg font-semibold text-white">{name}</h3>
      <p className="text-sm text-gray-400">{role}</p>
      {quantum && (
        <span className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition">
          <QuantumBadge />
        </span>
      )}
    </div>
  );
}