"""Domain service: summarize (aggregate) networks into supernets."""
from __future__ import annotations

import ipaddress

from src.domain.exceptions import InvalidAddressError
from src.domain.value_objects.subnet import Subnet

__all__ = ["SupernetSummarizer"]


class SupernetSummarizer:
    """Collapses a list of networks into the minimal set of supernets."""

    def summarize(self, networks: list[Subnet]) -> list[Subnet]:
        parsed = [ipaddress.ip_network(net.cidr, strict=False) for net in networks]
        try:
            collapsed = ipaddress.collapse_addresses(parsed)
        except (TypeError, ValueError) as error:
            raise InvalidAddressError(str(error)) from error
        return [Subnet(str(net)) for net in collapsed]
