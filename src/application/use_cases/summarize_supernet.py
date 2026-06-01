"""Use case: summarize networks into supernets."""
from __future__ import annotations

from src.application.dto.calculation_dto import (
    NetworkSummaryItem,
    SupernetRequest,
    SupernetResult,
)
from src.domain.exceptions import ValidationError
from src.domain.services.supernet_summarizer import SupernetSummarizer
from src.domain.value_objects.subnet import Subnet

__all__ = ["SummarizeSupernetUseCase"]


class SummarizeSupernetUseCase:
    """Collapses a list of networks into the minimal set of supernets."""

    def __init__(self, summarizer: SupernetSummarizer) -> None:
        self._summarizer = summarizer

    def execute(self, request: SupernetRequest) -> SupernetResult:
        if not request.networks:
            raise ValidationError("Provide at least one network")
        parsed = [Subnet(value.strip()) for value in request.networks]
        collapsed = self._summarizer.summarize(parsed)
        return SupernetResult(
            summarized=[_to_item(net) for net in collapsed],
            input_count=len(parsed),
            output_count=len(collapsed),
        )


def _to_item(subnet: Subnet) -> NetworkSummaryItem:
    return NetworkSummaryItem(
        cidr=subnet.cidr,
        network=subnet.network_address,
        broadcast=subnet.broadcast_address,
        hosts=subnet.usable_hosts,
        prefix=subnet.prefix_length,
    )
