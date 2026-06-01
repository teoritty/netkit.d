"""Domain exceptions.

All business-rule/invariant violations inherit from ``DomainError``.
The API layer maps them to HTTP 4xx via the single error handler.
"""
from __future__ import annotations

__all__ = [
    "DomainError",
    "ValidationError",
    "InvalidAddressError",
    "InvalidPrefixLengthError",
    "InvalidPortError",
    "InvalidHostnameError",
    "InvalidRangeError",
    "InsufficientAddressSpaceError",
    "TooManySubnetsError",
]


class DomainError(Exception):
    """Base domain exception. The message is safe to show to the user."""


class ValidationError(DomainError):
    """Violation of a general input-validation rule for a use case."""


class InvalidAddressError(DomainError):
    """Invalid IP address or network."""


class InvalidPrefixLengthError(DomainError):
    """Prefix length is out of the allowed range."""


class InvalidPortError(DomainError):
    """Port number is outside the 1..65535 range."""


class InvalidHostnameError(DomainError):
    """The hostname fails validation."""


class InvalidRangeError(DomainError):
    """Invalid address range (e.g. start greater than end)."""


class InsufficientAddressSpaceError(DomainError):
    """The parent network does not have enough address space for the request."""


class TooManySubnetsError(DomainError):
    """The subnet-count limit for a single request was exceeded."""
