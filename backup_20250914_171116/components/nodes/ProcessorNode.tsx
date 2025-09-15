import React from 'react';
import { Handle, Position } from 'reactflow';

interface ProcessorNodeProps {
  data: {
    label: string;
    processorType?: string;
    config?: any;
  };
}

const ProcessorNode: React.FC<ProcessorNodeProps> = ({ data }) => {
  return (
    <div className="bg-green-500 text-white p-4 rounded-lg shadow-lg min-w-[200px]">
      <div className="font-bold text-sm mb-2">⚙️ Processor</div>
      <div className="text-xs">{data.label}</div>
      {data.processorType && (
        <div className="text-xs opacity-75 mt-1">{data.processorType}</div>
      )}
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-green-300"
      />
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-green-300"
      />
    </div>
  );
};

export default ProcessorNode;