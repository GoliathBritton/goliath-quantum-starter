import React, { useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface QuantumAlgorithmNodeData {
  label: string;
  algorithmType: string;
  icon?: string;
  description?: string;
  category?: string;
  quantumAdvantage?: string;
  complexity?: string;
  parameters?: { [key: string]: any };
  config?: any;
}

const QuantumAlgorithmNode: React.FC<NodeProps<QuantumAlgorithmNodeData>> = ({ data, selected }) => {
  const [showConfig, setShowConfig] = useState(false);

  const getAlgorithmIcon = (algorithmType: string) => {
    const icons: { [key: string]: string } = {
      'portfolio_optimization': '📊',
      'energy_management': '⚡',
      'risk_assessment': '🛡️',
      'personalization': '👤',
      'supply_chain': '🚚',
      'fraud_detection': '🔍',
      'pricing_optimization': '💰',
      'route_optimization': '🗺️',
      'machine_learning': '🤖',
      'cryptography': '🔐',
      'quantum_llm': '🧠',
      'process_optimization': '⚙️',
      'simulation': '🧪',
      'optimization': '📈'
    };
    return icons[algorithmType] || '🔬';
  };

  const getAlgorithmColor = (category: string) => {
    const colors: { [key: string]: string } = {
      'Finance': 'bg-green-100 border-green-500',
      'Optimization': 'bg-blue-100 border-blue-500',
      'Machine Learning': 'bg-purple-100 border-purple-500',
      'Cryptography': 'bg-red-100 border-red-500',
      'Chemistry': 'bg-yellow-100 border-yellow-500',
      'Physics': 'bg-indigo-100 border-indigo-500',
      'Logistics': 'bg-orange-100 border-orange-500',
      'Healthcare': 'bg-pink-100 border-pink-500',
      'Energy': 'bg-teal-100 border-teal-500'
    };
    return colors[category || 'Optimization'] || 'bg-gray-100 border-gray-500';
  };

  const getComplexityColor = (complexity: string) => {
    const colors: { [key: string]: string } = {
      'low': 'text-green-600 bg-green-100',
      'medium': 'text-yellow-600 bg-yellow-100',
      'high': 'text-red-600 bg-red-100',
      'exponential': 'text-purple-600 bg-purple-100'
    };
    return colors[complexity?.toLowerCase() || 'medium'] || 'text-gray-600 bg-gray-100';
  };

  return (
    <div className={`px-4 py-3 shadow-lg rounded-lg bg-white border-2 ${
      selected ? 'border-indigo-600' : 'border-gray-200'
    } min-w-[250px]`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <div className={`rounded-lg w-14 h-14 flex justify-center items-center ${getAlgorithmColor(data.category)}`}>
            <span className="text-xl">{getAlgorithmIcon(data.algorithmType)}</span>
          </div>
          <div className="ml-3">
            <div className="text-sm font-bold">{data.label}</div>
            <div className="text-xs text-gray-500 capitalize">
              {data.algorithmType.replace(/_/g, ' ')}
            </div>
            {data.category && (
              <div className="text-xs text-indigo-600 font-medium">{data.category}</div>
            )}
          </div>
        </div>
        {(data.parameters || data.config) && (
          <button
            onClick={() => setShowConfig(!showConfig)}
            className="text-xs bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full hover:bg-indigo-200 transition-colors"
          >
            {showConfig ? 'Hide' : 'Config'}
          </button>
        )}
      </div>
      
      <div className="mt-3 space-y-2">
        {data.quantumAdvantage && (
          <div className="flex items-center text-xs">
            <span className="w-2 h-2 bg-quantum-gradient rounded-full mr-2"></span>
            <span className="text-gray-600">Quantum Advantage: </span>
            <span className="text-indigo-600 font-medium ml-1">{data.quantumAdvantage}</span>
          </div>
        )}
        
        {data.complexity && (
          <div className="flex items-center text-xs">
            <span className="w-2 h-2 bg-gray-400 rounded-full mr-2"></span>
            <span className="text-gray-600">Complexity: </span>
            <span className={`ml-1 px-2 py-1 rounded-full text-xs font-medium ${getComplexityColor(data.complexity)}`}>
              {data.complexity}
            </span>
          </div>
        )}
      </div>
      
      {data.description && (
        <div className="mt-3 p-2 bg-gray-50 rounded text-xs text-gray-700">
          {data.description}
        </div>
      )}
      
      {showConfig && (
        <div className="mt-3 p-3 bg-indigo-50 rounded-lg text-xs">
          {data.parameters && Object.keys(data.parameters).length > 0 && (
            <div className="mb-3">
              <strong className="text-indigo-800">Parameters:</strong>
              <div className="mt-1 space-y-1">
                {Object.entries(data.parameters).map(([key, value]) => (
                  <div key={key} className="flex justify-between items-center bg-white px-2 py-1 rounded">
                    <span className="text-gray-600">{key.replace(/_/g, ' ')}:</span>
                    <span className="text-indigo-700 font-medium">
                      {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {data.config && (
            <div>
              <strong className="text-indigo-800">Configuration:</strong>
              <pre className="mt-1 text-xs bg-white p-2 rounded border overflow-x-auto max-h-32">
                {JSON.stringify(data.config, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
      
      <Handle
        type="target"
        position={Position.Left}
        className="w-4 h-4 !bg-indigo-500"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-4 h-4 !bg-indigo-500"
      />
    </div>
  );
};

export default QuantumAlgorithmNode;

// Add quantum gradient CSS class
const style = document.createElement('style');
style.textContent = `
  .bg-quantum-gradient {
    background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  }
`;
document.head.appendChild(style);