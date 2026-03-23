import os
import torch
import torch.nn as nn
from torchvision import transforms, datasets, models
from PIL import Image

# Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "resnet50_cattle_classifier.pth")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cattle")
TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

def predict(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load classes
    dataset = datasets.ImageFolder(DATA_DIR)
    classes = dataset.classes
    num_classes = len(classes)

    # Load ResNet50 Architecture
    model = models.resnet50()
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    
    # Load Weights
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.to(device)
        model.eval()
    else:
        print(f"Warning: Model file {MODEL_PATH} not found.")
        return

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

    print(f"Predicted (ResNet50): {predicted_class} ({confidence:.2f}%)")

if __name__ == "__main__":
    test_img = os.path.join(TEST_IMAGE_DIR, "image.png")
    if os.path.exists(test_img):
        predict(test_img)
    else:
        print(f"Test image {test_img} not found.")
