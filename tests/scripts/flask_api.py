from flask import Flask, request, jsonify
import os
from model_predictor import predict_model

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Cattle Breed Classification API",
        "endpoints": {
            "/predict": "POST endpoint for predictions"
        },
        "models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
    })

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify({
        "models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Extract parameters
        model_type = data.get('model')
        image_path = data.get('image_path')
        
        # Validate inputs
        if not model_type:
            return jsonify({"error": "Missing 'model' parameter"}), 400
            
        if not image_path:
            return jsonify({"error": "Missing 'image_path' parameter"}), 400
        
        if model_type not in ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]:
            return jsonify({
                "error": f"Invalid model type: {model_type}",
                "available_models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
            }), 400
        
        if not os.path.exists(image_path):
            return jsonify({"error": f"Image file not found: {image_path}"}), 400
        
        # Run prediction
        result = predict_model(model_type, image_path)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)