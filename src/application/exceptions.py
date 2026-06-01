"""Application-layer exceptions.

``InfrastructureError`` is the base class for failures of external adapters (I/O,
external commands/services). The API layer maps them to HTTP 5xx (or 408 for a timeout).
"""
from __future__ import annotations

__all__ = [
    "ApplicationError",
    "NotFoundError",
    "InfrastructureError",
    "PortUnavailableError",
    "ToolTimeoutError",
    "ToolNotFoundError",
    "ExternalLookupError",
]


class ApplicationError(Exception):
    """Base use-case error (mapped to HTTP 4xx)."""


class NotFoundError(ApplicationError):
    """The requested resource/record was not found (HTTP 404)."""


class InfrastructureError(Exception):
    """Base infrastructure failure. The message is safe to show to the user."""


class PortUnavailableError(InfrastructureError):
    """A required external capability is unavailable (e.g. a library is not installed)."""


class ToolTimeoutError(InfrastructureError):
    """An external command/query timed out."""


class ToolNotFoundError(InfrastructureError):
    """A system command was not found (e.g. ping/traceroute is missing)."""


class ExternalLookupError(InfrastructureError):
    """Failure while contacting an external name/data resolution service."""
