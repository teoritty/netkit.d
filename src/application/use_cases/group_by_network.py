"""Use case: group IP addresses by their network."""
from __future__ import annotations

from src.application.dto.calculation_dto import GroupRequest, GroupResult
from src.domain.services.network_grouper import NetworkGrouper

__all__ = ["GroupByNetworkUseCase"]


class GroupByNetworkUseCase:
    """Groups IP/mask pairs by the network they belong to."""

    def __init__(self, grouper: NetworkGrouper) -> None:
        self._grouper = grouper

    def execute(self, request: GroupRequest) -> GroupResult:
        pairs = [(pair.ip, pair.mask) for pair in request.pairs]
        return GroupResult(networks=self._grouper.group(pairs))
