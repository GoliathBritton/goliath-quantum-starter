import React, { useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface QuantumCircuitNodeData {
  label: string;
  circuitType: string;
  icon?: string;
  description?: string;
  qubits?: number;
  depth?: number;
  gates?: string[];
  algorithm?: string;
  config?: any;
}

const QuantumCircuitNode: React.FC<NodeProps<QuantumCircuitNodeData>> = ({ data, selected }) => {
  const [showDetails, setShowDetails] = useState(false);

  const getCircuitIcon = (circuitType: string) => {
    const icons: { [key: string]: string } = {
      'qaoa': '🔄',
      'vqe': '⚡',
      'qft': '🌊',
      'grover': '🔍',
      'shor': '🔢',
      'quantum_teleportation': '📡',
      'bell_state': '🔗',
      'ghz_state': '🌐',
      'custom': '🛠️',
      'optimization': '📈',
      'simulation': '🧪'
    };
    return icons[circuitType] || '⚛️';
  };

  const getCircuitColor = (circuitType: string) => {
    const colors: { [key: string]: string } = {
      'qaoa': 'bg-purple-100 border-purple-500',
      'vqe': 'bg-yellow-100 border-yellow-500',
      'qft': 'bg-blue-100 border-blue-500',
      'grover': 'bg-green-100 border-green-500',
      'shor': 'bg-red-100 border-red-500',
      'quantum_teleportation': 'bg-pink-100 border-pink-500',
      'bell_state': 'bg-indigo-100 border-indigo-500',
      'ghz_state': 'bg-teal-100 border-teal-500',
      'custom': 'bg-gray-100 border-gray-500',
      'optimization': 'bg-orange-100 border-orange-500',
      'simulation': 'bg-cyan-100 border-cyan-500'
    };
    return colors[circuitType] || 'bg-purple-100 border-purple-500';
  };

  return (
    <div className={`px-4 py-3 shadow-md rounded-lg bg-white border-2 ${
      selected ? 'border-purple-600' : 'border-gray-200'
    } min-w-[200px]`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`rounded-lg w-12 h-12 flex justify-center items-center ${getCircuitColor(data.circuitType)}`}>
            <span className="text-lg">{getCircuitIcon(data.circuitType)}</span>
          </div>
          <div className="ml-3">
            <div className="text-sm font-bold">{data.label}</div>
            <div className="text-xs text-gray-500 capitalize">{data.circuitType.replace('_', ' ')}</div>
            {data.algorithm && (
              <div className="text-xs text-purple-600">Algorithm: {data.algorithm}</div>
            )}
          </div>
        </div>
        <button
          onClick={() => setShowDetails(!showDetails)}
          className="text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200"
        >
          {showDetails ? '▼' : '▶'}
        </button>
      </div>
      
      <div className="mt-2 flex gap-4 text-xs text-gray-600">
        {data.qubits && (
          <div className="flex items-center">
            <span className="w-2 h-2 bg-blue-400 rounded-full mr-1"></span>
            {data.qubits} qubits
          </div>
        )}
        {data.depth && (
          <div className="flex items-center">
            <span className="w-2 h-2 bg-green-400 rounded-full mr-1"></span>
            Depth: {data.depth}
          </div>
        )}
      </div>
      
      {showDetails && (
        <div className="mt-3 p-3 bg-gray-50 rounded text-xs">
          {data.description && (
            <div className="mb-2">
              <strong>Description:</strong> {data.description}
            </div>
          )}
          {data.gates && data.gates.length > 0 && (
            <div className="mb-2">
              <strong>Gates:</strong>
              <div className="flex flex-wrap gap-1 mt-1">
                {data.gates.map((gate, index) => (
                  <span key={index} className="bg-white px-2 py-1 rounded border text-xs">
                    {gate}
                  </span>
                ))}
              </div>
            </div>
          )}
          {data.config && (
            <div>
              <strong>Configuration:</strong>
              <pre className="mt-1 text-xs bg-white p-2 rounded border overflow-x-auto">
                {JSON.stringify(data.config, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
      
      <Handle
        type="target"
        position={Position.Left}
        className="w-4 h-4 !bg-purple-500"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-4 h-4 !bg-purple-500"
      />
    </div>
  );
};

export default QuantumCircuitNode;