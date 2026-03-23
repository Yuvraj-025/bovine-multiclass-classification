import React, { useState, useEffect } from 'react';
import ImageUpload from './components/ImageUpload';
import ModelSelector from './components/ModelSelector';
import ResultDisplay from './components/ResultDisplay';
import ConfidenceBar from './components/ConfidenceBar';

const API_BASE_URL = 'http://127.0.0.1:8000';

function App() {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [predictionResult, setPredictionResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch available models on component mount
  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/models`);
      const data = await response.json();
      setModels(data.models);
      
      // Select first model by default if available
      if (data.models.length > 0) {
        setSelectedModel(data.models[0]);
      }
    } catch (err) {
      setError('Failed to fetch models');
      console.error('Error fetching models:', err);
    }
  };

  const handleImageUpload = async (file) => {
    if (!selectedModel) {
      setError('Please select a model first');
      return;
    }

    setIsLoading(true);
    setError('');
    setPredictionResult(null);

    try {
      const formData = new FormData();
      formData.append('image', file);
      formData.append('model_name', selectedModel);

      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      setPredictionResult(result);
    } catch (err) {
      setError(`Prediction failed: ${err.message}`);
      console.error('Prediction error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReloadModels = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/reload-models`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setModels(data.models);
      setError('');
    } catch (err) {
      setError(`Failed to reload models: ${err.message}`);
      console.error('Error reloading models:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">🐄 Cow Breed Classifier</h1>
          <p className="text-gray-600">Upload an image to identify cow breeds using AI</p>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <ModelSelector 
                models={models} 
                selectedModel={selectedModel} 
                onSelect={setSelectedModel}
              />
              
              <button
                onClick={handleReloadModels}
                className="mt-3 w-full py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Reload Models
              </button>
            </div>
            
            <div>
              <ImageUpload onImageUpload={handleImageUpload} isLoading={isLoading} />
            </div>
          </div>

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {predictionResult && (
            <div className="mt-6">
              <ResultDisplay result={predictionResult} />
              <ConfidenceBar confidence={predictionResult.confidence} />
            </div>
          )}
        </div>

        <div className="text-center text-sm text-gray-500">
          <p>Upload an image of a cow to classify its breed using machine learning</p>
        </div>
      </div>
    </div>
  );
}

export default App;