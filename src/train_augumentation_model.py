#pip install albumentations opencv-python

import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, random_split, Subset
from torchvision import datasets
import matplotlib.pyplot as plt
import albumentations as A
from albumentations.pytorch import ToTensorV2


DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cattle")
BATCH_SIZE = 32
LEARNING_RATE = 0.001
NUM_EPOCHS = 150
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "cattle_cnn_model_morelayers_albumentations.pth")
NUM_WORKERS = 4
PIN_MEMORY = True


alb_train_transform = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.6, 1.0), ratio=(0.75, 1.33), p=1.0),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.05),
    A.ShiftScaleRotate(shift_limit=0.06, scale_limit=0.2, rotate_limit=25, p=0.6),
    A.OneOf([
        A.IAAAdditiveGaussianNoise(),
        A.GaussNoise(var_limit=(10.0, 50.0))
    ], p=0.2),
    A.OneOf([
        A.MotionBlur(blur_limit=7),
        A.MedianBlur(blur_limit=5),
        A.Blur(blur_limit=5)
    ], p=0.2),
    A.CLAHE(p=0.2),
    A.OneOf([
        A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3),
        A.HueSaturationValue(hue_shift_limit=15, sat_shift_limit=25, val_shift_limit=15),
        A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15)
    ], p=0.7),
    A.OneOf([
        A.GridDistortion(num_steps=5, distort_limit=0.3),
        A.OpticalDistortion(distort_limit=0.15),
        A.ElasticTransform(alpha=1, sigma=50, alpha_affine=50)
    ], p=0.2),
    A.Sharpen(p=0.2),
    A.IAAPerspective(p=0.15),
    # simulating occlusion
    A.CoarseDropout(max_holes=4, max_height=40, max_width=40, min_holes=1, min_height=10, min_width=10, fill_value=0, p=0.4),
    # Cutout-like
    A.Cutout(num_holes=8, max_h_size=40, max_w_size=40, fill_value=0, p=0.25),
    # final normalization and to tensor
    A.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)),
    ToTensorV2()
])

alb_test_transform = A.Compose([
    A.Resize(224, 224),
    A.Normalize(mean=(0.5,0.5,0.5), std=(0.5,0.5,0.5)),
    ToTensorV2()
])


class AlbumentationsWrapper(torch.utils.data.Dataset):
    def __init__(self, base_dataset, transform=None):
        """
        base_dataset: torchvision.datasets.ImageFolder OR torch.utils.data.Subset(ImageFolder)
        transform: albumentations transform (expects numpy images HWC)
        """
        self.transform = transform

        # If it's a Subset, extract underlying dataset and index mapping
        if isinstance(base_dataset, Subset):
            self.base_is_subset = True
            self.dataset = base_dataset.dataset  # underlying ImageFolder
            # historic compatibility: Subset stores indices in .indices
            self.indices = getattr(base_dataset, "indices", None)
            if self.indices is None:
                # new PyTorch versions may store .indices as list-like; fallback to attribute name _indices
                self.indices = getattr(base_dataset, "_indices", None)
            if self.indices is None:
                raise RuntimeError("Couldn't find indices in Subset. Unsupported Subset structure.")
        else:
            self.base_is_subset = False
            self.dataset = base_dataset
            # present dataset.samples or imgs
        # prefer .samples (ImageFolder sets .samples = list of (path, class_idx))
        self.samples = getattr(self.dataset, "samples", None) or getattr(self.dataset, "imgs", None)
        if self.samples is None:
            raise RuntimeError("Provided dataset must be torchvision.datasets.ImageFolder or Subset(ImageFolder).")

    def __len__(self):
        if self.base_is_subset:
            return len(self.indices)
        return len(self.samples)

    def __getitem__(self, idx):
        if self.base_is_subset:
            actual_idx = self.indices[idx]
        else:
            actual_idx = idx
        path, label = self.samples[actual_idx]
        image = Image.open(path).convert("RGB")
        image = np.array(image)
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented["image"]  # this is a torch.Tensor from ToTensorV2
        else:
            # fallback: simple conversion + normalization if no transform
            image = ToTensorV2()(image=image)["image"]
        return image, label


full_dataset = datasets.ImageFolder(root=DATA_PATH)
num_classes = len(full_dataset.classes)
total_images = len(full_dataset)
print(f"Found {total_images} images across {num_classes} classes: {full_dataset.classes}")

train_size = int(0.8 * total_images)
val_size = int(0.1 * total_images)
test_size = total_images - train_size - val_size
train_subset, val_subset, test_subset = random_split(full_dataset, [train_size, val_size, test_size])

train_dataset = AlbumentationsWrapper(train_subset, transform=alb_train_transform)
val_dataset = AlbumentationsWrapper(val_subset, transform=alb_test_transform)
test_dataset = AlbumentationsWrapper(test_subset, transform=alb_test_transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS, pin_memory=PIN_MEMORY)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=PIN_MEMORY)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS, pin_memory=PIN_MEMORY)


class VanillaCNN(nn.Module):
    def __init__(self, num_classes):
        super(VanillaCNN, self).__init__()

        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2)
        )

        # for input 224x224 after 4 maxpools -> spatial 14x14
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

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training on: {device}")

model = VanillaCNN(num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

train_losses, val_losses = [], []


for epoch in range(NUM_EPOCHS):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * images.size(0)
    avg_train_loss = running_loss / len(train_loader.dataset)

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item() * images.size(0)
    avg_val_loss = val_loss / len(val_loader.dataset)

    train_losses.append(avg_train_loss)
    val_losses.append(avg_val_loss)

    print(f"Epoch [{epoch+1}/{NUM_EPOCHS}] - Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}")


torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'num_classes': num_classes
}, MODEL_SAVE_PATH)
print(f"Model saved at: {MODEL_SAVE_PATH}")


model.eval()
correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = 100 * correct / total if total > 0 else 0.0
print(f"\nTest Accuracy: {accuracy:.2f}%")


plt.figure(figsize=(8,5))
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Validation Loss')
plt.title("Training and Validation Loss over Epochs")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()
