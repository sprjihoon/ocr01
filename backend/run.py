#!/usr/bin/env python3
"""
Railway entry point for FastAPI backend.
"""

import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting FastAPI server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)