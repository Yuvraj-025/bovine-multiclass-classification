import os
import torch
from torchvision import transforms, datasets
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Configuration
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cattle")

# Define Augmentation Pipeline (similar to augumentation_model.py)
aug_transform = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.5, 1.0), p=1.0),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.Rotate(limit=30, p=0.5),
    A.HueSaturationValue(p=0.3),
    A.GaussNoise(p=0.3),
    A.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
    ToTensorV2()
])

def visualize_augmentation(image_path, num_samples=5):
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)
    
    plt.figure(figsize=(15, 5))
    plt.subplot(1, num_samples + 1, 1)
    plt.imshow(image)
    plt.title("Original")
    plt.axis("off")
    
    for i in range(num_samples):
        augmented = aug_transform(image=image_np)["image"]
        # Convert back to numpy for visualization
        aug_img = augmented.permute(1, 2, 0).cpu().numpy()
        aug_img = (aug_img * 0.5 + 0.5) # unnormalize
        aug_img = np.clip(aug_img, 0, 1)
        
        plt.subplot(1, num_samples + 1, i + 2)
        plt.imshow(aug_img)
        plt.title(f"Aug {i+1}")
        plt.axis("off")
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Get a random image from the dataset to demonstrate augmentation
    if os.path.exists(DATA_PATH):
        breeds = os.listdir(DATA_PATH)
        if breeds:
            first_breed = breeds[0]
            breed_path = os.path.join(DATA_PATH, first_breed)
            images = os.listdir(breed_path)
            if images:
                sample_img = os.path.join(breed_path, images[0])
                print(f"Visualizing augmentation for: {sample_img}")
                visualize_augmentation(sample_img)
            else:
                print("No images found in breed folder.")
        else:
            print("No breed folders found in data.")
    else:
        print(f"Data path {DATA_PATH} not found.")

