# Cow Breed Classification Application Setup Guide

## Project Structure

```
cow_identification_project_AI/
├── backend/
│   ├── main.py                 # Main FastAPI application
│   ├── start_server.py         # Script to start the backend server
│   ├── requirements.txt        # Python dependencies
│   ├── model_loader/
│   │   └── model_manager.py    # Handles model loading and management
│   ├── services/
│   │   └── prediction_service.py # Handles image preprocessing and prediction
│   └── models/                 # Place your trained models here (already populated)
├── frontend/
│   ├── index.html              # Main HTML file
│   ├── package.json            # Frontend dependencies and scripts
│   ├── vite.config.js          # Vite configuration
│   └── src/
│       ├── main.jsx            # Entry point for React app
│       ├── App.jsx             # Main application component
│       └── components/         # Reusable UI components
└── README.md                   # Project overview (existing)
```

## Prerequisites

### Backend Requirements:
- Python 3.7+
- pip (Python package manager)

### Frontend Requirements:
- Node.js 14+
- npm (Node package manager)

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python start_server.py
```

The backend server will start on http://127.0.0.1:8000

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Usage Instructions

### Quick Start (Windows):
Double-click on `start-all.bat` to automatically start both backend and frontend servers.

### Quick Start (Linux/Mac):
Run the following command in terminal:
```bash
./start-all.sh
```

### Manual Start:
1. Make sure both backend and frontend servers are running:
   ```bash
   # Terminal 1 - Backend
   cd backend
   python start_server.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. Open your browser and go to http://localhost:3000
3. Select a model from the dropdown (models are automatically detected from the `models/` directory)
4. Drag and drop an image of a cow or click "Browse Files" to upload
5. Click "Predict" to classify the cow breed
6. View the predicted breed and confidence score

## API Endpoints

### GET /models
Returns a list of available models:
```json
{
  "models": [
    "cattle_breed_classifier.pth",
    "resnet50_cattle_classifier.pth"
  ]
}
```

### POST /predict
Accepts an image file and model name, returns prediction:
```json
{
  "model_used": "cattle_breed_classifier.pth",
  "predicted_class": "Gir",
  "confidence": 0.9234
}
```

### POST /reload-models
Reloads models from disk without restarting the server:
```json
{
  "message": "Models reloaded successfully",
  "models": ["cattle_breed_classifier.pth", "resnet50_cattle_classifier.pth"]
}
```

## Adding New Models

To add new models:
1. Place trained model files (`.pth`) in the `backend/models/` directory
2. Click "Reload Models" in the frontend or call the `/reload-models` endpoint
3. The new models will appear in the model selector dropdown

## Development Notes

### Backend
- The backend automatically scans the `models/` directory on startup
- Models are loaded using PyTorch
- Image preprocessing follows standard practices for computer vision models
- CORS is enabled for local development (configure origins for production)

### Frontend
- Built with React and Vite for fast development
- Uses TailwindCSS for styling (via CDN)
- Implements drag-and-drop file upload
- Provides visual feedback during loading states
- Responsive design works on desktop and mobile devices

## Troubleshooting

### Common Issues:

1. **Backend server won't start**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that the models directory exists and contains `.pth` files

2. **Frontend shows "No models available"**
   - Ensure the backend server is running
   - Check that models exist in the backend `models/` directory
   - Click "Reload Models" to refresh the model list

3. **CORS errors**
   - Ensure the backend is running on http://127.0.0.1:8000
   - Check that CORS middleware is enabled in `main.py`

4. **Prediction fails with "Invalid file type"**
   - Ensure you're uploading a valid image file (JPG, PNG, GIF)
   - Check that the file is not corrupted

### Startup Scripts

#### Windows (.bat files):
- `start-all.bat`: Starts both backend and frontend servers
- `start-backend.bat`: Starts only the backend server
- `start-frontend.bat`: Starts only the frontend server

#### Linux/Mac (.sh file):
- `start-all.sh`: Starts both backend and frontend servers

### For Production Deployment:

1. Update CORS settings in `main.py` to allow your frontend origin
2. Use a production WSGI server like Gunicorn instead of uvicorn
3. Consider deploying the frontend as a static site or with SSR
4. Secure the API with authentication if needed