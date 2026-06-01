"""Use case: DNS record resolution."""
from __future__ import annotations

from src.application.dto.diagnostics_dto import DnsRequest, DnsResult
from src.application.ports.dns_port import DnsResolverPort
from src.domain.exceptions import ValidationError
from src.domain.value_objects.hostname import Hostname

__all__ = ["DnsLookupUseCase"]


class DnsLookupUseCase:
    """Resolves DNS records of the given type via the resolver port."""

    def __init__(self, dns_port: DnsResolverPort) -> None:
        self._dns_port = dns_port

    def execute(self, request: DnsRequest) -> DnsResult:
        if not request.hostname.strip():
            raise ValidationError("Provide a hostname or IP address")
        host = Hostname(request.hostname.strip())
        return self._dns_port.resolve(host, request.record_type)
