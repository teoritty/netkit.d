"""Use case: Whois/ASN lookup for an IPv4 address."""
from __future__ import annotations

from src.application.dto.diagnostics_dto import WhoisRequest, WhoisResult
from src.application.ports.whois_port import WhoisPort
from src.domain.value_objects.ipv4_address import IPv4Address

__all__ = ["WhoisLookupUseCase"]


class WhoisLookupUseCase:
    """Performs a Whois lookup (IPv4 only) via the port."""

    def __init__(self, whois_port: WhoisPort) -> None:
        self._whois_port = whois_port

    def execute(self, request: WhoisRequest) -> WhoisResult:
        ip = IPv4Address(request.ip.strip())
        return self._whois_port.lookup(ip)
