"""Port: ICMP ping. Implemented in the infrastructure layer."""
from __future__ import annotations

from typing import Protocol

from src.application.dto.diagnostics_dto import PingResult
from src.domain.value_objects.hostname import Hostname

__all__ = ["PingPort"]


class PingPort(Protocol):
    def ping(self, host: Hostname, count: int) -> PingResult:
        """Sends a ping and returns the parsed result."""
        ...
