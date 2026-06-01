"""Port: route tracing. Implemented in the infrastructure layer."""
from __future__ import annotations

from typing import Protocol

from src.application.dto.diagnostics_dto import TracerouteResult
from src.domain.value_objects.hostname import Hostname

__all__ = ["TraceroutePort"]


class TraceroutePort(Protocol):
    def trace(self, host: Hostname, max_hops: int) -> TracerouteResult:
        """Traces the route to a host and returns the result."""
        ...
