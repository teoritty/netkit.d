"""DTOs for the calculation use cases (no I/O).

Grouped into one module because they belong to one actor (network calculations):
a change in calculation requirements is the only reason to change this file.
"""
from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "NetworkPairDTO",
    "SubnetInfoRequest",
    "SubnetInfoResult",
    "GroupRequest",
    "GroupResult",
    "IpClassRequest",
    "IpClassResult",
    "Ipv6ConvertRequest",
    "Ipv6ConvertResult",
    "PortInfoRequest",
    "PortInfoResult",
    "VlsmRequest",
    "VlsmSubnetResult",
    "VlsmResult",
    "NetworkSummaryItem",
    "SupernetRequest",
    "SupernetResult",
    "RangeRequest",
    "RangeResult",
]


@dataclass(frozen=True)
class SubnetInfoRequest:
    ip_address: str
    subnet_mask: str


@dataclass(frozen=True)
class SubnetInfoResult:
    hosts_count: str
    network_address: str
    first_address: str
    last_address: str
    broadcast_address: str


@dataclass(frozen=True)
class NetworkPairDTO:
    ip: str
    mask: str


@dataclass(frozen=True)
class GroupRequest:
    pairs: list[NetworkPairDTO]


@dataclass(frozen=True)
class GroupResult:
    networks: dict[str, list[str]]


@dataclass(frozen=True)
class IpClassRequest:
    ip_address: str


@dataclass(frozen=True)
class IpClassResult:
    address_class: str


@dataclass(frozen=True)
class Ipv6ConvertRequest:
    address: str


@dataclass(frozen=True)
class Ipv6ConvertResult:
    full: str
    compact: str


@dataclass(frozen=True)
class PortInfoRequest:
    port: int


@dataclass(frozen=True)
class PortInfoResult:
    service: str | None = None
    message: str | None = None


@dataclass(frozen=True)
class VlsmRequest:
    network: str
    requirements: list[int]


@dataclass(frozen=True)
class VlsmSubnetResult:
    required_hosts: int
    subnet: str
    prefix: int
    mask: str
    network: str
    first: str
    last: str
    broadcast: str
    hosts_available: int


@dataclass(frozen=True)
class VlsmResult:
    subnets: list[VlsmSubnetResult]
    parent: str


@dataclass(frozen=True)
class NetworkSummaryItem:
    cidr: str
    network: str
    broadcast: str
    hosts: int
    prefix: int


@dataclass(frozen=True)
class SupernetRequest:
    networks: list[str]


@dataclass(frozen=True)
class SupernetResult:
    summarized: list[NetworkSummaryItem]
    input_count: int
    output_count: int


@dataclass(frozen=True)
class RangeRequest:
    start_ip: str
    end_ip: str


@dataclass(frozen=True)
class RangeResult:
    cidrs: list[NetworkSummaryItem]
    total_ips: int
    blocks: int
