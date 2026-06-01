"""Use case: trace the route to a host."""
from __future__ import annotations

from src.application.dto.diagnostics_dto import TracerouteRequest, TracerouteResult
from src.application.ports.traceroute_port import TraceroutePort
from src.domain.value_objects.hostname import Hostname

__all__ = ["TraceRouteUseCase"]

_MAX_HOPS = 20


class TraceRouteUseCase:
    """Traces the route with a capped hop count."""

    def __init__(self, traceroute_port: TraceroutePort) -> None:
        self._traceroute_port = traceroute_port

    def execute(self, request: TracerouteRequest) -> TracerouteResult:
        host = Hostname(request.host.strip())
        max_hops = min(request.max_hops, _MAX_HOPS)
        return self._traceroute_port.trace(host, max_hops)
