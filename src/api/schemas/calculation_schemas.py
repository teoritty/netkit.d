"""Pydantic request schemas for the calculation endpoints.

Request-shape validation (field presence/types) happens here, at the boundary;
business validation (address correctness, etc.) lives in the domain.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

__all__ = [
    "SubnetInfoRequestSchema",
    "NetworkPairSchema",
    "GroupRequestSchema",
    "IpClassRequestSchema",
    "Ipv6ConvertRequestSchema",
    "VlsmRequestSchema",
    "SupernetRequestSchema",
    "RangeRequestSchema",
]


class SubnetInfoRequestSchema(BaseModel):
    ip_address: str
    subnet_mask: str


class NetworkPairSchema(BaseModel):
    ip: str
    mask: str


class GroupRequestSchema(BaseModel):
    pairs: list[NetworkPairSchema] = Field(min_length=1)


class IpClassRequestSchema(BaseModel):
    ip_address: str


class Ipv6ConvertRequestSchema(BaseModel):
    address: str


class VlsmRequestSchema(BaseModel):
    network: str
    requirements: list[int] = Field(min_length=1)


class SupernetRequestSchema(BaseModel):
    networks: list[str] = Field(min_length=1)


class RangeRequestSchema(BaseModel):
    start_ip: str
    end_ip: str
