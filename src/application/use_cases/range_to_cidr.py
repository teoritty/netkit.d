"""Use case: convert an IPv4 range into a set of CIDR blocks."""
from __future__ import annotations

from src.application.dto.calculation_dto import (
    NetworkSummaryItem,
    RangeRequest,
    RangeResult,
)
from src.domain.value_objects.ip_range import IpRange
from src.domain.value_objects.ipv4_address import IPv4Address
from src.domain.value_objects.subnet import Subnet

__all__ = ["RangeToCidrUseCase"]


class RangeToCidrUseCase:
    """Returns the minimal set of CIDR blocks covering the range."""

    def execute(self, request: RangeRequest) -> RangeResult:
        ip_range = IpRange(
            IPv4Address(request.start_ip.strip()),
            IPv4Address(request.end_ip.strip()),
        )
        networks = [Subnet(str(net)) for net in ip_range.to_cidr_networks()]
        cidrs = [
            NetworkSummaryItem(
                cidr=net.cidr,
                network=net.network_address,
                broadcast=net.broadcast_address,
                hosts=net.usable_hosts,
                prefix=net.prefix_length,
            )
            for net in networks
        ]
        return RangeResult(
            cidrs=cidrs, total_ips=ip_range.address_count(), blocks=len(cidrs)
        )
