from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import os
from model_loader.model_manager import ModelManager
from services.prediction_service import PredictionService
from PIL import Image
import io

app = FastAPI(title="Cow Breed Classification API", version="1.0.0")

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model manager and prediction service
try:
    # Pass explicit path to ensure correct resolution
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    models_path = os.path.join(project_root, "models")
    print(f"Initializing model manager with path: {models_path}")
    
    model_manager = ModelManager(model_directory=models_path)
    prediction_service = PredictionService(model_manager)
    print("Backend initialized successfully")
    print(f"Available models: {model_manager.list_models()}")
except Exception as e:
    print(f"Error initializing backend: {str(e)}")
    import traceback
    traceback.print_exc()
    model_manager = None
    prediction_service = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Cow Breed Classification API"}

@app.get("/models")
async def get_models():
    """Get list of available models"""
    try:
        if model_manager is None:
            return {"models": [], "error": "Model manager not initialized"}
        models = model_manager.list_models()
        print(f"Returning {len(models)} models: {models}")
        return {"models": models}
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"models": [], "error": f"Error listing models: {str(e)}"}

@app.post("/predict")
async def predict(image: UploadFile = File(...), model_name: str = Form(...)):
    """Predict cow breed from uploaded image"""
    if model_manager is None or prediction_service is None:
        raise HTTPException(status_code=500, detail="Backend not properly initialized")
        
    try:
        # Validate image file
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
        
        # Read image
        image_bytes = await image.read()
        img = Image.open(io.BytesIO(image_bytes))
        
        # Make prediction
        result = prediction_service.predict(img, model_name)
        
        return {
            "model_used": model_name,
            "predicted_class": result["class"],
            "confidence": result["confidence"]
        }
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found")
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/reload-models")
async def reload_models():
    """Reload models from disk"""
    try:
        if model_manager is None:
            raise HTTPException(status_code=500, detail="Model manager not initialized")
        model_manager.reload_models()
        return {"message": "Models reloaded successfully", "models": model_manager.list_models()}
    except Exception as e:
        print(f"Error reloading models: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error reloading models: {str(e)}")