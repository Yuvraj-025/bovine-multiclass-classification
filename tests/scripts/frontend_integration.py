#!/usr/bin/env python3
"""
Frontend Integration Script
This script serves as the entry point for your frontend to call the model predictions.
"""

import sys
import os
import json
from model_predictor import predict_model

def main():
    # Expecting exactly 2 arguments: model_type and image_path
    if len(sys.argv) != 3:
        print(json.dumps({
            "error": "Usage: python frontend_integration.py <model_type> <image_path>",
            "available_models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
        }))
        sys.exit(1)
    
    model_type = sys.argv[1]
    image_path = sys.argv[2]
    
    # Validate inputs
    if model_type not in ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]:
        print(json.dumps({
            "error": f"Invalid model type: {model_type}",
            "available_models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
        }))
        sys.exit(1)
    
    if not os.path.exists(image_path):
        print(json.dumps({
            "error": f"Image file not found: {image_path}"
        }))
        sys.exit(1)
    
    try:
        # Run prediction
        result = predict_model(model_type, image_path)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({
            "error": f"Prediction failed: {str(e)}"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()