"""Value object: network port number."""
from __future__ import annotations

from dataclasses import dataclass

from src.domain.exceptions import InvalidPortError

__all__ = ["Port"]

_MIN_PORT = 1
_MAX_PORT = 65535


@dataclass(frozen=True)
class Port:
    """TCP/UDP port number in the 1..65535 range."""

    value: int

    def __post_init__(self) -> None:
        if not _MIN_PORT <= self.value <= _MAX_PORT:
            raise InvalidPortError(
                f"Port must be in the {_MIN_PORT}..{_MAX_PORT} range, got {self.value}"
            )
