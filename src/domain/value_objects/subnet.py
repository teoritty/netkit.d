"""Value object: IPv4 network (address + prefix).

Encapsulates network-boundary calculations over the stdlib ``ipaddress`` (no I/O).
Uses ``strict=False`` so that host bits in the input do not cause
an error — this preserves the original application's behavior.
"""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from src.domain.exceptions import InvalidAddressError

__all__ = ["Subnet"]


@dataclass(frozen=True)
class Subnet:
    """IPv4 network. Built from a CIDR string or an address/mask pair."""

    cidr: str

    def __post_init__(self) -> None:
        try:
            network = ipaddress.ip_network(self.cidr, strict=False)
        except ValueError as error:
            raise InvalidAddressError(str(error)) from error
        object.__setattr__(self, "cidr", str(network))

    @classmethod
    def from_address_and_mask(cls, address: str, mask: str) -> Subnet:
        """Builds a network from an IP address and mask (a CIDR number or dotted mask)."""
        return cls(f"{address}/{mask}")

    @property
    def _network(self) -> ipaddress.IPv4Network | ipaddress.IPv6Network:
        return ipaddress.ip_network(self.cidr, strict=False)

    @property
    def network_address(self) -> str:
        return str(self._network.network_address)

    @property
    def broadcast_address(self) -> str:
        return str(self._network.broadcast_address)

    @property
    def netmask(self) -> str:
        return str(self._network.netmask)

    @property
    def prefix_length(self) -> int:
        return self._network.prefixlen

    @property
    def total_addresses(self) -> int:
        return self._network.num_addresses

    @property
    def usable_hosts(self) -> int:
        return max(0, self.total_addresses - 2)

    @property
    def first_usable(self) -> str:
        network = self._network
        if self.usable_hosts > 0:
            return str(network.network_address + 1)
        return str(network.network_address)

    @property
    def last_usable(self) -> str:
        network = self._network
        if self.usable_hosts > 0:
            return str(network.broadcast_address - 1)
        return str(network.broadcast_address)
