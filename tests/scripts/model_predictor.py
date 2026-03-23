import os
import torch
import torch.nn as nn
from torchvision import transforms, datasets, models
from PIL import Image
import json

# Configuration
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cattle")
TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

class VanillaCNNLessLayers(nn.Module):
    def __init__(self, num_classes):
        super(VanillaCNNLessLayers, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)
        )
        self.classifier = nn.Sequential(
            nn.Linear(128 * 28 * 28, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

class VanillaCNNMoreLayers(nn.Module):
    def __init__(self, num_classes):
        super(VanillaCNNMoreLayers, self).__init__()
        self.features = nn.Sequential(
            # Block 1
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            # Block 2
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            # Block 3
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            # Block 4
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)
        )
        # 224 / 2^4 = 14
        self.classifier = nn.Sequential(
            nn.Linear(512 * 14 * 14, 1024),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(1024, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

def load_classes():
    """Load class names from the dataset"""
    dataset = datasets.ImageFolder(DATA_DIR)
    return dataset.classes

def predict_lesslayers(image_path):
    """Predict using the less layers CNN model"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load classes
    classes = load_classes()
    num_classes = len(classes)

    # Load Model
    model_path = os.path.join(MODELS_DIR, "cattle_cnn_model_lesslayers.pth")
    model = VanillaCNNLessLayers(num_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    # Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    # Load Image
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
        prob = torch.nn.functional.softmax(output, dim=1)[0]
    
    predicted_class = classes[predicted.item()]
    confidence = prob[predicted.item()].item() * 100

    return {
        "model": "lesslayers",
        "prediction": predicted_class,
        "confidence": round(confidence, 2),
        "all_probabilities": {classes[i]: round(prob[i].item() * 100, 2) for i in range(len(classes))}
    }

def predict_morelayers(image_path):
    """Predict using the more layers CNN model"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load classes
    classes = load_classes()
    num_classes = len(classes)

    # Load Model
    model_path = os.path.join(MODELS_DIR, "cattle_cnn_model_more.pth")
    model = VanillaCNNMoreLayers(num_classes).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()

    # Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    # Load Image
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
        prob = torch.nn.functional.softmax(output, dim=1)[0]
    
    predicted_class = classes[predicted.item()]
    confidence = prob[predicted.item()].item() * 100

    return {
        "model": "morelayers",
        "prediction": predicted_class,
        "confidence": round(confidence, 2),
        "all_probabilities": {classes[i]: round(prob[i].item() * 100, 2) for i in range(len(classes))}
    }

def predict_resnet(image_path):
    """Predict using the ResNet50 model"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load classes
    classes = load_classes()
    num_classes = len(classes)

    # Load ResNet50 Architecture
    model = models.resnet50()
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    
    # Load Weights
    model_path = os.path.join(MODELS_DIR, "resnet50_cattle_classifier.pth")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    # Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load Image
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
        prob = torch.nn.functional.softmax(output, dim=1)[0]
    
    predicted_class = classes[predicted.item()]
    confidence = prob[predicted.item()].item() * 100

    return {
        "model": "resnet50",
        "prediction": predicted_class,
        "confidence": round(confidence, 2),
        "all_probabilities": {classes[i]: round(prob[i].item() * 100, 2) for i in range(len(classes))}
    }

def predict_cattle_breed_classifier(image_path):
    """Predict using the cattle breed classifier model"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load classes
    classes = load_classes()
    num_classes = len(classes)

    # Load ResNet50 Architecture
    model = models.resnet50()
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    
    # Load Weights
    model_path = os.path.join(MODELS_DIR, "cattle_breed_classifier.pth")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    # Transform
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load Image
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0).to(device)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        _, predicted = torch.max(output, 1)
        prob = torch.nn.functional.softmax(output, dim=1)[0]
    
    predicted_class = classes[predicted.item()]
    confidence = prob[predicted.item()].item() * 100

    return {
        "model": "cattle_breed_classifier",
        "prediction": predicted_class,
        "confidence": round(confidence, 2),
        "all_probabilities": {classes[i]: round(prob[i].item() * 100, 2) for i in range(len(classes))}
    }

def predict_model(model_type, image_path):
    """Main prediction function that routes to the appropriate model"""
    if model_type == "lesslayers":
        return predict_lesslayers(image_path)
    elif model_type == "morelayers":
        return predict_morelayers(image_path)
    elif model_type == "resnet50":
        return predict_resnet(image_path)
    elif model_type == "cattle_breed_classifier":
        return predict_cattle_breed_classifier(image_path)
    else:
        raise ValueError(f"Unknown model type: {model_type}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python model_predictor.py <model_type> <image_path>")
        print("Available models: lesslayers, morelayers, resnet50, cattle_breed_classifier")
        sys.exit(1)
    
    model_type = sys.argv[1]
    image_path = sys.argv[2]
    
    if not os.path.exists(image_path):
        print(f"Image file {image_path} not found")
        sys.exit(1)
        
    try:
        result = predict_model(model_type, image_path)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)