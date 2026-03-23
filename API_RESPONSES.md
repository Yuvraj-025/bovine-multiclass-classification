# API Response Examples

## GET /models

### Request
```bash
curl -X GET http://127.0.0.1:8000/models
```

### Successful Response
```json
{
  "models": [
    "cattle_breed_classifier.pth",
    "cattle_cnn_model.pth",
    "cattle_cnn_model_lesslayers.pth",
    "cattle_cnn_model_more.pth",
    "resnet50_cattle_classifier.pth"
  ]
}
```

## POST /predict

### Request
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -F "image=@/path/to/cow-image.jpg" \
  -F "model_name=cattle_breed_classifier.pth"
```

### Successful Response
```json
{
  "model_used": "cattle_breed_classifier.pth",
  "predicted_class": "Gir",
  "confidence": 0.9234
}
```

### Error Responses

#### Invalid File Type
```json
{
  "detail": "Invalid file type. Please upload an image."
}
```

#### Model Not Found
```json
{
  "detail": "Model 'nonexistent_model.pth' not found"
}
```

#### Server Error
```json
{
  "detail": "Prediction error: Expected tensor ... but got ..."
}
```

## POST /reload-models

### Request
```bash
curl -X POST http://127.0.0.1:8000/reload-models
```

### Successful Response
```json
{
  "message": "Models reloaded successfully",
  "models": [
    "cattle_breed_classifier.pth",
    "cattle_cnn_model.pth",
    "cattle_cnn_model_lesslayers.pth",
    "cattle_cnn_model_more.pth",
    "resnet50_cattle_classifier.pth"
  ]
}
```

### Error Response
```json
{
  "detail": "Error reloading models: [specific error message]"
}
```