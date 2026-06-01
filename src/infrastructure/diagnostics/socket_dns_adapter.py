"""Fallback socket-based DNS adapter (A records only).

Used when the dnspython library is unavailable — preserves partial
DNS-tool functionality, as in the original application.
"""
from __future__ import annotations

import socket

from src.application.dto.diagnostics_dto import DnsRecordType, DnsResult
from src.application.exceptions import NotFoundError, PortUnavailableError
from src.domain.value_objects.hostname import Hostname

__all__ = ["SocketDnsAdapter"]


class SocketDnsAdapter:
    """``DnsResolverPort`` implementation via ``socket.getaddrinfo`` (A-only)."""

    def resolve(self, hostname: Hostname, record_type: DnsRecordType) -> DnsResult:
        if record_type is not DnsRecordType.A:
            raise PortUnavailableError(
                "The dnspython library is not installed. Only the A type is supported."
            )
        try:
            infos = socket.getaddrinfo(hostname.value, None, socket.AF_INET)
        except socket.gaierror as error:
            raise NotFoundError(str(error)) from error
        records = sorted({info[4][0] for info in infos})
        return DnsResult(
            records=list(records), type="A", hostname=hostname.value, ttl=None
        )
