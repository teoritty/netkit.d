"""Shared test fixtures.

Diagnostic ports are replaced with fakes — real ping/DNS/whois/scan
are never run in tests, so the suite is deterministic and CI-safe.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from composition_root import build_container
from src.api.app_factory import create_app
from src.api.container import Container
from src.application.dto.diagnostics_dto import (
    DnsRecordType,
    DnsResult,
    PingResult,
    PortStatus,
    TracerouteResult,
    WhoisResult,
)
from src.application.use_cases.dns_lookup import DnsLookupUseCase
from src.application.use_cases.ping_host import PingHostUseCase
from src.application.use_cases.scan_ports import ScanPortsUseCase
from src.application.use_cases.trace_route import TraceRouteUseCase
from src.application.use_cases.whois_lookup import WhoisLookupUseCase
from src.domain.value_objects.hostname import Hostname
from src.domain.value_objects.ipv4_address import IPv4Address
from src.domain.value_objects.port import Port
from src.infrastructure.config.settings import load_settings


class FakePingPort:
    def ping(self, host: Hostname, count: int) -> PingResult:
        return PingResult(output=f"PING {host.value} x{count}", success=True, avg_ms=1.0)


class FakeTraceroutePort:
    def trace(self, host: Hostname, max_hops: int) -> TracerouteResult:
        return TracerouteResult(output=f"traceroute {host.value} ({max_hops})", success=True)


class FakeDnsPort:
    def resolve(self, hostname: Hostname, record_type: DnsRecordType) -> DnsResult:
        return DnsResult(
            records=["93.184.216.34"], type=record_type.value, hostname=hostname.value, ttl=60
        )


class FakeWhoisPort:
    def lookup(self, ip: IPv4Address) -> WhoisResult:
        return WhoisResult(ip=ip.value, asn="AS15169", asn_country="US", org="Example Org")


class FakePortScanPort:
    async def scan(self, host: Hostname, ports: list[Port]) -> list[PortStatus]:
        return [PortStatus(port=p.value, status="open", service="") for p in ports]


@pytest.fixture
def container() -> Container:
    base = build_container(load_settings())
    return Container(
        calculate_subnet_info=base.calculate_subnet_info,
        group_by_network=base.group_by_network,
        classify_ipv4=base.classify_ipv4,
        classify_ipv6=base.classify_ipv6,
        lookup_port_info=base.lookup_port_info,
        convert_ipv6=base.convert_ipv6,
        split_vlsm=base.split_vlsm,
        summarize_supernet=base.summarize_supernet,
        range_to_cidr=base.range_to_cidr,
        ping_host=PingHostUseCase(FakePingPort()),
        trace_route=TraceRouteUseCase(FakeTraceroutePort()),
        dns_lookup=DnsLookupUseCase(FakeDnsPort()),
        whois_lookup=WhoisLookupUseCase(FakeWhoisPort()),
        scan_ports=ScanPortsUseCase(FakePortScanPort()),
    )


@pytest.fixture
def client(container: Container) -> TestClient:
    return TestClient(create_app(container, load_settings()))
