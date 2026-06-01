"""Use case: convert IPv6 between full and compressed forms."""
from __future__ import annotations

from src.application.dto.calculation_dto import Ipv6ConvertRequest, Ipv6ConvertResult
from src.domain.value_objects.ipv6_address import IPv6Address

__all__ = ["ConvertIpv6UseCase"]


class ConvertIpv6UseCase:
    """Returns the expanded and compressed forms of an IPv6 address."""

    def execute(self, request: Ipv6ConvertRequest) -> Ipv6ConvertResult:
        address = IPv6Address(request.address)
        return Ipv6ConvertResult(full=address.exploded(), compact=address.compressed())
