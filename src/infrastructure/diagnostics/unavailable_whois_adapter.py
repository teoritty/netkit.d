"""Whois-port stub for when the ipwhois library is absent.

Preserves the original app's graceful-degradation behavior: the request
fails with a feature-unavailable error (HTTP 503).
"""
from __future__ import annotations

from src.application.dto.diagnostics_dto import WhoisResult
from src.application.exceptions import PortUnavailableError
from src.domain.value_objects.ipv4_address import IPv4Address

__all__ = ["UnavailableWhoisAdapter"]


class UnavailableWhoisAdapter:
    """``WhoisPort`` implementation that always reports unavailability."""

    def lookup(self, ip: IPv4Address) -> WhoisResult:
        raise PortUnavailableError("The ipwhois library is not installed")
