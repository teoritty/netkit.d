"""FastAPI dependencies: access to the use-case container from ``app.state``."""
from __future__ import annotations

from fastapi import Request

from src.api.container import Container

__all__ = ["get_container"]


def get_container(request: Request) -> Container:
    """Returns the container built in composition_root at application startup."""
    container: Container = request.app.state.container
    return container
