"""Single schema for the error response body."""
from __future__ import annotations

from pydantic import BaseModel

__all__ = ["ErrorResponse"]


class ErrorResponse(BaseModel):
    error: str
