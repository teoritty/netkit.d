import pytest

from src.domain.exceptions import InvalidAddressError
from src.domain.value_objects.subnet import Subnet


def test_subnet_boundaries_for_24_network_returns_expected_addresses():
    subnet = Subnet.from_address_and_mask("192.168.1.0", "24")
    assert subnet.network_address == "192.168.1.0"
    assert subnet.first_usable == "192.168.1.1"
    assert subnet.last_usable == "192.168.1.254"
    assert subnet.broadcast_address == "192.168.1.255"
    assert subnet.usable_hosts == 254


def test_subnet_with_host_bits_is_normalized_to_network():
    subnet = Subnet.from_address_and_mask("192.168.1.10", "24")
    assert subnet.cidr == "192.168.1.0/24"


def test_subnet_with_invalid_ip_raises_domain_error():
    with pytest.raises(InvalidAddressError):
        Subnet.from_address_and_mask("999.1.1.1", "24")


def test_subnet_31_has_no_usable_hosts():
    subnet = Subnet("10.0.0.0/31")
    assert subnet.usable_hosts == 0
    assert subnet.first_usable == "10.0.0.0"
