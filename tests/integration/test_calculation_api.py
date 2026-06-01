"""Integration tests for the calculation endpoints (new JSON contract)."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_index_served(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert "Network Tools" in response.text


def test_subnet_calculation(client: TestClient):
    response = client.post(
        "/calculate_network_info/", json={"ip_address": "192.168.1.0", "subnet_mask": "24"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["network_address"] == "192.168.1.0"
    assert data["first_address"] == "192.168.1.1"
    assert data["last_address"] == "192.168.1.254"
    assert data["broadcast_address"] == "192.168.1.255"


def test_subnet_invalid_ip_returns_400(client: TestClient):
    response = client.post(
        "/calculate_network_info/", json={"ip_address": "999.1.1.1", "subnet_mask": "24"}
    )
    assert response.status_code == 400
    assert "error" in response.json()


def test_ip_class_global(client: TestClient):
    response = client.post("/check_ip_class/", json={"ip_address": "8.8.8.8"})
    assert response.json()["address_class"] == "Global"


def test_ip_class_private(client: TestClient):
    response = client.post("/check_ip_class/", json={"ip_address": "192.168.1.1"})
    assert response.json()["address_class"] == "Private"


def test_ipv6_class_link_local(client: TestClient):
    response = client.post("/check_ipv6_class/", json={"ip_address": "fe80::1"})
    assert response.json()["address_class"] == "Link-Local"


def test_port_info_known(client: TestClient):
    response = client.get("/port_info", params={"port": 443})
    assert "HTTPS" in response.json()["service"]


def test_convert_ipv6(client: TestClient):
    response = client.post("/convert_ipv6/", json={"address": "2001:db8::1"})
    data = response.json()
    assert data["full"] == "2001:0db8:0000:0000:0000:0000:0000:0001"
    assert data["compact"] == "2001:db8::1"


def test_vlsm_split(client: TestClient):
    response = client.post(
        "/vlsm/", json={"network": "192.168.1.0/24", "requirements": [100, 50, 25]}
    )
    subnets = response.json()["subnets"]
    assert subnets[0]["subnet"] == "192.168.1.0/25"
    assert subnets[0]["hosts_available"] == 126
    assert subnets[1]["subnet"] == "192.168.1.128/26"
    assert subnets[2]["subnet"] == "192.168.1.192/27"


def test_supernet_summarization(client: TestClient):
    response = client.post(
        "/supernet/", json={"networks": ["192.168.0.0/24", "192.168.1.0/24"]}
    )
    summarized = response.json()["summarized"]
    assert len(summarized) == 1
    assert summarized[0]["cidr"] == "192.168.0.0/23"


def test_ip_range_to_cidr(client: TestClient):
    response = client.post(
        "/ip_range_to_cidr/", json={"start_ip": "10.0.0.0", "end_ip": "10.0.0.63"}
    )
    data = response.json()
    assert data["total_ips"] == 64
    assert data["cidrs"][0]["cidr"] == "10.0.0.0/26"


def test_find_same_network(client: TestClient):
    response = client.post(
        "/find_same_network/",
        json={
            "pairs": [
                {"ip": "192.168.1.10", "mask": "24"},
                {"ip": "192.168.1.99", "mask": "24"},
            ]
        },
    )
    networks = response.json()["networks"]
    assert "192.168.1.0/24" in networks
    assert len(networks["192.168.1.0/24"]) == 2
