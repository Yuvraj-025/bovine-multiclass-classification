import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

print("Backend path:", backend_path)
print("Path exists:", os.path.exists(backend_path))

# Test importing ModelManager
try:
    from model_loader.model_manager import ModelManager
    print("ModelManager imported successfully")
    
    # Check current working directory
    print("Current working directory:", os.getcwd())
    print("Script directory:", os.path.dirname(__file__))
    
    # Try different paths to find models
    project_root = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(project_root, "models")
    print("Trying models path:", models_path)
    print("Models path exists:", os.path.exists(models_path))
    
    if os.path.exists(models_path):
        import glob
        files = glob.glob(os.path.join(models_path, "*.pth"))
        print(f"Found {len(files)} .pth files in models directory")
        for f in files[:3]:  # Show first 3
            print(f"  - {os.path.basename(f)}")
    
    # Create model manager instance with absolute path
    mgr = ModelManager(models_path)
    models = mgr.list_models()
    print(f"Found {len(models)} models:")
    for model in models:
        print(f"  - {model}")
        
    print("Test completed successfully!")
    
except Exception as e:
    print("Error:", str(e))
    import traceback
    traceback.print_exc()