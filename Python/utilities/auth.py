"""Path-based API secret validation for FastAPI endpoints."""
import os
from fastapi import HTTPException, status


def require_path_secret(api_secret: str) -> None:
    """Validate the secret embedded in the URL path."""

    expected_secret = os.getenv("API_PATH_SECRET")
    if not expected_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API_PATH_SECRET is not configured",
        )
    if api_secret != expected_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API secret",
        )



