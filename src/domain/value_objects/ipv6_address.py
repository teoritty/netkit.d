"""Value object: IPv6 address.

An immutable object without identity; the invariant is validated in the constructor.
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from src.domain.exceptions import InvalidAddressError

__all__ = ["IPv6Address"]


@dataclass(frozen=True)
class IPv6Address:
    """A valid IPv6 address."""

    value: str

    def __post_init__(self) -> None:
        try:
            ipaddress.IPv6Address(self.value)
        except ValueError as error:
            raise InvalidAddressError(f"Invalid IPv6 address: {self.value}") from error

    def exploded(self) -> str:
        return ipaddress.IPv6Address(self.value).exploded

    def compressed(self) -> str:
        return ipaddress.IPv6Address(self.value).compressed
