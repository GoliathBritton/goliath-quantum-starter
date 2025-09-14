import React from 'react';
import { Handle, Position } from 'reactflow';

interface QuantumNodeProps {
  data: {
    label: string;
    quantumType?: string;
    config?: any;
  };
}

const QuantumNode: React.FC<QuantumNodeProps> = ({ data }) => {
  return (
    <div className="bg-gradient-to-r from-flyfox-500 to-quantum-500 text-white p-4 rounded-lg shadow-lg min-w-[200px] border border-quantum-300">
      <div className="font-bold text-sm mb-2">🔮 Quantum Omniscient™</div>
      <div className="text-xs">{data.label}</div>
      {data.quantumType && (
        <div className="text-xs opacity-75 mt-1">{data.quantumType}</div>
      )}
      <div className="text-xs opacity-60 mt-1">Echelon Quantum™ Core</div>
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-quantum-300"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-quantum-300"
      />
    </div>
  );
};

export default QuantumNode;