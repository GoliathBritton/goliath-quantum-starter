import React, { useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

// Type assertion for component
const HandleComponent = Handle as any;

interface ConditionalNodeData {
  label: string;
  icon?: string;
  description?: string;
  condition?: string;
  conditionType?: string;
  config?: any;
}

const ConditionalNode: React.FC<NodeProps<ConditionalNodeData>> = ({ data, selected }) => {
  const [showConfig, setShowConfig] = useState(false);

  const getConditionIcon = (conditionType?: string) => {
    const icons: { [key: string]: string } = {
      'if_else': '🔀',
      'switch': '🎛️',
      'loop': '🔄',
      'while': '⏳',
      'for': '🔢',
      'filter': '🔍',
      'threshold': '📏',
      'comparison': '⚖️',
      'logical': '🧮'
    };
    return icons[conditionType || ''] || '🔀';
  };

  return (
    <div className={`px-4 py-2 shadow-md rounded-md bg-white border-2 ${
      selected ? 'border-orange-500' : 'border-gray-200'
    }`}>
      <div className="flex items-center">
        <div className="rounded-full w-12 h-12 flex justify-center items-center bg-orange-100">
          <span className="text-lg">{data.icon || getConditionIcon(data.conditionType)}</span>
        </div>
        <div className="ml-2">
          <div className="text-lg font-bold">{data.label}</div>
          <div className="text-gray-500 text-sm">{data.description}</div>
          {data.conditionType && (
            <div className="text-xs text-orange-600">Type: {data.conditionType}</div>
          )}
          {data.condition && (
            <div className="text-xs text-gray-600">Condition: {data.condition}</div>
          )}
        </div>
      </div>
      
      {data.config && Object.keys(data.config).length > 0 && (
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="mt-2 text-xs text-orange-600 hover:text-orange-800"
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
        className="w-3 h-3 !bg-orange-500"
      />
      <HandleComponent
        type="source"
        position={Position.Right}
        className="w-3 h-3 !bg-orange-500"
      />
      <HandleComponent
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 !bg-orange-500"
        id="false"
      />
    </div>
  );
};

export default ConditionalNode;