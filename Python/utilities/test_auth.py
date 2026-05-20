import pytest
from fastapi import HTTPException

from utilities.auth import require_path_secret


def test_path_secret_valid(monkeypatch):
    monkeypatch.setenv("API_PATH_SECRET", "super-secret")
    require_path_secret("super-secret")

def test_path_secret_missing_env_raises(monkeypatch):
    monkeypatch.delenv("API_PATH_SECRET", raising=False)

    with pytest.raises(HTTPException) as exc:
        require_path_secret("anything")

    assert exc.value.status_code == 500


def test_path_secret_invalid_raises(monkeypatch):
    monkeypatch.setenv("API_PATH_SECRET", "super-secret")

    with pytest.raises(HTTPException) as exc:
        require_path_secret("wrong-secret")

    assert exc.value.status_code == 401



