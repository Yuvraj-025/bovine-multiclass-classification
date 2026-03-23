import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F
from model_loader.model_manager import ModelManager

class PredictionService:
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        # Define image transformations
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),  # Resize to match model input
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        # Define class labels (adjust based on your model)
        # TODO: Load these dynamically from your dataset classes
        self.class_labels = [
            "Amritmahal", "Bachaur", "Bangus", "Barrosa", "Bhadawari", "Cholistani", 
            "Dangi", "Deoni", "Gaolao", "Gir", "Goan", "Hariana", "Indo-Brazilian", 
            "Jersey", "Kangayam", "Karmanag", "Kasaragod", "Kenyah", "Kherigarh", 
            "Khillar", "Krishnagari", "Lohani", "Malvi", "Marathwada", "Mejankari", 
            "Nagori", "Nali", "Nelore", "Nilambur", "Ponwar", "Radha Valley", 
            "Sahiwal", "Salars", "Tadzhik", "Tamankaduwa"
        ]
    
    def predict(self, image: Image.Image, model_name: str) -> dict:
        """
        Predict cow breed from image using specified model
        
        Args:
            image: PIL Image object
            model_name: Name of the model to use
            
        Returns:
            Dictionary with predicted class and confidence
        """
        # Get the model
        model = self.model_manager.get_model(model_name)
        device = self.model_manager.device
        
        # Preprocess image
        input_tensor = self.transform(image)
        input_batch = input_tensor.unsqueeze(0).to(device)  # Add batch dimension and move to device
        
        # Perform inference
        with torch.no_grad():
            output = model(input_batch)
            
            # Apply softmax to get probabilities
            probabilities = F.softmax(output[0], dim=0)
            
            # Get the predicted class and confidence
            confidence, predicted_idx = torch.max(probabilities, 0)
            
            # Convert to Python types
            # Note: Ensure index is within bounds of class_labels
            if predicted_idx.item() < len(self.class_labels):
                predicted_class = self.class_labels[predicted_idx.item()]
            else:
                predicted_class = f"Unknown (ID: {predicted_idx.item()})"
                
            confidence_score = confidence.item()
            
        return {
            "class": predicted_class,
            "confidence": confidence_score
        }