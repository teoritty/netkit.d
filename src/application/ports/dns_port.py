"""Port: DNS record resolution. Implemented in the infrastructure layer."""
from __future__ import annotations

from typing import Protocol

from src.application.dto.diagnostics_dto import DnsRecordType, DnsResult
from src.domain.value_objects.hostname import Hostname

__all__ = ["DnsResolverPort"]


class DnsResolverPort(Protocol):
    def resolve(self, hostname: Hostname, record_type: DnsRecordType) -> DnsResult:
        """Resolves records of the given type for a host."""
        ...
