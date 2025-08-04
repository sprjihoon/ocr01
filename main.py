#!/usr/bin/env python3
"""
Main entry point for Railway deployment.
Handles PORT environment variable correctly.
"""

import os
import sys
import subprocess

def main():
    # Get port from Railway environment
    port = os.environ.get("PORT", "8000")
    print(f"Railway PORT environment variable: {port}")
    
    # Change to backend directory and run the app
    backend_dir = os.path.join(os.path.dirname(__file__), "backend")
    os.chdir(backend_dir)
    
    # Run the backend application
    cmd = [sys.executable, "run.py"]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()