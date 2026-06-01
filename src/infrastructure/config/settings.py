"""Infrastructure configuration.

Values come from environment variables with sensible defaults —
no hardcoding in the adapters. Platform detection selects the commands and encoding
for the subprocess diagnostic adapters.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

__all__ = ["Settings", "load_settings"]


@dataclass(frozen=True)
class Settings:
    is_windows: bool
    ping_timeout_seconds: int
    traceroute_timeout_seconds: int
    port_scan_timeout_seconds: float
    dns_timeout_seconds: int
    static_dir: str
    templates_dir: str

    @property
    def subprocess_encoding(self) -> str:
        return "cp866" if self.is_windows else "utf-8"


def load_settings() -> Settings:
    return Settings(
        is_windows=sys.platform.startswith("win"),
        ping_timeout_seconds=int(os.getenv("NETKIT_PING_TIMEOUT", "15")),
        traceroute_timeout_seconds=int(os.getenv("NETKIT_TRACEROUTE_TIMEOUT", "60")),
        port_scan_timeout_seconds=float(os.getenv("NETKIT_PORT_SCAN_TIMEOUT", "2.0")),
        dns_timeout_seconds=int(os.getenv("NETKIT_DNS_TIMEOUT", "5")),
        static_dir=os.getenv("NETKIT_STATIC_DIR", "static"),
        templates_dir=os.getenv("NETKIT_TEMPLATES_DIR", "templates"),
    )
