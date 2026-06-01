from src.domain.reference.port_services import describe_port, service_label
from src.domain.services.network_grouper import NetworkGrouper


def test_group_two_ips_in_same_network():
    groups = NetworkGrouper().group(
        [("192.168.1.10", "24"), ("192.168.1.99", "24")]
    )
    assert "192.168.1.0/24" in groups
    assert len(groups["192.168.1.0/24"]) == 2


def test_invalid_pair_is_skipped_silently():
    groups = NetworkGrouper().group([("not-an-ip", "24"), ("10.0.0.1", "8")])
    assert "10.0.0.0/8" in groups
    assert len(groups) == 1


def test_describe_known_port():
    assert "HTTPS" in (describe_port(443) or "")


def test_service_label_unknown_port_is_empty():
    assert service_label(1) == ""
