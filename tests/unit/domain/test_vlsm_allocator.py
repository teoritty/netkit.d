import pytest

from src.domain.exceptions import InsufficientAddressSpaceError
from src.domain.services.vlsm_allocator import VlsmAllocator
from src.domain.value_objects.host_count import HostCount
from src.domain.value_objects.subnet import Subnet


def test_allocate_three_requirements_returns_descending_prefixes():
    allocations = VlsmAllocator().allocate(
        Subnet("192.168.1.0/24"), [HostCount(100), HostCount(50), HostCount(25)]
    )
    assert allocations[0].subnet.cidr == "192.168.1.0/25"
    assert allocations[0].subnet.usable_hosts == 126
    assert allocations[1].subnet.cidr == "192.168.1.128/26"
    assert allocations[2].subnet.cidr == "192.168.1.192/27"


def test_allocate_raises_when_space_exhausted():
    with pytest.raises(InsufficientAddressSpaceError):
        VlsmAllocator().allocate(
            Subnet("192.168.1.0/29"), [HostCount(100), HostCount(100)]
        )
