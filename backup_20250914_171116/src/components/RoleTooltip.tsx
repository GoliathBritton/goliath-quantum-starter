// src/components/RoleTooltip.tsx
import { useState } from "react";

interface RoleTooltipProps {
  label: string;
  roleInsight: string;
}

export default function RoleTooltip({ label, roleInsight }: RoleTooltipProps) {
  const [isVisible, setIsVisible] = useState(false);

  return (
    <div className="relative inline-block">
      <button 
        className="px-4 py-2 bg-violet-700 text-white rounded-lg hover:bg-violet-800 transition-colors"
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
      >
        {label}
      </button>
      {isVisible && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 max-w-xs bg-gray-900 text-white shadow-lg p-3 rounded-lg border border-gray-700 z-10">
          <p className="text-sm">{roleInsight}</p>
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
        </div>
      )}
    </div>
  );
}