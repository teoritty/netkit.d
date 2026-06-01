"""Dependency container: the assembled application use cases.

A plain immutable object (not a singleton or service locator) — the instance
is built in composition_root and placed in ``app.state`` to be read via Depends.
"""
from __future__ import annotations

from dataclasses import dataclass

from src.application.use_cases.calculate_subnet_info import CalculateSubnetInfoUseCase
from src.application.use_cases.classify_ipv4 import ClassifyIpv4UseCase
from src.application.use_cases.classify_ipv6 import ClassifyIpv6UseCase
from src.application.use_cases.convert_ipv6 import ConvertIpv6UseCase
from src.application.use_cases.dns_lookup import DnsLookupUseCase
from src.application.use_cases.group_by_network import GroupByNetworkUseCase
from src.application.use_cases.lookup_port_info import LookupPortInfoUseCase
from src.application.use_cases.ping_host import PingHostUseCase
from src.application.use_cases.range_to_cidr import RangeToCidrUseCase
from src.application.use_cases.scan_ports import ScanPortsUseCase
from src.application.use_cases.split_vlsm import SplitVlsmUseCase
from src.application.use_cases.summarize_supernet import SummarizeSupernetUseCase
from src.application.use_cases.trace_route import TraceRouteUseCase
from src.application.use_cases.whois_lookup import WhoisLookupUseCase

__all__ = ["Container"]


@dataclass(frozen=True)
class Container:
    calculate_subnet_info: CalculateSubnetInfoUseCase
    group_by_network: GroupByNetworkUseCase
    classify_ipv4: ClassifyIpv4UseCase
    classify_ipv6: ClassifyIpv6UseCase
    lookup_port_info: LookupPortInfoUseCase
    convert_ipv6: ConvertIpv6UseCase
    split_vlsm: SplitVlsmUseCase
    summarize_supernet: SummarizeSupernetUseCase
    range_to_cidr: RangeToCidrUseCase
    ping_host: PingHostUseCase
    trace_route: TraceRouteUseCase
    dns_lookup: DnsLookupUseCase
    whois_lookup: WhoisLookupUseCase
    scan_ports: ScanPortsUseCase
