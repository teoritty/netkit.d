"""Value object: the required host count for a subnet."""
from __future__ import annotations

from dataclasses import dataclass

from src.domain.value_objects.prefix_length import PrefixLength

__all__ = ["HostCount"]

_IPV4_MAX_BITS = 32


@dataclass(frozen=True)
class HostCount:
    """The number of hosts a subnet must accommodate."""

    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(f"Host count cannot be negative: {self.value}")

    def needed_prefix(self) -> PrefixLength:
        """The smallest IPv4 prefix that fits this host count (including 2 reserved)."""
        for prefix in range(_IPV4_MAX_BITS, -1, -1):
            if 2 ** (_IPV4_MAX_BITS - prefix) - 2 >= self.value:
                return PrefixLength(prefix)
        return PrefixLength(0)
