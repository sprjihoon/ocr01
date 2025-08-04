#!/usr/bin/env python3
"""
Simple Railway entry point - final approach
"""
import os
import sys

# Add backend to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import FastAPI app
from app.main import app

if __name__ == "__main__":
    import uvicorn
    
    # Get Railway port
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting Railway server on port {port}")
    print(f"🔧 Backend path: {backend_path}")
    print(f"🐍 Python version: {sys.version}")
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )