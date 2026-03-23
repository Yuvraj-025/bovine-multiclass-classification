#!/usr/bin/env python3
"""
Simple test script to verify model prediction functionality
"""

import sys
import os
import json
from model_predictor import predict_model

def main():
    # Test with a specific image and model
    image_path = "image.png"
    model_type = "lesslayers"
    
    if not os.path.exists(image_path):
        print(f"Test image not found: {image_path}")
        return
        
    try:
        print(f"Testing prediction with model '{model_type}' on image '{image_path}'")
        result = predict_model(model_type, image_path)
        print("Prediction result:")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error during prediction: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()