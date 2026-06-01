from src.domain.services.ip_classifier import IpClassifier
from src.domain.value_objects.address_class import AddressClass
from src.domain.value_objects.ipv4_address import IPv4Address
from src.domain.value_objects.ipv6_address import IPv6Address


def test_classify_public_ipv4_returns_global():
    assert IpClassifier().classify_ipv4(IPv4Address("8.8.8.8")) is AddressClass.GLOBAL


def test_classify_rfc1918_ipv4_returns_private():
    assert IpClassifier().classify_ipv4(IPv4Address("192.168.1.1")) is AddressClass.PRIVATE


def test_classify_ipv6_link_local():
    assert IpClassifier().classify_ipv6(IPv6Address("fe80::1")) is AddressClass.LINK_LOCAL


def test_ipv6_explode_and_compress():
    address = IPv6Address("2001:db8::1")
    assert address.exploded() == "2001:0db8:0000:0000:0000:0000:0000:0001"
    assert address.compressed() == "2001:db8::1"
