import torch
import os
import glob
from typing import Dict, List
import torch.nn as nn
from .models import VanillaCNNLessLayers, VanillaCNNMoreLayers, get_resnet50_model

class ModelManager:
    def __init__(self, model_directory: str = "../models"):
        """
        Initialize ModelManager with the specified model directory.
        
        Args:
            model_directory: Path to the models directory. If relative, will be resolved
                           from the backend directory to the project root.
        """
        # Determine the project root (parent of backend directory)
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(backend_dir)
        
        # Handle relative path from backend directory
        if model_directory.startswith("../"):
            # Go up one level from backend to project root, then to models
            self.model_directory = os.path.join(project_root, "models")
        elif not os.path.isabs(model_directory):
            # If it's a relative path that doesn't start with ../, resolve from project root
            self.model_directory = os.path.join(project_root, model_directory)
        else:
            # Absolute path
            self.model_directory = model_directory
            
        self.models: Dict[str, nn.Module] = {}  # Store loaded model objects
        self.model_paths: Dict[str, str] = {}   # Store paths for reference
        self.supported_formats = ["*.pth", "*.pt", "*.h5", "*.pkl"]
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Determine number of classes from data directory
        self.num_classes = self._get_num_classes()
        print(f"Detected {self.num_classes} classes for models")
        
        self.load_models()
        print(f"Model Manager initialized. Loaded {len(self.models)} models on {self.device}")

    def _get_num_classes(self) -> int:
        """Helper to determine number of classes from the dataset"""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        data_dir = os.path.join(project_root, "data", "cattle")
        if os.path.exists(data_dir):
            classes = [d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))]
            if classes:
                return len(classes)
        return 49  # Default fallback based on current dataset

    def load_models(self):
        """Load all models from the models directory"""
        self.models = {}
        self.model_paths = {}
        
        print(f"Looking for models in: {self.model_directory}")
        
        if not os.path.exists(self.model_directory):
            print(f"Warning: Models directory '{self.model_directory}' does not exist")
            return
        
        # Find all supported model files
        model_files = []
        for pattern in self.supported_formats:
            pattern_files = glob.glob(os.path.join(self.model_directory, pattern))
            model_files.extend(pattern_files)
        
        print(f"Found {len(model_files)} model files total")
        
        for model_path in model_files:
            try:
                model_name = os.path.basename(model_path)
                self.model_paths[model_name] = model_path
                
                # Load state dict first to detect number of classes
                state_dict = torch.load(model_path, map_location=self.device)
                
                # Detect number of classes from state_dict
                model_num_classes = self.num_classes
                # Check common final layer bias keys
                for key in ["fc.bias", "classifier.6.bias", "classifier.3.bias"]:
                    if key in state_dict:
                        model_num_classes = state_dict[key].shape[0]
                        break
                
                # Load the appropriate architecture
                model = None
                if "resnet50" in model_name.lower() or "cattle_breed_classifier" in model_name.lower():
                    model = get_resnet50_model(model_num_classes)
                elif "more" in model_name.lower() or "morelayers" in model_name.lower() or "cnn_model2" in model_name.lower():
                    model = VanillaCNNMoreLayers(model_num_classes)
                elif "lesslayers" in model_name.lower() or "cattle_cnn_model" in model_name.lower():
                    model = VanillaCNNLessLayers(model_num_classes)
                
                if model:
                    model.load_state_dict(state_dict)
                    model.to(self.device)
                    model.eval()
                    self.models[model_name] = model
                    if model_num_classes != self.num_classes:
                        print(f"Successfully loaded {model_name} ({model_num_classes} classes)")
                    else:
                        print(f"Successfully loaded and registered model: {model_name}")
                else:
                    print(f"Warning: Unknown model architecture for {model_name}. Skipping loading.")
                    
            except Exception as e:
                print(f"Warning: Could not load model {model_path}: {str(e)}")
    
    def list_models(self) -> List[str]:
        """Return list of available model names"""
        return list(self.models.keys())
    
    def get_model(self, model_name: str) -> nn.Module:
        """Get a specific loaded model by name"""
        if model_name not in self.models:
            raise FileNotFoundError(f"Model '{model_name}' not found or could not be loaded")
        return self.models[model_name]
    
    def reload_models(self):
        """Reload all models from disk"""
        print("Reloading models...")
        self.load_models()