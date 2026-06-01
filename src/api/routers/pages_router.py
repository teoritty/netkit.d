"""Page controller: serves the SPA shell (index.html)."""
from __future__ import annotations

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

__all__ = ["router"]

router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    templates = request.app.state.templates
    return templates.TemplateResponse(request=request, name="index.html")
