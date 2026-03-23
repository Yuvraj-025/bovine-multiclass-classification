import React from 'react';

const ModelSelector = ({ models, selectedModel, onSelect }) => {
  return (
    <div className="space-y-2">
      <label htmlFor="model-select" className="block text-sm font-medium text-gray-700">
        Select Model
      </label>
      <select
        id="model-select"
        value={selectedModel}
        onChange={(e) => onSelect(e.target.value)}
        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
      >
        {models.length > 0 ? (
          models.map((model) => (
            <option key={model} value={model}>
              {model}
            </option>
          ))
        ) : (
          <option disabled>No models available</option>
        )}
      </select>
      <p className="text-xs text-gray-500">
        {models.length > 0 
          ? `${models.length} model${models.length > 1 ? 's' : ''} loaded` 
          : 'Add models to the backend /models directory'}
      </p>
    </div>
  );
};

export default ModelSelector;