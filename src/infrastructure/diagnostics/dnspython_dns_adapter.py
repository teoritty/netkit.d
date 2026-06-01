"""DNS resolver adapter over the dnspython library (full support)."""
from __future__ import annotations

import ipaddress

import dns.resolver
import dns.reversename

from src.application.dto.diagnostics_dto import DnsRecordType, DnsResult
from src.application.exceptions import (
    ExternalLookupError,
    NotFoundError,
    ToolTimeoutError,
)
from src.domain.exceptions import ValidationError
from src.domain.value_objects.hostname import Hostname
from src.infrastructure.config.settings import Settings

__all__ = ["DnspythonDnsAdapter"]


class DnspythonDnsAdapter:
    """``DnsResolverPort`` implementation via dnspython."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def resolve(self, hostname: Hostname, record_type: DnsRecordType) -> DnsResult:
        resolver = self._build_resolver()
        try:
            answers = self._query(resolver, hostname.value, record_type)
        except dns.resolver.NXDOMAIN as error:
            raise NotFoundError(f"Domain '{hostname.value}' not found") from error
        except dns.resolver.NoAnswer as error:
            raise NotFoundError(
                f"No {record_type.value} records for '{hostname.value}'"
            ) from error
        except dns.resolver.Timeout as error:
            raise ToolTimeoutError("DNS query timed out") from error
        except dns.exception.DNSException as error:
            raise ExternalLookupError(str(error)) from error

        ttl = answers.rrset.ttl if answers.rrset else None
        records = [self._format(rdata, record_type) for rdata in answers]
        return DnsResult(
            records=records, type=record_type.value, hostname=hostname.value, ttl=ttl
        )

    def _build_resolver(self) -> dns.resolver.Resolver:
        resolver = dns.resolver.Resolver()
        resolver.timeout = self._settings.dns_timeout_seconds
        resolver.lifetime = self._settings.dns_timeout_seconds
        return resolver

    def _query(
        self, resolver: dns.resolver.Resolver, hostname: str, record_type: DnsRecordType
    ) -> dns.resolver.Answer:
        if record_type is DnsRecordType.PTR:
            return resolver.resolve(self._reverse_name(hostname), "PTR")
        return resolver.resolve(hostname, record_type.value)

    def _reverse_name(self, hostname: str) -> dns.name.Name:
        try:
            address = ipaddress.ip_address(hostname)
        except ValueError as error:
            raise ValidationError("Enter an IP address for a PTR query") from error
        return dns.reversename.from_address(str(address))

    def _format(self, rdata: object, record_type: DnsRecordType) -> object:
        if record_type is DnsRecordType.MX:
            return {"preference": rdata.preference, "exchange": str(rdata.exchange)}
        if record_type is DnsRecordType.TXT:
            return " ".join(
                segment.decode() if isinstance(segment, bytes) else segment
                for segment in rdata.strings
            )
        return str(rdata)
