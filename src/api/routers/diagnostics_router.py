"""Controllers for the diagnostics endpoints (ping/traceroute/dns/whois/scan)."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from src.api.container import Container
from src.api.dependencies import get_container
from src.api.schemas.diagnostics_schemas import (
    DnsRequestSchema,
    PingRequestSchema,
    PortScanRequestSchema,
    TracerouteRequestSchema,
    WhoisRequestSchema,
)
from src.application.dto.diagnostics_dto import (
    DnsRequest,
    PingRequest,
    PortScanRequest,
    TracerouteRequest,
    WhoisRequest,
)

__all__ = ["router"]

router = APIRouter(tags=["diagnostics"])


@router.post("/ping/")
def ping(
    body: PingRequestSchema, container: Container = Depends(get_container)
) -> object:
    return container.ping_host.execute(PingRequest(host=body.host, count=body.count))


@router.post("/traceroute/")
def traceroute(
    body: TracerouteRequestSchema, container: Container = Depends(get_container)
) -> object:
    request = TracerouteRequest(host=body.host, max_hops=body.max_hops)
    return container.trace_route.execute(request)


@router.post("/dns_lookup/")
def dns_lookup(
    body: DnsRequestSchema, container: Container = Depends(get_container)
) -> object:
    request = DnsRequest(hostname=body.hostname, record_type=body.record_type)
    return container.dns_lookup.execute(request)


@router.post("/whois/")
def whois(
    body: WhoisRequestSchema, container: Container = Depends(get_container)
) -> object:
    return container.whois_lookup.execute(WhoisRequest(ip=body.ip))


@router.post("/port_scan/")
async def port_scan(
    body: PortScanRequestSchema, container: Container = Depends(get_container)
) -> object:
    return await container.scan_ports.execute(
        PortScanRequest(host=body.host, ports=body.ports)
    )
