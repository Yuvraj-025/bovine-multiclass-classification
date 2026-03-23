import os
import sys

# Add backend to path
backend_path = r"y:\Projects\cow_identification_project_AI\backend"
if backend_path not in sys.path:
    sys.path.append(backend_path)

from model_loader.model_manager import ModelManager

def main():
    try:
        # Initialize ModelManager with the backend/models directory
        # Based on the code, it resolves relative to project root.
        # Let's just pass the absolute path to be sure.
        models_dir = os.path.join(backend_path, "models")
        print(f"Testing ModelManager with directory: {models_dir}")
        manager = ModelManager(model_directory=models_dir)
        
        print("\nLoaded models:")
        for name in manager.list_models():
            print(f" - {name}")
            
        print(f"\nTotal loaded: {len(manager.models)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
