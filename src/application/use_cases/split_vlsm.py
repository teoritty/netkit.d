"""Use case: split a network into subnets using VLSM."""
from __future__ import annotations

from src.application.dto.calculation_dto import VlsmRequest, VlsmResult, VlsmSubnetResult
from src.domain.exceptions import ValidationError
from src.domain.services.vlsm_allocator import VlsmAllocation, VlsmAllocator
from src.domain.value_objects.host_count import HostCount
from src.domain.value_objects.subnet import Subnet

__all__ = ["SplitVlsmUseCase"]


class SplitVlsmUseCase:
    """Allocates subnets for a list of host-count requirements."""

    def __init__(self, allocator: VlsmAllocator) -> None:
        self._allocator = allocator

    def execute(self, request: VlsmRequest) -> VlsmResult:
        if not request.requirements:
            raise ValidationError("Provide a list of host requirements")
        parent = Subnet(request.network)
        requirements = [HostCount(value) for value in request.requirements]
        allocations = self._allocator.allocate(parent, requirements)
        return VlsmResult(
            subnets=[self._to_result(item) for item in allocations],
            parent=parent.cidr,
        )

    def _to_result(self, allocation: VlsmAllocation) -> VlsmSubnetResult:
        subnet = allocation.subnet
        return VlsmSubnetResult(
            required_hosts=allocation.required_hosts,
            subnet=subnet.cidr,
            prefix=subnet.prefix_length,
            mask=subnet.netmask,
            network=subnet.network_address,
            first=subnet.first_usable,
            last=subnet.last_usable,
            broadcast=subnet.broadcast_address,
            hosts_available=subnet.usable_hosts,
        )
