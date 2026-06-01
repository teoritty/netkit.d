"""Pydantic request schemas for the diagnostics endpoints."""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator

from src.application.dto.diagnostics_dto import DnsRecordType

__all__ = [
    "PingRequestSchema",
    "TracerouteRequestSchema",
    "DnsRequestSchema",
    "WhoisRequestSchema",
    "PortScanRequestSchema",
]


class PingRequestSchema(BaseModel):
    host: str
    count: int = Field(default=4, ge=1)


class TracerouteRequestSchema(BaseModel):
    host: str
    max_hops: int = Field(default=15, ge=1)


class DnsRequestSchema(BaseModel):
    hostname: str
    record_type: DnsRecordType = DnsRecordType.A

    @field_validator("record_type", mode="before")
    @classmethod
    def _normalize_record_type(cls, value: object) -> object:
        return value.upper() if isinstance(value, str) else value


class WhoisRequestSchema(BaseModel):
    ip: str


class PortScanRequestSchema(BaseModel):
    host: str
    ports: str = "22,80,443"
