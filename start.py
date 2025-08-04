#!/usr/bin/env python3
"""
Railway startup script - completely new approach
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    # Import and run directly
    from app.main import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    print(f"=== Starting server on port {port} ===")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port,
        log_level="info"
    )