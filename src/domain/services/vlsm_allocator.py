"""Domain service: greedy VLSM subnet allocation."""
from __future__ import annotations

import ipaddress
from dataclasses import dataclass

from src.domain.exceptions import InsufficientAddressSpaceError, TooManySubnetsError
from src.domain.value_objects.host_count import HostCount
from src.domain.value_objects.subnet import Subnet

__all__ = ["VlsmAllocation", "VlsmAllocator"]

_MAX_SUBNETS = 64


@dataclass(frozen=True)
class VlsmAllocation:
    """One allocated subnet and its original host-count requirement."""

    required_hosts: int
    subnet: Subnet


class VlsmAllocator:
    """Allocates subnets for host-count requirements, largest first."""

    def allocate(self, parent: Subnet, requirements: list[HostCount]) -> list[VlsmAllocation]:
        if len(requirements) > _MAX_SUBNETS:
            raise TooManySubnetsError(f"At most {_MAX_SUBNETS} subnets")

        parent_net = ipaddress.ip_network(parent.cidr, strict=False)
        ordered = sorted(requirements, key=lambda hosts: hosts.value, reverse=True)
        allocations: list[VlsmAllocation] = []
        current_address = parent_net.network_address

        for index, hosts in enumerate(ordered):
            prefix = hosts.needed_prefix()
            candidate = ipaddress.ip_network(
                f"{current_address}/{prefix.value}", strict=False
            )
            self._ensure_fits(parent_net, candidate, hosts.value)
            allocations.append(VlsmAllocation(hosts.value, Subnet(str(candidate))))

            current_address = candidate.broadcast_address + 1
            is_last = index == len(ordered) - 1
            if int(current_address) > int(parent_net.broadcast_address) and not is_last:
                raise InsufficientAddressSpaceError(
                    "Not enough address space for all subnets"
                )
        return allocations

    def _ensure_fits(
        self,
        parent_net: ipaddress.IPv4Network | ipaddress.IPv6Network,
        candidate: ipaddress.IPv4Network | ipaddress.IPv6Network,
        hosts_needed: int,
    ) -> None:
        if parent_net.supernet_of(candidate) or candidate == parent_net:
            return
        if (
            candidate.network_address < parent_net.network_address
            or candidate.broadcast_address > parent_net.broadcast_address
        ):
            raise InsufficientAddressSpaceError(
                f"Not enough address space for {hosts_needed} hosts"
            )
