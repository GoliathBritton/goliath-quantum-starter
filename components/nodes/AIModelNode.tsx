import React from 'react';
import { Handle, Position } from 'reactflow';

interface AIModelNodeProps {
  data: {
    label: string;
    modelType?: string;
    config?: any;
  };
}

const AIModelNode: React.FC<AIModelNodeProps> = ({ data }) => {
  return (
    <div className="bg-purple-500 text-white p-4 rounded-lg shadow-lg min-w-[200px]">
      <div className="font-bold text-sm mb-2">🤖 AI Model</div>
      <div className="text-xs">{data.label}</div>
      {data.modelType && (
        <div className="text-xs opacity-75 mt-1">{data.modelType}</div>
      )}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-purple-300"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-purple-300"
      />
    </div>
  );
};

export default AIModelNode;