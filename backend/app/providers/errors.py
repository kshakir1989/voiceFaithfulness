"""Provider errors mapped to API codes."""

from __future__ import annotations


class ProviderError(Exception):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class RateLimitedError(ProviderError):
    def __init__(self, message: str = "Free-tier rate limit reached.") -> None:
        super().__init__("rate_limited", message)
