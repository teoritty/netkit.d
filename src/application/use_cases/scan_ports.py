"""Use case: scan TCP ports on a host."""
from __future__ import annotations

from src.application.dto.diagnostics_dto import (
    PortScanRequest,
    PortScanResult,
    PortStatus,
)
from src.application.ports.port_scan_port import PortScanPort
from src.domain.exceptions import ValidationError
from src.domain.value_objects.hostname import Hostname
from src.domain.value_objects.port import Port

__all__ = ["ScanPortsUseCase"]

_MAX_PORTS = 50


class ScanPortsUseCase:
    """Parses the port list, validates limits, and runs the scan."""

    def __init__(self, port_scan_port: PortScanPort) -> None:
        self._port_scan_port = port_scan_port

    async def execute(self, request: PortScanRequest) -> PortScanResult:
        host = Hostname(request.host.strip())
        ports = self._parse_ports(request.ports.strip())
        if len(ports) > _MAX_PORTS:
            raise ValidationError(f"At most {_MAX_PORTS} ports per request")
        statuses = await self._port_scan_port.scan(host, ports)
        return self._summarize(host, statuses)

    def _parse_ports(self, ports_str: str) -> list[Port]:
        numbers: set[int] = set()
        try:
            for part in ports_str.split(","):
                self._collect_part(part.strip(), numbers)
        except ValueError as error:
            raise ValidationError(
                "Invalid port format. Examples: 22,80,443 or 20-25"
            ) from error
        return [Port(number) for number in sorted(numbers)]

    def _collect_part(self, part: str, numbers: set[int]) -> None:
        if "-" in part:
            start, end = part.split("-", 1)
            numbers.update(range(int(start.strip()), int(end.strip()) + 1))
        else:
            numbers.add(int(part))

    def _summarize(self, host: Hostname, statuses: list[PortStatus]) -> PortScanResult:
        return PortScanResult(
            host=host.value,
            results=statuses,
            open=sum(1 for item in statuses if item.status == "open"),
            closed=sum(1 for item in statuses if item.status == "closed"),
            filtered=sum(1 for item in statuses if item.status == "filtered"),
        )
