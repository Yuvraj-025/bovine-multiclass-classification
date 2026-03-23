# Bovine Multiclass Classification System 🐄 :contentReference[oaicite:0]{index=0}

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)

## Project Overview
**Bovine Multiclass Classification** is an AI-powered system designed to identify and classify diverse breeds of Indian cattle. By leveraging modern Deep Learning techniques, specifically Convolutional Neural Networks (CNNs), the project aims to provide an accurate and accessible tool for farmers, veterinarians, and agricultural researchers to recognize cattle breeds instantly from a single photograph.
The system is capable of distinguishing between **49 different breeds**, including prominent varieties like Amritmahal, Gir, Sahiwal, and many more. It provides a real-time prediction interface with confidence scores across multiple trained architectures, ranging from custom "Vanilla" CNNs to advanced Transfer Learning models like ResNet50.

## 🌐 Web Application
Our full-stack solution offers a seamless experience through an interactive web portal:
We've built a complete web application with React frontend and FastAPI backend that allows you to:
- Upload images of cows
- Select from multiple trained models
- Get instant breed predictions with confidence scores
See [Setup Instructions](SETUP.md) for detailed installation instructions.

## 📁 Project Structure

'''
cow_identification_project_AI/
├── backend/
│   ├── api/                 # API endpoints
│   ├── model_loader/        # Model management
│   ├── services/            # Business logic
│   ├── models/              # Trained models
│   ├── main.py              # FastAPI application
│   ├── start_server.py      # Server startup script
│   └── requirements.txt     # Dependencies
├── frontend/                # React frontend application
├── src/                     # Training scripts
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── models/                  # Symlink to backend/models for convenience
├── start-system.py          # Unified startup script
├── SETUP.md                 # Setup instructions
└── README.md                # Project documentation
'''

## ⚙️ Setup Instructions
### Prerequisites
- Python 3.7+
- Node.js 14+
- PyTorch
- torchvision

### Automated Installation
#### Option 1: Unified Startup (Recommended)
The easiest way to start both the frontend and backend is using the `start-system.py` script:

```bash
python start-system.py
'''

Option 2: Manual Start (Advanced)
If you need to start individual components:
Backend:
cd backend && python start_server.py
Frontend:
cd frontend && npm install
npm run dev
Then visit http://localhost:3000 to use the application.
Manual Installation Steps
1. Backend Setup
cd backend
pip install -r requirements.txt
python start_server.py
2. Frontend Setup
cd frontend
npm install
npm run dev

▶️ Usage Instructions
1. Start both backend and frontend servers (see Setup above)
2. Open your browser and go to http://localhost:3000
3. Select a model from the dropdown (models are automatically detected)
4. Drag and drop an image of a cow or click "Browse Files" to upload
5. Click "Predict" to classify the cow breed
6. View the predicted breed and confidence score

## 🧠 Models
Currently available models:
- cattle_cnn_model_lesslayers.pth - Simple CNN with fewer layers
- cattle_cnn_model_more.pth - More complex CNN with additional layers
- resnet50_cattle_classifier.pth - Transfer learning model based on ResNet50
- cattle_breed_classifier.pth - Optimized ResNet50-based classifier
Models will automatically appear in the model selector when placed in backend/models/.

## 🖼️ Screenshots
Screenshots
Upload UI
Prediction Result

## 🏗️ Training New Models
Training CNN Models
To train the vanilla CNN with more layers:
```bash
python src/train_cow_vanilla_lesslayers.py
To train the vanilla CNN with more layers:
```bash
python src/train_cow_vanilla_more.py
Note: You'll need to obtain the cattle breed dataset separately. See Dataset Information (docs/dataset.md).

Training ResNet50 Model
To train the model using ResNet50:
```bash
python src/train_resnet50_cattle.py

## 🔌 API Endpoints
GET /models
Returns a list of available models:
{
  "models": [
    "cattle_breed_classifier.pth",
    "resnet50_cattle_classifier.pth"
  ]
}
POST /predict
Accepts an image file and model name, returns prediction:
{
  "model_used": "cattle_breed_classifier.pth",
  "predicted_class": "Gir",
  "confidence": 0.9234
}
POST /reload-models
Reloads models from disk without restarting the server:
{
  "message": "Models reloaded successfully",
  "models": ["cattle_breed_classifier.pth", "resnet50_cattle_classifier.pth"]
}
'''


## ❓ Troubleshooting
Common Issues:
1. Backend server won't start
   - Ensure all dependencies are installed: pip install -r requirements.txt
   - Check that the models directory exists and contains .pth files
2. Frontend shows "No models available"
   - Ensure the backend server is running
   - Check that models exist in the backend models/ directory
   - Click "Reload Models" to refresh the model list
3. CORS errors
   - Ensure the backend is running on http://127.0.0.1:8000
   - Check that CORS middleware is enabled in main.py
4. Prediction fails with "Invalid file type"
   - Ensure you're uploading a valid image file (JPG, PNG, GIF)
   - Check that the file is not corrupted

## 📈 Future Improvements
- [ ] Add model performance metrics dashboard
- [ ] Implement model versioning system
- [ ] Add support for batch predictions
- [ ] Extend to other livestock species
- [ ] Mobile application development
- [ ] Enhanced data visualization features
- [ ] User authentication and history tracking

## 📄 License
This project is licensed under the MIT License - see the LICENSE (LICENSE) file for details.