import React from 'react';

const ResultDisplay = ({ result }) => {
  if (!result) return null;

  return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-4">
      <h3 className="text-lg font-medium text-green-800 mb-2">Prediction Result</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <p className="text-sm text-gray-600">Model Used</p>
          <p className="font-medium">{result.model_used}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Predicted Breed</p>
          <p className="font-medium text-lg text-green-700">{result.predicted_class}</p>
        </div>
        <div>
          <p className="text-sm text-gray-600">Confidence Score</p>
          <p className="font-medium">
            {(result.confidence * 100).toFixed(2)}%
          </p>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;