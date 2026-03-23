# Cow Identification Project (AI)

This project uses Convolutional Neural Networks (CNNs) to identify different breeds of cattle from images.

## 🌐 Web Application (New!)

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

### Running the Web Application

#### Option 1: Using Batch Files (Windows)
```bash
# Start both backend and frontend servers (Windows only)
start-all.bat

# Or start individual components
start-backend.bat
start-frontend.bat
```

#### Option 2: Manual Start (Cross-platform)
```bash
# Start the backend server
cd backend && python start_server.py

# In a new terminal, start the frontend development server
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
