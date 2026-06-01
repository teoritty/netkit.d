"""Use case: ping a host."""
from __future__ import annotations

from src.application.dto.diagnostics_dto import PingRequest, PingResult
from src.application.ports.ping_port import PingPort
from src.domain.value_objects.hostname import Hostname

__all__ = ["PingHostUseCase"]

_MAX_COUNT = 5


class PingHostUseCase:
    """Pings with a capped packet count."""

    def __init__(self, ping_port: PingPort) -> None:
        self._ping_port = ping_port

    def execute(self, request: PingRequest) -> PingResult:
        host = Hostname(request.host.strip())
        count = min(request.count, _MAX_COUNT)
        return self._ping_port.ping(host, count)
