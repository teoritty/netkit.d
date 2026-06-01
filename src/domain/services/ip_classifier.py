"""Domain service: classify IP addresses by IANA/RFC category."""
from __future__ import annotations

import ipaddress

from src.domain.value_objects.address_class import AddressClass
from src.domain.value_objects.ipv4_address import IPv4Address
from src.domain.value_objects.ipv6_address import IPv6Address

__all__ = ["IpClassifier"]


class IpClassifier:
    """Determines the class of an IPv4/IPv6 address.

    The order of checks is significant and matches the original implementation.
    """

    def classify_ipv4(self, address: IPv4Address) -> AddressClass:
        return self._classify(ipaddress.IPv4Address(address.value))

    def classify_ipv6(self, address: IPv6Address) -> AddressClass:
        return self._classify(ipaddress.IPv6Address(address.value))

    def _classify(
        self, ip_obj: ipaddress.IPv4Address | ipaddress.IPv6Address
    ) -> AddressClass:
        if ip_obj.is_loopback:
            return AddressClass.LOOPBACK
        if ip_obj.is_multicast:
            return AddressClass.MULTICAST
        if ip_obj.is_reserved:
            return AddressClass.RESERVED
        if ip_obj.is_global:
            return AddressClass.GLOBAL
        if ip_obj.is_link_local:
            return AddressClass.LINK_LOCAL
        if ip_obj.is_private:
            return AddressClass.PRIVATE
        return AddressClass.UNSPECIFIED
