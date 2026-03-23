import torch
import os
import glob
from typing import Dict, List
import torch.nn as nn

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
            
        self.models: Dict[str, str] = {}  # Store paths as strings, not model objects
        self.supported_formats = ["*.pth", "*.pt", "*.h5", "*.pkl"]
        self.load_models()
        print(f"Model Manager initialized. Found {len(self.models)} models")
    
    def load_models(self):
        """Load all models from the models directory"""
        self.models = {}
        
        print(f"Looking for models in: {self.model_directory}")
        
        if not os.path.exists(self.model_directory):
            print(f"Warning: Models directory '{self.model_directory}' does not exist")
            return
        
        # Find all supported model files
        model_files = []
        for pattern in self.supported_formats:
            pattern_files = glob.glob(os.path.join(self.model_directory, pattern))
            print(f"Pattern {pattern} matched {len(pattern_files)} files")
            model_files.extend(pattern_files)
        
        print(f"Found {len(model_files)} model files total")
        if model_files:
            print(f"First few files: {[os.path.basename(f) for f in model_files[:3]]}")
        
        for model_path in model_files:
            try:
                model_name = os.path.basename(model_path)
                # For now, just store the path instead of loading the actual model
                # Loading PyTorch models can fail with pickled models
                self.models[model_name] = model_path
                print(f"Registered model: {model_name}")
            except Exception as e:
                print(f"Warning: Could not register model {model_path}: {str(e)}")
    
    def list_models(self) -> List[str]:
        """Return list of available model names"""
        return list(self.models.keys())
    
    def get_model(self, model_name: str):
        """Get a specific model by name (returns path)"""
        if model_name not in self.models:
            raise FileNotFoundError(f"Model '{model_name}' not found")
        # Return the path for now, actual loading will happen in prediction service
        return self.models[model_name]
    
    def reload_models(self):
        """Reload all models from disk"""
        print("Reloading models...")
        self.load_models()