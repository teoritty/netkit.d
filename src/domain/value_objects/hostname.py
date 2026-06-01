"""Value object: hostname or IP address for diagnostic commands."""
from __future__ import annotations

import re
from dataclasses import dataclass

from src.domain.exceptions import InvalidHostnameError

__all__ = ["Hostname"]

_HOST_RE = re.compile(r"^[a-zA-Z0-9._-]{1,253}$")


@dataclass(frozen=True)
class Hostname:
    """A safe host/IP value to pass to external network commands."""

    value: str

    def __post_init__(self) -> None:
        if not _HOST_RE.match(self.value):
            raise InvalidHostnameError(f"Invalid host or IP address: {self.value!r}")
