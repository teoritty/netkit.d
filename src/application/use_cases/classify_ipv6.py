"""Use case: IPv6 address class detection."""
from __future__ import annotations

from src.application.dto.calculation_dto import IpClassRequest, IpClassResult
from src.domain.services.ip_classifier import IpClassifier
from src.domain.value_objects.ipv6_address import IPv6Address

__all__ = ["ClassifyIpv6UseCase"]


class ClassifyIpv6UseCase:
    """Returns the class of an IPv6 address."""

    def __init__(self, classifier: IpClassifier) -> None:
        self._classifier = classifier

    def execute(self, request: IpClassRequest) -> IpClassResult:
        address_class = self._classifier.classify_ipv6(IPv6Address(request.ip_address))
        return IpClassResult(address_class=address_class.value)
