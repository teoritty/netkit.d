"""FastAPI application factory: mounts the presentation layer around the container."""
from __future__ import annotations

import mimetypes

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from src.api.container import Container
from src.api.middleware.error_handler import register_error_handlers
from src.api.routers import calculation_router, diagnostics_router, pages_router
from src.infrastructure.config.settings import Settings

__all__ = ["create_app"]


def create_app(container: Container, settings: Settings) -> FastAPI:
    _ensure_javascript_mime_type()
    app = FastAPI(title="Network Tools")
    app.state.container = container
    app.state.templates = Jinja2Templates(directory=settings.templates_dir)
    app.mount(
        "/static", StaticFiles(directory=settings.static_dir), name="static"
    )
    app.include_router(pages_router.router)
    app.include_router(calculation_router.router)
    app.include_router(diagnostics_router.router)
    register_error_handlers(app)
    return app


def _ensure_javascript_mime_type() -> None:
    # On some Windows environments .js is served as text/plain and the browser
    # refuses to load ES modules. Force-register the JS MIME type.
    mimetypes.add_type("text/javascript", ".js")
    mimetypes.add_type("text/javascript", ".mjs")
