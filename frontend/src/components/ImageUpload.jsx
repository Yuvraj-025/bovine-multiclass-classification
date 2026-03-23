import React, { useRef } from 'react';

const ImageUpload = ({ onImageUpload, isLoading }) => {
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file) {
      processFile(file);
    }
  };

  const processFile = (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file');
      return;
    }
    
    onImageUpload(file);
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="space-y-4">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          isLoading 
            ? 'border-gray-300 bg-gray-100' 
            : 'border-indigo-300 hover:border-indigo-400 bg-indigo-50 hover:bg-indigo-100'
        }`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={!isLoading ? handleClick : undefined}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInput}
          accept="image/*"
          className="hidden"
          disabled={isLoading}
        />
        
        {isLoading ? (
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mb-2"></div>
            <p className="text-gray-600">Analyzing image...</p>
          </div>
        ) : (
          <>
            <div className="mx-auto mb-3">
              <svg className="w-12 h-12 mx-auto text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
            </div>
            <p className="text-lg font-medium text-gray-700 mb-1">Drag & drop an image</p>
            <p className="text-gray-500 mb-2">or</p>
            <button 
              type="button" 
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Browse Files
            </button>
            <p className="text-xs text-gray-500 mt-2">Supports JPG, PNG, GIF</p>
          </>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;