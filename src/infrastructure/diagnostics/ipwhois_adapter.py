"""Whois/ASN adapter over the ipwhois library (RDAP)."""
from __future__ import annotations

from typing import Any

from ipwhois import IPWhois

from src.application.dto.diagnostics_dto import WhoisResult
from src.application.exceptions import ExternalLookupError
from src.domain.value_objects.ipv4_address import IPv4Address

__all__ = ["IpwhoisAdapter"]

_MAX_ABUSE_EMAILS = 5


class IpwhoisAdapter:
    """``WhoisPort`` implementation via ipwhois RDAP lookup."""

    def lookup(self, ip: IPv4Address) -> WhoisResult:
        try:
            result = IPWhois(ip.value).lookup_rdap(depth=1)
        except Exception as error:  # ipwhois raises a variety of network/parsing errors
            raise ExternalLookupError(str(error)) from error

        org, abuse_emails = self._extract_contacts(result.get("objects", {}))
        return WhoisResult(
            ip=ip.value,
            asn=result.get("asn"),
            asn_cidr=result.get("asn_cidr"),
            asn_country=result.get("asn_country_code"),
            asn_description=result.get("asn_description"),
            org=org,
            abuse_emails=abuse_emails[:_MAX_ABUSE_EMAILS],
        )

    def _extract_contacts(
        self, entities: dict[str, Any]
    ) -> tuple[str | None, list[str]]:
        org: str | None = None
        emails: list[str] = []
        for entity in entities.values():
            contact = entity.get("contact") or {}
            if not contact:
                continue
            if org is None and contact.get("name"):
                org = contact["name"]
            self._collect_emails(contact.get("email", []), emails)
        return org, emails

    def _collect_emails(self, raw_emails: object, emails: list[str]) -> None:
        if not isinstance(raw_emails, list):
            return
        for item in raw_emails:
            value = item.get("value") if isinstance(item, dict) else str(item)
            if value and value not in emails:
                emails.append(value)
