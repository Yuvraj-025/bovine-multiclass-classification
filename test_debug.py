import os
import sys
import torch

# Add backend to path
backend_path = r"y:\Projects\cow_identification_project_AI\backend"
if backend_path not in sys.path:
    sys.path.append(backend_path)

from model_loader.models import VanillaCNNLessLayers, VanillaCNNMoreLayers, get_resnet50_model

def get_num_classes():
    return 49

def test_loading():
    models_dir = os.path.join(backend_path, "models")
    num_classes = get_num_classes()
    device = torch.device("cpu")
    
    if not os.path.exists(models_dir):
        print(f"Error: {models_dir} does not exist")
        return

    model_files = [f for f in os.listdir(models_dir) if f.endswith(".pth")]
    print(f"Found {len(model_files)} models: {model_files}")
    
    for model_name in model_files:
        model_path = os.path.join(models_dir, model_name)
        print(f"\nProcessing: {model_name}")
        
        # Mimic logic in model_manager.py
        arch = "None"
        model = None
        if "resnet50" in model_name.lower() or "cattle_breed_classifier" in model_name.lower():
            arch = "get_resnet50_model"
            model = get_resnet50_model(num_classes)
        elif "more" in model_name.lower() or "morelayers" in model_name.lower() or "cnn_model2" in model_name.lower():
            arch = "VanillaCNNMoreLayers"
            model = VanillaCNNMoreLayers(num_classes)
        elif "lesslayers" in model_name.lower() or "cattle_cnn_model" in model_name.lower():
            arch = "VanillaCNNLessLayers"
            model = VanillaCNNLessLayers(num_classes)
            
        print(f"Selected Architecture: {arch}")
        
        if model:
            try:
                state_dict = torch.load(model_path, map_location=device)
                model.load_state_dict(state_dict)
                print(f"SUCCESS: Loaded {model_name} with {arch}")
            except Exception as e:
                print(f"FAILURE: Could not load {model_name} with {arch}. Error: {str(e)}")
        else:
            print(f"SKIP: No architecture found for {model_name}")

if __name__ == "__main__":
    test_loading()
