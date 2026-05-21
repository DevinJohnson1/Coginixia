"""Path-based API secret validation for FastAPI endpoints."""
import hashlib
import os
import secrets
import hmac
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 150000
SALT_BYTES = 16
bearer_scheme = HTTPBearer(auto_error=False)


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


def require_register_token(register_token: str) -> None:
    """Validate the registration token before allowing account creation."""

    expected_token = os.getenv("REGISTER_TOKEN")
    if not expected_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="REGISTER_TOKEN is not configured",
        )
    if not register_token or not hmac.compare_digest(register_token, expected_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid registration token",
        )


def hash_password(password: str) -> str:
    """Hash a password using PBKDF2 with a random salt."""

    if not password or len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters",
        )

    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )
    return f"pbkdf2_{PBKDF2_ALGORITHM}${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plaintext password against a PBKDF2 hash string."""

    try:
        method, iterations_str, salt_hex, digest_hex = stored_hash.split("$")
        algorithm = method.replace("pbkdf2_", "", 1)
        iterations = int(iterations_str)
        expected = bytes.fromhex(digest_hex)
        salt = bytes.fromhex(salt_hex)
    except (ValueError, TypeError):
        return False

    candidate = hashlib.pbkdf2_hmac(
        algorithm,
        password.encode("utf-8"),
        salt,
        iterations,
    )
    return hmac.compare_digest(candidate, expected)


def create_session_token() -> str:
    """Generate a strong random token for bearer auth sessions."""

    return secrets.token_urlsafe(48)


def extract_bearer_token(credentials: HTTPAuthorizationCredentials | None) -> str:
    """Extract and validate a bearer token from authorization credentials."""

    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    return credentials.credentials



