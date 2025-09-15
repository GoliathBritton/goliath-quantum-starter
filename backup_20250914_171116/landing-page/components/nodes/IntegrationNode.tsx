import React, { useState } from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

// Type assertion for component
const HandleComponent = Handle as any;

interface IntegrationNodeData {
  label: string;
  icon?: string;
  description?: string;
  integrationType?: string;
  endpoint?: string;
  config?: any;
  credentials?: any;
}

const IntegrationNode: React.FC<NodeProps<IntegrationNodeData>> = ({ data, selected }) => {
  const [showConfig, setShowConfig] = useState(false);

  const getIntegrationIcon = (integrationType?: string) => {
    const icons: { [key: string]: string } = {
      'api': '🔗',
      'database': '🗄️',
      'webhook': '📡',
      'file_system': '📁',
      'cloud_storage': '☁️',
      'message_queue': '📬',
      'email': '📧',
      'slack': '💬',
      'github': '🐙',
      'aws': '🟠',
      'azure': '🔵',
      'gcp': '🟡',
      'docker': '🐳',
      'kubernetes': '⚙️'
    };
    return icons[integrationType || ''] || '🔗';
  };

  return (
    <div className={`px-4 py-2 shadow-md rounded-md bg-white border-2 ${
      selected ? 'border-teal-500' : 'border-gray-200'
    }`}>
      <div className="flex items-center">
        <div className="rounded-full w-12 h-12 flex justify-center items-center bg-teal-100">
          <span className="text-lg">{data.icon || getIntegrationIcon(data.integrationType)}</span>
        </div>
        <div className="ml-2">
          <div className="text-lg font-bold">{data.label}</div>
          <div className="text-gray-500 text-sm">{data.description}</div>
          {data.integrationType && (
            <div className="text-xs text-teal-600">Type: {data.integrationType}</div>
          )}
          {data.endpoint && (
            <div className="text-xs text-gray-600">Endpoint: {data.endpoint}</div>
          )}
        </div>
      </div>
      
      {data.config && Object.keys(data.config).length > 0 && (
        <button
          onClick={() => setShowConfig(!showConfig)}
          className="mt-2 text-xs text-teal-600 hover:text-teal-800"
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
        className="w-3 h-3 !bg-teal-500"
      />
      <HandleComponent
        type="source"
        position={Position.Right}
        className="w-3 h-3 !bg-teal-500"
      />
    </div>
  );
};

export default IntegrationNode;