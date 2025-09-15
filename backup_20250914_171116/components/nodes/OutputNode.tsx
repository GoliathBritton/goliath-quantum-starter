import React from 'react';
import { Handle, Position } from 'reactflow';

interface OutputNodeProps {
  data: {
    label: string;
    outputType?: string;
    config?: any;
  };
}

const OutputNode: React.FC<OutputNodeProps> = ({ data }) => {
  return (
    <div className="bg-orange-500 text-white p-4 rounded-lg shadow-lg min-w-[200px]">
      <div className="font-bold text-sm mb-2">📤 Output</div>
      <div className="text-xs">{data.label}</div>
      {data.outputType && (
        <div className="text-xs opacity-75 mt-1">{data.outputType}</div>
      )}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-orange-300"
      />
    </div>
  );
};

export default OutputNode;