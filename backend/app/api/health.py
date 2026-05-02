"""Health check endpoint"""

from datetime import datetime
from typing import Any, Dict

from app.config import settings
from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Health check endpoint"
)
async def health_check() -> Dict[str, Any]:
    """
    Check if the service is healthy and running.
    
    Returns:
        Health status information including service name, version, and timestamp
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": "production" if settings.is_production else "development"
    }


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, str],
    summary="Readiness check endpoint"
)
async def readiness_check() -> Dict[str, str]:
    """
    Check if the service is ready to accept requests.
    
    Returns:
        Readiness status
    """
    # Add checks for dependencies (database, redis, etc.)
    return {
        "status": "ready"
    }

# Made with Bob
