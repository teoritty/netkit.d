"""IP address class (a finite set of values)."""
from __future__ import annotations

from enum import Enum

__all__ = ["AddressClass"]


class AddressClass(str, Enum):
    """IP address category per IANA/RFC standards."""

    LOOPBACK = "Loopback"
    MULTICAST = "Multicast"
    RESERVED = "Reserved"
    GLOBAL = "Global"
    LINK_LOCAL = "Link-Local"
    PRIVATE = "Private"
    UNSPECIFIED = "Unspecified"
