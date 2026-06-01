"""DTOs for the diagnostics use cases (which perform I/O through ports).

They belong to one actor (network diagnostics). The same result DTOs
are returned by the infrastructure ports — the contract belongs to the application layer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

__all__ = [
    "DnsRecordType",
    "PingRequest",
    "PingResult",
    "TracerouteRequest",
    "TracerouteResult",
    "DnsRequest",
    "DnsResult",
    "WhoisRequest",
    "WhoisResult",
    "PortScanRequest",
    "PortStatus",
    "PortScanResult",
]


class DnsRecordType(str, Enum):
    """Supported DNS record types."""

    A = "A"
    AAAA = "AAAA"
    MX = "MX"
    TXT = "TXT"
    NS = "NS"
    CNAME = "CNAME"
    PTR = "PTR"


@dataclass(frozen=True)
class PingRequest:
    host: str
    count: int = 4


@dataclass(frozen=True)
class PingResult:
    output: str
    success: bool
    avg_ms: float | None = None


@dataclass(frozen=True)
class TracerouteRequest:
    host: str
    max_hops: int = 15


@dataclass(frozen=True)
class TracerouteResult:
    output: str
    success: bool


@dataclass(frozen=True)
class DnsRequest:
    hostname: str
    record_type: DnsRecordType = DnsRecordType.A


@dataclass(frozen=True)
class DnsResult:
    # records holds strings or dicts (for MX: {preference, exchange}),
    # so the type is intentionally broad — the format is kept from the original app.
    records: list[object]
    type: str
    hostname: str
    ttl: int | None = None


@dataclass(frozen=True)
class WhoisRequest:
    ip: str


@dataclass(frozen=True)
class WhoisResult:
    ip: str
    asn: str | None = None
    asn_cidr: str | None = None
    asn_country: str | None = None
    asn_description: str | None = None
    org: str | None = None
    abuse_emails: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PortScanRequest:
    host: str
    ports: str = "22,80,443"


@dataclass(frozen=True)
class PortStatus:
    port: int
    status: str
    service: str


@dataclass(frozen=True)
class PortScanResult:
    host: str
    results: list[PortStatus]
    open: int
    closed: int
    filtered: int
