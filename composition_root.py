"""Application composition root.

The single place where concrete port implementations are selected (including
optional ones) and use cases are assembled into a container with constructor injection.
No global singletons.
"""
from __future__ import annotations

from src.api.container import Container
from src.application.ports.dns_port import DnsResolverPort
from src.application.ports.whois_port import WhoisPort
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
from src.domain.services.ip_classifier import IpClassifier
from src.domain.services.network_grouper import NetworkGrouper
from src.domain.services.supernet_summarizer import SupernetSummarizer
from src.domain.services.vlsm_allocator import VlsmAllocator
from src.infrastructure.config.settings import Settings, load_settings
from src.infrastructure.diagnostics.asyncio_port_scan_adapter import AsyncioPortScanAdapter
from src.infrastructure.diagnostics.subprocess_ping_adapter import SubprocessPingAdapter
from src.infrastructure.diagnostics.subprocess_traceroute_adapter import (
    SubprocessTracerouteAdapter,
)

__all__ = ["build_container", "select_dns_adapter", "select_whois_adapter"]


def build_container(settings: Settings | None = None) -> Container:
    settings = settings or load_settings()
    grouper = NetworkGrouper()
    classifier = IpClassifier()
    return Container(
        calculate_subnet_info=CalculateSubnetInfoUseCase(),
        group_by_network=GroupByNetworkUseCase(grouper),
        classify_ipv4=ClassifyIpv4UseCase(classifier),
        classify_ipv6=ClassifyIpv6UseCase(classifier),
        lookup_port_info=LookupPortInfoUseCase(),
        convert_ipv6=ConvertIpv6UseCase(),
        split_vlsm=SplitVlsmUseCase(VlsmAllocator()),
        summarize_supernet=SummarizeSupernetUseCase(SupernetSummarizer()),
        range_to_cidr=RangeToCidrUseCase(),
        ping_host=PingHostUseCase(SubprocessPingAdapter(settings)),
        trace_route=TraceRouteUseCase(SubprocessTracerouteAdapter(settings)),
        dns_lookup=DnsLookupUseCase(select_dns_adapter(settings)),
        whois_lookup=WhoisLookupUseCase(select_whois_adapter()),
        scan_ports=ScanPortsUseCase(AsyncioPortScanAdapter(settings)),
    )


def select_dns_adapter(settings: Settings) -> DnsResolverPort:
    """Full dnspython resolver, or the fallback A-only socket resolver."""
    try:
        from src.infrastructure.diagnostics.dnspython_dns_adapter import (
            DnspythonDnsAdapter,
        )
    except ImportError:
        from src.infrastructure.diagnostics.socket_dns_adapter import SocketDnsAdapter

        return SocketDnsAdapter()
    return DnspythonDnsAdapter(settings)


def select_whois_adapter() -> WhoisPort:
    """ipwhois RDAP adapter, or a stub that errors with unavailability."""
    try:
        from src.infrastructure.diagnostics.ipwhois_adapter import IpwhoisAdapter
    except ImportError:
        from src.infrastructure.diagnostics.unavailable_whois_adapter import (
            UnavailableWhoisAdapter,
        )

        return UnavailableWhoisAdapter()
    return IpwhoisAdapter()
