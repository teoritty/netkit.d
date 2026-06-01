"""Value object: IPv4 address.

An immutable object without identity. Validates its invariant in the constructor —
an invalid address cannot be created. Compared by value (dataclass eq/frozen).
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from src.domain.exceptions import InvalidAddressError

__all__ = ["IPv4Address"]


@dataclass(frozen=True)
class IPv4Address:
    """A valid IPv4 address. Stores the canonical string representation."""

    value: str

    def __post_init__(self) -> None:
        try:
            parsed = ipaddress.IPv4Address(self.value)
        except ValueError as error:
            raise InvalidAddressError(f"Invalid IPv4 address: {self.value}") from error
        object.__setattr__(self, "value", str(parsed))

    def as_int(self) -> int:
        return int(ipaddress.IPv4Address(self.value))
