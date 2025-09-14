import React from 'react';
import { Handle, Position } from 'reactflow';

interface DataSourceNodeProps {
  data: {
    label: string;
    sourceType?: string;
    config?: any;
  };
}

const DataSourceNode: React.FC<DataSourceNodeProps> = ({ data }) => {
  return (
    <div className="bg-blue-500 text-white p-4 rounded-lg shadow-lg min-w-[200px]">
      <div className="font-bold text-sm mb-2">📊 Data Source</div>
      <div className="text-xs">{data.label}</div>
      {data.sourceType && (
        <div className="text-xs opacity-75 mt-1">{data.sourceType}</div>
      )}
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-blue-300"
      />
    </div>
  );
};

export default DataSourceNode;