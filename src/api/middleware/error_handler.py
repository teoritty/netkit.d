"""Single mapping of application exceptions to HTTP responses.

Domain errors -> 4xx, infrastructure errors -> 5xx (timeout -> 408). The response body
is always normalized to ``{"error": "..."}``, as the frontend expects.
"""
from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.application.exceptions import (
    ExternalLookupError,
    InfrastructureError,
    NotFoundError,
    PortUnavailableError,
    ToolNotFoundError,
    ToolTimeoutError,
)
from src.domain.exceptions import DomainError

__all__ = ["register_error_handlers"]

# Order does not matter: Starlette selects the handler by the concrete exception class.
_STATUS_BY_EXCEPTION: tuple[tuple[type[Exception], int], ...] = (
    (NotFoundError, 404),
    (ToolTimeoutError, 408),
    (PortUnavailableError, 503),
    (ToolNotFoundError, 500),
    (ExternalLookupError, 500),
    (InfrastructureError, 500),
    (DomainError, 400),
)


def register_error_handlers(app: FastAPI) -> None:
    for exception_type, status_code in _STATUS_BY_EXCEPTION:
        app.add_exception_handler(exception_type, _build_handler(status_code))
    app.add_exception_handler(RequestValidationError, _handle_validation_error)


def _build_handler(status_code: int):
    async def handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status_code, content={"error": str(exc)})

    return handler


async def _handle_validation_error(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": _first_message(exc)})


def _first_message(exc: RequestValidationError) -> str:
    errors = exc.errors()
    if not errors:
        return "Invalid request data"
    first = errors[0]
    location = ".".join(str(part) for part in first.get("loc", ()) if part != "body")
    message = first.get("msg", "Invalid request data")
    return f"{location}: {message}" if location else message
