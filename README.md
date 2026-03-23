# Cow Identification Project (AI)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

This project uses Convolutional Neural Networks (CNNs) to identify different breeds of cattle from images.

## 🌐 Web Application

We've built a complete web application with React frontend and FastAPI backend that allows you to:
- Upload images of cows
- Select from multiple trained models
- Get instant breed predictions with confidence scores

See [SETUP.md](SETUP.md) for detailed installation instructions.

## Project Structure

- `data/`
  - `cattle/`: Dataset used for training and feeding the models.
  - `cattle_images_destructured/`: Renamed and flattened images from the original source.
- `models/`: Trained model files (`.pth`).
- `src/`: Core Python scripts for training and augmentation.
- `backend/`: FastAPI backend for the web application
- `frontend/`: React frontend for the web application
- `tests/`:
  - `images/`: Individual test images.
  - `scripts/`: Test scripts (to be restored/completed).
- `README.md`: Project documentation.
- `SETUP.md`: Detailed setup instructions for the web application.
- `.gitignore`: Git exclusion rules.

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 14+
- PyTorch
- torchvision
- matplotlib
- albumentations
- opencv-python

### Installation
```bash
# Install backend dependencies
pip install torch torchvision matplotlib albumentations opencv-python scikit-learn

# Install frontend dependencies
cd frontend && npm install
```

#### Running the Web Application

#### Option 1: Unified Startup (Recommended)
The easiest way to start both the frontend and backend is using the `start-system.py` script:
```bash
python start-system.py
```

#### Option 2: Manual Start (Advanced)
If you need to start individual components:

**Backend:**
```bash
cd backend && python start_server.py
```

**Frontend:**
```bash
cd frontend && npm run dev
```

Then visit http://localhost:3000 to use the application.

### Training Models
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
