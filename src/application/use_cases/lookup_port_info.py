"""Use case: network port information."""
from __future__ import annotations

from src.application.dto.calculation_dto import PortInfoRequest, PortInfoResult
from src.domain.reference.port_services import describe_port

__all__ = ["LookupPortInfoUseCase"]


class LookupPortInfoUseCase:
    """Returns the description of a known port."""

    def execute(self, request: PortInfoRequest) -> PortInfoResult:
        description = describe_port(request.port)
        if description is None:
            return PortInfoResult(message="No information")
        return PortInfoResult(service=description)
