"""Port-scanner adapter over asyncio TCP connections."""
from __future__ import annotations

import asyncio

from src.application.dto.diagnostics_dto import PortStatus
from src.domain.reference.port_services import service_label
from src.domain.value_objects.hostname import Hostname
from src.domain.value_objects.port import Port
from src.infrastructure.config.settings import Settings

__all__ = ["AsyncioPortScanAdapter"]


class AsyncioPortScanAdapter:
    """``PortScanPort`` implementation via TCP connection attempts."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def scan(self, host: Hostname, ports: list[Port]) -> list[PortStatus]:
        tasks = [self._check_port(host.value, port.value) for port in ports]
        return list(await asyncio.gather(*tasks))

    async def _check_port(self, host: str, port: int) -> PortStatus:
        try:
            _, writer = await asyncio.wait_for(
                asyncio.open_connection(host, port),
                timeout=self._settings.port_scan_timeout_seconds,
            )
        except asyncio.TimeoutError:
            return PortStatus(port=port, status="filtered", service=service_label(port))
        except (ConnectionRefusedError, OSError):
            return PortStatus(port=port, status="closed", service=service_label(port))
        await self._close(writer)
        return PortStatus(port=port, status="open", service=service_label(port))

    async def _close(self, writer: asyncio.StreamWriter) -> None:
        writer.close()
        try:
            await writer.wait_closed()
        except OSError:
            pass
