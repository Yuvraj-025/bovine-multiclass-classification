# Cow Identification Project (AI)

This project uses Convolutional Neural Networks (CNNs) to identify different breeds of cattle from images.

## Project Structure

- `data/`
  - `cattle/`: Dataset used for training and feeding the models.
  - `cattle_images_destructured/`: Renamed and flattened images from the original source.
- `models/`: Trained model files (`.pth`).
- `src/`: Core Python scripts for training and augmentation.
- `tests/`:
  - `images/`: Individual test images.
  - `scripts/`: Test scripts (to be restored/completed).
- `README.md`: Project documentation.
- `.gitignore`: Git exclusion rules.

## Getting Started

### Prerequisites
- Python 3.11+
- PyTorch
- torchvision
- matplotlib
- albumentations
- opencv-python

### Installation
```bash
pip install torch torchvision matplotlib albumentations opencv-python scikit-learn
```

### Running the Project
To train the model using ResNet50:
```bash
python src/train_resnet50.py
```

To run the augmentation model:
```bash
python src/augumentation_model.py
```

## Dataset
The dataset consists of various Indian cattle breeds such as Amritmahal, Gir, Sahiwal, etc.
The training scripts expect the dataset in `data/cattle/`.

## Note on Destructured Images
The folder `data/cattle_images_destructured/` contains images renamed in the format `[breedname]_img_[index].ext`. These were processed from the original `cattle_images` folder to provide a flat, searchable naming convention.
