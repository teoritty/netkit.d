import pytest

from src.application.dto.diagnostics_dto import (
    DnsRecordType,
    DnsRequest,
    DnsResult,
    PingRequest,
    PingResult,
    WhoisRequest,
)
from src.application.exceptions import PortUnavailableError
from src.application.use_cases.dns_lookup import DnsLookupUseCase
from src.application.use_cases.ping_host import PingHostUseCase
from src.application.use_cases.whois_lookup import WhoisLookupUseCase
from src.domain.exceptions import InvalidHostnameError, ValidationError
from src.domain.value_objects.hostname import Hostname
from src.infrastructure.diagnostics.unavailable_whois_adapter import UnavailableWhoisAdapter


class _RecordingPingPort:
    def __init__(self) -> None:
        self.last_count: int | None = None

    def ping(self, host: Hostname, count: int) -> PingResult:
        self.last_count = count
        return PingResult(output="ok", success=True)


def test_ping_clamps_count_to_five():
    port = _RecordingPingPort()
    PingHostUseCase(port).execute(PingRequest(host="example.com", count=99))
    assert port.last_count == 5


def test_ping_invalid_host_raises_domain_error():
    with pytest.raises(InvalidHostnameError):
        PingHostUseCase(_RecordingPingPort()).execute(PingRequest(host="bad host"))


def test_dns_empty_hostname_raises_validation_error():
    class _Port:
        def resolve(self, hostname: Hostname, record_type: DnsRecordType) -> DnsResult:
            raise AssertionError("must not be called")

    with pytest.raises(ValidationError):
        DnsLookupUseCase(_Port()).execute(DnsRequest(hostname="   "))


def test_whois_unavailable_adapter_raises_port_unavailable():
    use_case = WhoisLookupUseCase(UnavailableWhoisAdapter())
    with pytest.raises(PortUnavailableError):
        use_case.execute(WhoisRequest(ip="8.8.8.8"))
