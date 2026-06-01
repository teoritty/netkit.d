"""Traceroute port adapter over the system tracert/traceroute command."""
from __future__ import annotations

import subprocess

from src.application.dto.diagnostics_dto import TracerouteResult
from src.application.exceptions import ToolNotFoundError, ToolTimeoutError
from src.domain.value_objects.hostname import Hostname
from src.infrastructure.config.settings import Settings

__all__ = ["SubprocessTracerouteAdapter"]


class SubprocessTracerouteAdapter:
    """``TraceroutePort`` implementation via subprocess (platform-dependent)."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def trace(self, host: Hostname, max_hops: int) -> TracerouteResult:
        command = self._build_command(host.value, max_hops)
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self._settings.traceroute_timeout_seconds,
                encoding=self._settings.subprocess_encoding,
            )
        except subprocess.TimeoutExpired as error:
            raise ToolTimeoutError("Traceroute timed out") from error
        except FileNotFoundError as error:
            raise ToolNotFoundError("tracert/traceroute command not found") from error

        output = completed.stdout or completed.stderr
        return TracerouteResult(output=output, success=completed.returncode == 0)

    def _build_command(self, host: str, max_hops: int) -> list[str]:
        if self._settings.is_windows:
            return ["tracert", "-h", str(max_hops), "-d", host]
        return ["traceroute", "-m", str(max_hops), "-n", host]
