import React from 'react';
import { Handle, Position, NodeProps } from 'reactflow';

interface OutputNodeData {
  label: string;
  icon?: string;
  description?: string;
  config?: any;
}

const OutputNode: React.FC<NodeProps<OutputNodeData>> = ({ data, selected }) => {
  return (
    <div className={`px-4 py-2 shadow-md rounded-md bg-white border-2 ${
      selected ? 'border-purple-500' : 'border-gray-200'
    }`}>
      <div className="flex items-center">
        <div className="rounded-full w-12 h-12 flex justify-center items-center bg-purple-100">
          <span className="text-lg">{data.icon || '📤'}</span>
        </div>
        <div className="ml-2">
          <div className="text-lg font-bold">{data.label}</div>
          <div className="text-gray-500 text-sm">{data.description}</div>
        </div>
      </div>
      
      <Handle
        type="target"
        position={Position.Left}
        className="w-16 !bg-purple-500"
      />
    </div>
  );
};

export default OutputNode;