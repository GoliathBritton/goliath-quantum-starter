import React, { useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface QuantumGateNodeData {
  label: string;
  gateType: string;
  icon?: string;
  description?: string;
  qubits?: number;
  parameters?: { [key: string]: number };
  config?: any;
}

const QuantumGateNode: React.FC<NodeProps<QuantumGateNodeData>> = ({ data, selected }) => {
  const [showConfig, setShowConfig] = useState(false);

  const getGateIcon = (gateType: string) => {
    const icons: { [key: string]: string } = {
      'hadamard': 'H',
      'pauli_x': 'X',
      'pauli_y': 'Y',
      'pauli_z': 'Z',
      'cnot': '⊕',
      'rotation_x': 'Rx',
      'rotation_y': 'Ry',
      'rotation_z': 'Rz',
      'phase': 'P',
      'toffoli': 'T',
      'swap': '⇄'
    };
    return icons[gateType] || '🚪';
  };

  const getGateColor = (gateType: string) => {
    const colors: { [key: string]: string } = {
      'hadamard': 'bg-blue-100 border-blue-500',
      'pauli_x': 'bg-red-100 border-red-500',
      'pauli_y': 'bg-green-100 border-green-500',
      'pauli_z': 'bg-purple-100 border-purple-500',
      'cnot': 'bg-orange-100 border-orange-500',
      'rotation_x': 'bg-pink-100 border-pink-500',
      'rotation_y': 'bg-teal-100 border-teal-500',
      'rotation_z': 'bg-indigo-100 border-indigo-500',
      'phase': 'bg-yellow-100 border-yellow-500',
      'toffoli': 'bg-gray-100 border-gray-500',
      'swap': 'bg-cyan-100 border-cyan-500'
    };
    return colors[gateType] || 'bg-gray-100 border-gray-500';
  };

  return (
    <div className={`px-3 py-2 shadow-md rounded-md bg-white border-2 ${
      selected ? 'border-blue-600' : 'border-gray-200'
    }`}>
      <div className="flex items-center">
        <div className={`rounded-md w-10 h-10 flex justify-center items-center ${getGateColor(data.gateType)}`}>
          <span className="text-sm font-bold">{getGateIcon(data.gateType)}</span>
        </div>
        <div className="ml-2">
          <div className="text-sm font-bold">{data.label}</div>
          <div className="text-xs text-gray-500">{data.gateType}</div>
          {data.qubits && (
            <div className="text-xs text-blue-600">Qubits: {data.qubits}</div>
          )}
        </div>
        {data.parameters && Object.keys(data.parameters).length > 0 && (
          <button
            onClick={() => setShowConfig(!showConfig)}
            className="ml-2 text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200"
          >
            ⚙️
          </button>
        )}
      </div>
      
      {showConfig && data.parameters && (
        <div className="mt-2 p-2 bg-gray-50 rounded text-xs">
          {Object.entries(data.parameters).map(([key, value]) => (
            <div key={key} className="flex justify-between">
              <span>{key}:</span>
              <span>{value}</span>
            </div>
          ))}
        </div>
      )}
      
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 !bg-blue-500"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 !bg-blue-500"
      />
    </div>
  );
};

export default QuantumGateNode;