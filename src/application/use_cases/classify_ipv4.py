"""Use case: IPv4 address class detection."""
from __future__ import annotations

from src.application.dto.calculation_dto import IpClassRequest, IpClassResult
from src.domain.services.ip_classifier import IpClassifier
from src.domain.value_objects.ipv4_address import IPv4Address

__all__ = ["ClassifyIpv4UseCase"]


class ClassifyIpv4UseCase:
    """Returns the class of an IPv4 address."""

    def __init__(self, classifier: IpClassifier) -> None:
        self._classifier = classifier

    def execute(self, request: IpClassRequest) -> IpClassResult:
        address_class = self._classifier.classify_ipv4(IPv4Address(request.ip_address))
        return IpClassResult(address_class=address_class.value)
