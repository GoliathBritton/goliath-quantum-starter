import React from 'react';
import { Handle, Position } from 'reactflow';

interface ConditionalNodeProps {
  data: {
    label: string;
    condition?: string;
    config?: any;
  };
}

const ConditionalNode: React.FC<ConditionalNodeProps> = ({ data }) => {
  return (
    <div className="bg-yellow-500 text-white p-4 rounded-lg shadow-lg min-w-[200px]">
      <div className="font-bold text-sm mb-2">🔀 Conditional</div>
      <div className="text-xs">{data.label}</div>
      {data.condition && (
        <div className="text-xs opacity-75 mt-1">{data.condition}</div>
      )}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-yellow-300"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="true"
        style={{ top: '30%' }}
        className="w-3 h-3 bg-green-400"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="false"
        style={{ top: '70%' }}
        className="w-3 h-3 bg-red-400"
      />
    </div>
  );
};

export default ConditionalNode;