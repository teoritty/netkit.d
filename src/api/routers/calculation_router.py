"""Controllers for the calculation endpoints.

Each controller: deserializes the request -> builds a DTO -> calls the use case ->
returns a DTO (FastAPI serializes it to JSON). No business logic.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from src.api.container import Container
from src.api.dependencies import get_container
from src.api.schemas.calculation_schemas import (
    GroupRequestSchema,
    IpClassRequestSchema,
    Ipv6ConvertRequestSchema,
    RangeRequestSchema,
    SubnetInfoRequestSchema,
    SupernetRequestSchema,
    VlsmRequestSchema,
)
from src.application.dto.calculation_dto import (
    GroupRequest,
    IpClassRequest,
    Ipv6ConvertRequest,
    NetworkPairDTO,
    PortInfoRequest,
    RangeRequest,
    SubnetInfoRequest,
    SupernetRequest,
    VlsmRequest,
)

__all__ = ["router"]

router = APIRouter(tags=["calculations"])


@router.post("/calculate_network_info/")
def calculate_network_info(
    body: SubnetInfoRequestSchema, container: Container = Depends(get_container)
) -> object:
    request = SubnetInfoRequest(ip_address=body.ip_address, subnet_mask=body.subnet_mask)
    return container.calculate_subnet_info.execute(request)


@router.post("/find_same_network/")
def find_same_network(
    body: GroupRequestSchema, container: Container = Depends(get_container)
) -> object:
    pairs = [NetworkPairDTO(ip=pair.ip, mask=pair.mask) for pair in body.pairs]
    return container.group_by_network.execute(GroupRequest(pairs=pairs))


@router.post("/check_ip_class/")
def check_ip_class(
    body: IpClassRequestSchema, container: Container = Depends(get_container)
) -> object:
    return container.classify_ipv4.execute(IpClassRequest(ip_address=body.ip_address))


@router.post("/check_ipv6_class/")
def check_ipv6_class(
    body: IpClassRequestSchema, container: Container = Depends(get_container)
) -> object:
    return container.classify_ipv6.execute(IpClassRequest(ip_address=body.ip_address))


@router.get("/port_info")
def port_info(
    port: int = Query(...), container: Container = Depends(get_container)
) -> object:
    return container.lookup_port_info.execute(PortInfoRequest(port=port))


@router.post("/convert_ipv6/")
def convert_ipv6(
    body: Ipv6ConvertRequestSchema, container: Container = Depends(get_container)
) -> object:
    return container.convert_ipv6.execute(Ipv6ConvertRequest(address=body.address))


@router.post("/vlsm/")
def vlsm(
    body: VlsmRequestSchema, container: Container = Depends(get_container)
) -> object:
    request = VlsmRequest(network=body.network, requirements=body.requirements)
    return container.split_vlsm.execute(request)


@router.post("/supernet/")
def supernet(
    body: SupernetRequestSchema, container: Container = Depends(get_container)
) -> object:
    return container.summarize_supernet.execute(SupernetRequest(networks=body.networks))


@router.post("/ip_range_to_cidr/")
def ip_range_to_cidr(
    body: RangeRequestSchema, container: Container = Depends(get_container)
) -> object:
    request = RangeRequest(start_ip=body.start_ip, end_ip=body.end_ip)
    return container.range_to_cidr.execute(request)
