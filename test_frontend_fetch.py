import sys
import os

# Test fetching models
try:
    import requests
    response = requests.get("http://127.0.0.1:8000/models")
    print("Status Code:", response.status_code)
    print("Response:", response.json())
except Exception as e:
    print("Error connecting to backend:", str(e))
    print("This might be a network/firewall issue on Windows")
    
    # Fallback test - check if the backend logic works
    print("\n--- Testing backend logic directly ---")
    try:
        # Add backend to path and go up one level
        backend_path = os.path.join(os.path.dirname(__file__), 'backend')
        sys.path.insert(0, backend_path)
        
        # Import and test model manager
        from model_loader.model_manager import ModelManager
        mgr = ModelManager("../models")  # This should resolve to project_root/models
        models = mgr.list_models()
        print("Models from backend logic:", models)
        print("Expected frontend response:")
        print({"models": models})
        
        # Also test prediction service import
        try:
            from services.prediction_service import PredictionService
            print("Prediction service imported successfully")
        except Exception as e3:
            print("Prediction service import error:", str(e3))
    except Exception as e2:
        print("Error testing backend logic:", str(e2))
        import traceback
        traceback.print_exc()