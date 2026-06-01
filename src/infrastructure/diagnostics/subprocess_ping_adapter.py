"""Ping port adapter over the system ``ping`` command."""
from __future__ import annotations

import subprocess

from src.application.dto.diagnostics_dto import PingResult
from src.application.exceptions import ToolNotFoundError, ToolTimeoutError
from src.infrastructure.config.settings import Settings
from src.infrastructure.mappers.ping_output_parser import parse_average_ms
from src.domain.value_objects.hostname import Hostname

__all__ = ["SubprocessPingAdapter"]


class SubprocessPingAdapter:
    """``PingPort`` implementation via subprocess (platform-dependent)."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def ping(self, host: Hostname, count: int) -> PingResult:
        command = self._build_command(host.value, count)
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self._settings.ping_timeout_seconds,
                encoding=self._settings.subprocess_encoding,
            )
        except subprocess.TimeoutExpired as error:
            raise ToolTimeoutError("Timeout — host is not responding") from error
        except FileNotFoundError as error:
            raise ToolNotFoundError("ping command not found") from error

        output = completed.stdout or completed.stderr
        return PingResult(
            output=output,
            success=completed.returncode == 0,
            avg_ms=parse_average_ms(output, self._settings.is_windows),
        )

    def _build_command(self, host: str, count: int) -> list[str]:
        flag = "-n" if self._settings.is_windows else "-c"
        return ["ping", flag, str(count), host]
