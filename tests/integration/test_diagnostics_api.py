"""Integration tests for the diagnostics endpoints (with fake ports)."""
from __future__ import annotations

from fastapi.testclient import TestClient


def test_ping_returns_fake_output(client: TestClient):
    response = client.post("/ping/", json={"host": "example.com", "count": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "example.com" in data["output"]


def test_ping_invalid_host_returns_400(client: TestClient):
    response = client.post("/ping/", json={"host": "bad host name"})
    assert response.status_code == 400
    assert "error" in response.json()


def test_dns_lookup_returns_records(client: TestClient):
    response = client.post("/dns_lookup/", json={"hostname": "example.com", "record_type": "a"})
    data = response.json()
    assert data["type"] == "A"
    assert data["records"] == ["93.184.216.34"]


def test_whois_returns_asn(client: TestClient):
    response = client.post("/whois/", json={"ip": "8.8.8.8"})
    assert response.json()["asn"] == "AS15169"


def test_port_scan_reports_open_ports(client: TestClient):
    response = client.post("/port_scan/", json={"host": "127.0.0.1", "ports": "22,80,443"})
    data = response.json()
    assert data["open"] == 3
    assert len(data["results"]) == 3


def test_port_scan_too_many_ports_returns_400(client: TestClient):
    response = client.post("/port_scan/", json={"host": "127.0.0.1", "ports": "1-100"})
    assert response.status_code == 400


def test_validation_error_is_normalized_to_error_key(client: TestClient):
    response = client.post("/vlsm/", json={"network": "192.168.1.0/24", "requirements": []})
    assert response.status_code == 400
    assert "error" in response.json()
