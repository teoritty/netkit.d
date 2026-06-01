import pytest

from src.domain.exceptions import (
    InvalidHostnameError,
    InvalidPortError,
    InvalidPrefixLengthError,
    InvalidRangeError,
)
from src.domain.value_objects.hostname import Hostname
from src.domain.value_objects.ip_range import IpRange
from src.domain.value_objects.ipv4_address import IPv4Address
from src.domain.value_objects.port import Port
from src.domain.value_objects.prefix_length import PrefixLength


def test_port_out_of_range_raises():
    with pytest.raises(InvalidPortError):
        Port(70000)


def test_prefix_length_out_of_range_raises():
    with pytest.raises(InvalidPrefixLengthError):
        PrefixLength(33)


def test_hostname_with_spaces_raises():
    with pytest.raises(InvalidHostnameError):
        Hostname("bad host name")


def test_ip_range_reversed_raises():
    with pytest.raises(InvalidRangeError):
        IpRange(IPv4Address("10.0.0.10"), IPv4Address("10.0.0.1"))
