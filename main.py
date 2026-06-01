"""ASGI entry point: ``uvicorn main:app``."""
from __future__ import annotations

from composition_root import build_container
from src.api.app_factory import create_app
from src.infrastructure.config.settings import load_settings

settings = load_settings()
app = create_app(build_container(settings), settings)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000)
