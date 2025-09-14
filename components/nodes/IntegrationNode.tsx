import React from 'react';
import { Handle, Position } from 'reactflow';

interface IntegrationNodeProps {
  data: {
    label: string;
    integrationType?: string;
    config?: any;
  };
}

const IntegrationNode: React.FC<IntegrationNodeProps> = ({ data }) => {
  return (
    <div className="bg-indigo-500 text-white p-4 rounded-lg shadow-lg min-w-[200px]">
      <div className="font-bold text-sm mb-2">🔗 Integration</div>
      <div className="text-xs">{data.label}</div>
      {data.integrationType && (
        <div className="text-xs opacity-75 mt-1">{data.integrationType}</div>
      )}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-indigo-300"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-indigo-300"
      />
    </div>
  );
};

export default IntegrationNode;