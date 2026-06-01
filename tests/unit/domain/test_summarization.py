from src.domain.services.supernet_summarizer import SupernetSummarizer
from src.domain.value_objects.ip_range import IpRange
from src.domain.value_objects.ipv4_address import IPv4Address
from src.domain.value_objects.subnet import Subnet


def test_supernet_collapses_two_adjacent_24_into_23():
    result = SupernetSummarizer().summarize(
        [Subnet("192.168.0.0/24"), Subnet("192.168.1.0/24")]
    )
    assert len(result) == 1
    assert result[0].cidr == "192.168.0.0/23"


def test_ip_range_to_cidr_covers_64_addresses_with_single_26():
    ip_range = IpRange(IPv4Address("10.0.0.0"), IPv4Address("10.0.0.63"))
    networks = ip_range.to_cidr_networks()
    assert ip_range.address_count() == 64
    assert str(networks[0]) == "10.0.0.0/26"
