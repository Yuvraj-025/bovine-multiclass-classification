#!/usr/bin/env python3
"""
Simple API Server for Cattle Breed Classification
This script creates a simple HTTP server that exposes the model prediction functionality
via REST API endpoints.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
from model_predictor import predict_model

class ModelAPIServer(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "message": "Cattle Breed Classification API",
                "endpoints": {
                    "/predict": "POST endpoint for predictions"
                },
                "models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/models':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response, indent=2).encode())

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/predict':
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse JSON data
                data = json.loads(post_data.decode('utf-8'))
                
                # Extract parameters
                model_type = data.get('model')
                image_path = data.get('image_path')
                
                # Validate inputs
                if not model_type:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": "Missing 'model' parameter"}
                    self.wfile.write(json.dumps(response, indent=2).encode())
                    return
                    
                if not image_path:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": "Missing 'image_path' parameter"}
                    self.wfile.write(json.dumps(response, indent=2).encode())
                    return
                
                if model_type not in ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        "error": f"Invalid model type: {model_type}",
                        "available_models": ["lesslayers", "morelayers", "resnet50", "cattle_breed_classifier"]
                    }
                    self.wfile.write(json.dumps(response, indent=2).encode())
                    return
                
                if not os.path.exists(image_path):
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {"error": f"Image file not found: {image_path}"}
                    self.wfile.write(json.dumps(response, indent=2).encode())
                    return
                
                # Run prediction
                result = predict_model(model_type, image_path)
                
                # Send successful response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(result, indent=2).encode())
                
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": "Invalid JSON in request body"}
                self.wfile.write(json.dumps(response, indent=2).encode())
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"error": f"Prediction failed: {str(e)}"}
                self.wfile.write(json.dumps(response, indent=2).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Endpoint not found"}
            self.wfile.write(json.dumps(response, indent=2).encode())

def run_server(port=8000):
    """Start the HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ModelAPIServer)
    print(f"Starting server on port {port}...")
    print(f"API endpoints:")
    print(f"  GET  http://localhost:{port}/ - API info")
    print(f"  GET  http://localhost:{port}/models - Available models")
    print(f"  POST http://localhost:{port}/predict - Make predictions")
    print("\nExample POST request body:")
    print('{')
    print('  "model": "lesslayers",')
    print('  "image_path": "/path/to/image.jpg"')
    print('}')
    httpd.serve_forever()

if __name__ == '__main__':
    import sys
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    run_server(port)