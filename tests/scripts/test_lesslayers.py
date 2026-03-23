import os
import torch
import torch.nn as nn
from torchvision import transforms, datasets
from PIL import Image
import matplotlib.pyplot as plt

# Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "models", "cattle_cnn_model_lesslayers.pth")
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cattle")
TEST_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

class VanillaCNN(nn.Module):
    def __init__(self, num_classes):
        super(VanillaCNN, self).__init__()
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

def predict(image_path):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load classes from DATA_DIR
    dataset = datasets.ImageFolder(DATA_DIR)
    classes = dataset.classes
    num_classes = len(classes)

    # Load Model
    model = VanillaCNN(num_classes).to(device)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
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

    print(f"Predicted: {predicted_class} ({confidence:.2f}%)")
    
    # Optional: Display result
    # plt.imshow(image)
    # plt.title(f"Predicted: {predicted_class} ({confidence:.2f}%)")
    # plt.axis("off")
    # plt.show()

if __name__ == "__main__":
    # Test with one of the images in tests/images
    test_img = os.path.join(TEST_IMAGE_DIR, "image.png")
    if os.path.exists(test_img):
        predict(test_img)
    else:
        print(f"Test image {test_img} not found. Please provide a valid path.")
