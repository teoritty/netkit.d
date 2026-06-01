"""Port: TCP port scanning. Implemented in the infrastructure layer."""
from __future__ import annotations

from typing import Protocol

from src.application.dto.diagnostics_dto import PortStatus
from src.domain.value_objects.hostname import Hostname
from src.domain.value_objects.port import Port

__all__ = ["PortScanPort"]


class PortScanPort(Protocol):
    async def scan(self, host: Hostname, ports: list[Port]) -> list[PortStatus]:
        """Checks the state of a list of ports on a host."""
        ...
