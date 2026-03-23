# Cow Identification Project - Frontend Integration Guide

## Overview

This guide explains how to integrate the cow breed identification models with your frontend application. We've created several ways to interact with the models depending on your technical requirements.

## Available Models

1. **lesslayers** - A simpler CNN with fewer layers
2. **morelayers** - A more complex CNN with additional layers and batch normalization
3. **resnet50** - Transfer learning model based on ResNet50
4. **cattle_breed_classifier** - Another ResNet50-based classifier optimized for cattle breeds

## Method 1: Direct Script Execution (Simplest)

Call the frontend integration script directly from your backend:

```bash
python tests/scripts/frontend_integration.py <model_type> <image_path>
```

### Example Usage:

```bash
python tests/scripts/frontend_integration.py lesslayers /path/to/uploaded/image.jpg
```

This returns a JSON response:
```json
{
  "model": "lesslayers",
  "prediction": "Sahiwal",
  "confidence": 89.41,
  "all_probabilities": {
    "Amritmahal": 0.0,
    "Ayrshire": 0.0,
    // ... more breeds with probabilities
    "Sahiwal": 89.41,
    // ...
  }
}
```

## Method 2: Flask API Server (Recommended for Web Applications)

We also provide a RESTful API using Flask for easier integration with web applications.

### Starting the API Server:

```bash
python tests/scripts/flask_api.py
```

The server runs on `http://localhost:8000` by default.

### API Endpoints:

#### GET /
Returns API information

#### GET /models
Returns available models

#### POST /predict
Makes a prediction using the specified model

##### Request Body:
```json
{
  "model": "lesslayers",  // or "morelayers", "resnet50", "cattle_breed_classifier"
  "image_path": "/absolute/path/to/image.jpg"
}
```

##### Response:
```json
{
  "model": "lesslayers",
  "prediction": "Sahiwal",
  "confidence": 89.41,
  "all_probabilities": {
    // ... probabilities for all breeds
  }
}
```

### Example API Usage with curl:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"model":"resnet50","image_path":"/absolute/path/to/image.jpg"}'
```

## Method 3: Programmatic Integration

Import the predictor directly in your Python backend:

```python
from tests.scripts.model_predictor import predict_model

# Make prediction
result = predict_model("lesslayers", "/path/to/image.jpg")
print(result["prediction"])  # e.g., "Sahiwal"
print(result["confidence"])   # e.g., 89.41
```

## Implementation Recommendations

### For Web Applications:
1. Use the Flask API server method
2. Have your frontend upload images to your server
3. Save uploaded images to a temporary location
4. Call the API with the path to the saved image
5. Return the results to your frontend

### For Desktop Applications:
1. Use the direct script execution method
2. Execute the script as a subprocess
3. Parse the JSON output

## Error Handling

All methods return structured error messages:
- Missing parameters
- Invalid model types
- Image file not found
- Model loading errors

Always check for error responses in your integration code.

## File Locations

- Model files: `models/`
- Test images: `tests/images/`
- Scripts: `tests/scripts/`

## Requirements

Make sure to install required packages:
```bash
pip install torch torchvision pillow
```

For Flask API:
```bash
pip install flask
```

## Notes

1. All image paths must be absolute paths
2. Image files must be accessible from the server
3. Models must be trained and available in the `models/` directory
4. Supported image formats: JPG, PNG, and other formats supported by PIL

## Troubleshooting

If you encounter issues:
1. Check that model files exist in the `models/` directory
2. Verify that test images exist and are accessible
3. Confirm all required Python packages are installed
4. Ensure there's sufficient memory for model loading (especially ResNet50 models)