#!/usr/bin/env python3
"""
Startup Script for Cow Breed Classification System

This script provides an easy way to start both the frontend and backend
components of the cow breed classification system.
"""

import subprocess
import sys
import os
import time
import threading

def print_header(text):
    """Print a formatted header"""
    print("=" * 60)
    print(text.center(60))
    print("=" * 60)

def start_backend():
    """Start the backend server"""
    print_header("STARTING BACKEND SERVER")
    print("Initializing FastAPI backend on http://127.0.0.1:8000")
    
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), "backend")
        os.chdir(backend_dir)
        
        # Start the server
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
        
        print("✓ Backend server started successfully")
        print("  Access API documentation at: http://127.0.0.1:8000/docs")
        return process
        
    except Exception as e:
        print(f"✗ Failed to start backend: {e}")
        return None

def start_frontend():
    """Start the frontend development server"""
    print_header("STARTING FRONTEND SERVER")
    print("Initializing React frontend on http://localhost:3000")
    
    try:
        # Change to frontend directory
        frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
        os.chdir(frontend_dir)
        
        # Check if node_modules exists, if not install dependencies
        if not os.path.exists("node_modules"):
            print("Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start the development server
        process = subprocess.Popen(["npm", "run", "dev"])
        
        print("✓ Frontend server started successfully")
        print("  Access the application at: http://localhost:3000")
        return process
        
    except Exception as e:
        print(f"✗ Failed to start frontend: {e}")
        return None

def monitor_processes(processes):
    """Monitor running processes and handle cleanup"""
    try:
        while True:
            # Check if any process has terminated
            for name, process in processes.items():
                if process and process.poll() is not None:
                    print(f"\n⚠️  {name} process terminated unexpectedly")
                    return
                    
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
        for name, process in processes.items():
            if process:
                print(f"Stopping {name}...")
                process.terminate()
        print("👋 All services stopped. Goodbye!")

def main():
    """Main startup function"""
    print_header("COW BREED CLASSIFICATION SYSTEM STARTUP")
    
    # Dictionary to hold our processes
    processes = {}
    
    # Start backend
    original_dir = os.getcwd()
    processes["Backend"] = start_backend()
    
    # Change back to original directory
    os.chdir(original_dir)
    
    # Start frontend
    processes["Frontend"] = start_frontend()
    
    # Change back to original directory
    os.chdir(original_dir)
    
    # Check if both processes started successfully
    if all(process is not None for process in processes.values()):
        print_header("SYSTEM STARTED SUCCESSFULLY")
        print("📘 API Documentation: http://127.0.0.1:8000/docs")
        print("🌐 Web Application:   http://localhost:3000")
        print("📊 Available Models:  http://127.0.0.1:8000/models")
        print("\nPress Ctrl+C to stop all services")
        
        # Monitor processes
        monitor_processes(processes)
    else:
        print_header("STARTUP FAILED")
        print("❌ One or more services failed to start")
        print("💡 Check the error messages above for troubleshooting")

if __name__ == "__main__":
    main()