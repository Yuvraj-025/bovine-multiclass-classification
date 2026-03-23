import React from 'react';

const ConfidenceBar = ({ confidence }) => {
  // Convert confidence to percentage for display
  const percentage = Math.round(confidence * 100);
  
  // Determine color based on confidence level
  let barColor = 'bg-red-500';
  if (percentage >= 70) {
    barColor = 'bg-green-500';
  } else if (percentage >= 40) {
    barColor = 'bg-yellow-500';
  }

  return (
    <div className="mt-4">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">Confidence</span>
        <span className="text-sm font-medium text-gray-700">{percentage}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div 
          className={`${barColor} h-2.5 rounded-full`} 
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      <div className="flex justify-between mt-1">
        <span className="text-xs text-gray-500">Low</span>
        <span className="text-xs text-gray-500">High</span>
      </div>
    </div>
  );
};

export default ConfidenceBar;