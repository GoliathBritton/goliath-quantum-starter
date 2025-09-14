import React, { useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

// Type assertion for component
const HandleComponent = Handle as any;

interface AIModelNodeData {
  label: string;
  icon?: string;
  description?: string;
  modelType?: string;
  config?: any;
  parameters?: { [key: string]: any };
}

const AIModelNode: React.FC<NodeProps<AIModelNodeData>> = ({ data, selected }) => {
  const [showConfig, setShowConfig] = useState(false);

  const getModelIcon = (modelType?: string) => {
    const icons: { [key: string]: string } = {
      'neural_network': '🧠',
      'decision_tree': '🌳',
      'random_forest': '🌲',
      'svm': '📊',
      'linear_regression': '📈',
      'logistic_regression': '📉',
      'clustering': '🎯',
      'deep_learning': '🤖',
      'transformer': '🔄',
      'cnn': '👁️',
      'rnn': '🔁',
      'lstm': '📝'
    };
    return icons[modelType || ''] || '🤖';
  };

  return (
    <div className={`px-4 py-2 shadow-md rounded-md bg-white border-2 ${
      selected ? 'border-purple-500' : 'border-gray-200'
    }`}>
      <div className="flex items-center">
        <div className="rounded-full w-12 h-12 flex justify-center items-center bg-purple-100">
          <span className="text-lg">{data.icon || getModelIcon(data.modelType)}</span>
        </div>
        <div className="ml-2">
          <div className="text-lg font-bold">{data.label}</div>
          <div className="text-gray-500 text-sm">{data.description}</div>
          {data.modelType && (
            <div className="text-xs text-purple-600">Model: {data.modelType}</div>
          )}
        </div>
      </div>
      
      {data.config && Object.keys(data.config).length > 0 && (
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="mt-2 text-xs text-purple-600 hover:text-purple-800"
        >
          {showConfig ? 'Hide Config' : 'Show Config'}
        </button>
      )}
      
      {showConfig && data.config && (
        <div className="mt-2 p-2 bg-gray-50 rounded text-xs">
          {Object.entries(data.config).map(([key, value]) => (
            <div key={key} className="flex justify-between">
              <span>{key}:</span>
              <span>{String(value)}</span>
            </div>
          ))}
        </div>
      )}
      
      <HandleComponent
        type="target"
        position={Position.Left}
        className="w-3 h-3 !bg-purple-500"
      />
      <HandleComponent
        type="source"
        position={Position.Right}
        className="w-3 h-3 !bg-purple-500"
      />
    </div>
  );
};

export default AIModelNode;