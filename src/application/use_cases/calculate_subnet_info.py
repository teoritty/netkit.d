"""Use case: subnet parameter calculation."""
from __future__ import annotations

from src.application.dto.calculation_dto import SubnetInfoRequest, SubnetInfoResult
from src.domain.value_objects.subnet import Subnet

__all__ = ["CalculateSubnetInfoUseCase"]


class CalculateSubnetInfoUseCase:
    """Returns the boundaries and capacity of a subnet from an IP and mask."""

    def execute(self, request: SubnetInfoRequest) -> SubnetInfoResult:
        subnet = Subnet.from_address_and_mask(request.ip_address, request.subnet_mask)
        return SubnetInfoResult(
            hosts_count=f"{subnet.usable_hosts} (+2 reserved)",
            network_address=subnet.network_address,
            first_address=subnet.first_usable,
            last_address=subnet.last_usable,
            broadcast_address=subnet.broadcast_address,
        )
