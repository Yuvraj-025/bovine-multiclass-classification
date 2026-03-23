import uvicorn
import os
import sys

if __name__ == "__main__":
    # Add the current directory to Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Change to the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["."]
    )