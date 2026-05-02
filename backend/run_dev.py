"""
Development server runner for Process Doctor backend
"""

import os
import sys

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn
    from app.config import settings
    
    print("=" * 60)
    print(f"Starting {settings.app_name} Development Server")
    print("=" * 60)
    print(f"Host: {settings.backend_host}")
    print(f"Port: {settings.backend_port}")
    print(f"Debug: {settings.debug}")
    print(f"API Docs: http://{settings.backend_host}:{settings.backend_port}/docs")
    print("=" * 60)
    
    # Check if API keys are configured
    if not settings.granite_api_key or settings.granite_api_key == "your_granite_api_key_here":
        print("\n⚠️  WARNING: API keys not configured!")
        print("Please update backend/.env with your actual API keys")
        print("The server will start but API calls will fail without valid keys\n")
    
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )

# Made with Bob
