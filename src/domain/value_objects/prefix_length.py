"""Value object: network prefix length (CIDR)."""
from __future__ import annotations

from dataclasses import dataclass

from src.domain.exceptions import InvalidPrefixLengthError

__all__ = ["PrefixLength"]

_IPV4_MAX_BITS = 32


@dataclass(frozen=True)
class PrefixLength:
    """IPv4 network prefix length (0..32)."""

    value: int
    max_bits: int = _IPV4_MAX_BITS

    def __post_init__(self) -> None:
        if not 0 <= self.value <= self.max_bits:
            raise InvalidPrefixLengthError(
                f"Prefix length must be in the 0..{self.max_bits} range, got {self.value}"
            )

    def host_bits(self) -> int:
        return self.max_bits - self.value
