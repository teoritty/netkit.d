"""Parser for ping command output: extracts the average RTT.

Kept in a separate module so the parsing can be tested on captured strings
without running a real ping. Supports Russian/English Windows and Unix.
"""
from __future__ import annotations

import re

__all__ = ["parse_average_ms"]

_WINDOWS_PATTERNS = (
    re.compile(r"Среднее\s*=\s*(\d+)"),
    re.compile(r"Average\s*=\s*(\d+)"),
)
_UNIX_PATTERN = re.compile(r"rtt.+?=\s*[\d.]+/([\d.]+)/")


def parse_average_ms(output: str, is_windows: bool) -> float | None:
    """Returns the average RTT in milliseconds, or ``None``."""
    if is_windows:
        match = _first_match(output, _WINDOWS_PATTERNS)
    else:
        match = _UNIX_PATTERN.search(output)
    return float(match.group(1)) if match else None


def _first_match(output: str, patterns: tuple[re.Pattern[str], ...]) -> re.Match[str] | None:
    for pattern in patterns:
        match = pattern.search(output)
        if match:
            return match
    return None
