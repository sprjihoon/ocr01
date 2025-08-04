"""
Main entry point for Railway deployment.
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

if __name__ == "__main__":
    import uvicorn
    from app.main import app
    
    # Get port from environment variable
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}")
    
    uvicorn.run(app, host="0.0.0.0", port=port)