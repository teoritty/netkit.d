"""Domain service: group IP addresses by their network."""
from __future__ import annotations

import ipaddress

__all__ = ["NetworkGrouper"]


class NetworkGrouper:
    """Groups (IP, mask) pairs by the network they belong to.

    Invalid pairs are skipped silently — the original application's behavior.
    """

    def group(self, pairs: list[tuple[str, str]]) -> dict[str, list[str]]:
        groups: dict[str, list[str]] = {}
        for ip_value, mask_value in pairs:
            network = self._network_of(ip_value, mask_value)
            if network is None:
                continue
            groups.setdefault(network, []).append(f"{ip_value}/{mask_value}")
        return groups

    def _network_of(self, ip_value: str, mask_value: str) -> str | None:
        try:
            return str(ipaddress.ip_interface(f"{ip_value}/{mask_value}").network)
        except ValueError:
            return None
