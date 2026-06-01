"""Value object: a range of IPv4 addresses (start..end)."""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from src.domain.exceptions import InvalidRangeError
from src.domain.value_objects.ipv4_address import IPv4Address

__all__ = ["IpRange"]


@dataclass(frozen=True)
class IpRange:
    """A closed range of IPv4 addresses with the invariant start <= end."""

    start: IPv4Address
    end: IPv4Address

    def __post_init__(self) -> None:
        if self.start.as_int() > self.end.as_int():
            raise InvalidRangeError("Start IP must be less than or equal to end IP")

    def address_count(self) -> int:
        return self.end.as_int() - self.start.as_int() + 1

    def to_cidr_networks(self) -> list[ipaddress.IPv4Network]:
        """The minimal set of CIDR blocks covering the range."""
        first = ipaddress.IPv4Address(self.start.value)
        last = ipaddress.IPv4Address(self.end.value)
        return list(ipaddress.summarize_address_range(first, last))
