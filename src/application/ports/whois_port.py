"""Port: Whois/ASN lookup by IP. Implemented in the infrastructure layer."""
from __future__ import annotations

from typing import Protocol

from src.application.dto.diagnostics_dto import WhoisResult
from src.domain.value_objects.ipv4_address import IPv4Address

__all__ = ["WhoisPort"]


class WhoisPort(Protocol):
    def lookup(self, ip: IPv4Address) -> WhoisResult:
        """Performs an RDAP/Whois lookup for an IPv4 address."""
        ...
