"""Configuration for selenium-expect assertions."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from dataclasses import replace as _replace
from typing import Any


def normalize_timeout(timeout: float) -> float:
    """Convert timeout to seconds.

    Any value >= 1000 is interpreted as milliseconds; smaller values
    are treated as seconds.
    """
    if timeout >= 1000:
        return timeout / 1000.0
    return float(timeout)


@dataclass(frozen=True, slots=True)
class ExpectConfig:
    """Immutable configuration for expect assertions.

    Use ``replace()`` to create a new instance with overridden fields.
    The global config singleton is mutated via the module-level setters.
    """

    timeout: float = 5.0
    polling_interval: float = 0.5
    polling_intervals: Sequence[float] | None = None
    screenshot_on_failure: bool = False
    screenshot_path: str | None = None
    debug_mode: bool = False
    soft_mode: bool = False

    def __post_init__(self) -> None:
        if self.timeout < 0:
            raise ValueError(f"timeout must be >= 0, got {self.timeout}")
        if self.polling_interval < 0:
            raise ValueError(f"polling_interval must be >= 0, got {self.polling_interval}")
        if self.polling_intervals is not None:
            # Store as tuple so the frozen dataclass is truly immutable.
            object.__setattr__(self, "polling_intervals", tuple(self.polling_intervals))
            if len(self.polling_intervals) == 0:
                raise ValueError("polling_intervals must not be empty; use None for fixed interval")
            for i, interval in enumerate(self.polling_intervals):
                if interval < 0:
                    raise ValueError(f"polling_intervals[{i}] must be >= 0, got {interval}")

    def replace(self, **kwargs: Any) -> ExpectConfig:
        """Return a new instance with overridden fields."""
        return _replace(self, **kwargs)


_global_config: ExpectConfig = ExpectConfig()


def set_default_timeout(seconds: float) -> None:
    """Set the default timeout for all expect assertions.

    Any value >= 1000 is interpreted as milliseconds
    (consistent with ``expect(timeout=...)``).
    """
    global _global_config
    _global_config = _global_config.replace(timeout=normalize_timeout(seconds))


def set_default_polling_interval(seconds: float) -> None:
    """Set the default polling interval for all expect assertions."""
    global _global_config
    _global_config = _global_config.replace(polling_interval=seconds)


def set_default_polling_intervals(intervals: Sequence[float]) -> None:
    """Set a backoff schedule for polling intervals."""
    global _global_config
    _global_config = _global_config.replace(polling_intervals=intervals)


def set_screenshot_on_failure(enabled: bool, path: str | None = None) -> None:
    """Enable or disable screenshot capture on assertion failure."""
    global _global_config
    _global_config = _global_config.replace(
        screenshot_on_failure=enabled,
        screenshot_path=path if path is not None else "./screenshots/",
    )


def set_debug_mode(enabled: bool) -> None:
    """Enable or disable debug logging for retry loops."""
    global _global_config
    _global_config = _global_config.replace(debug_mode=enabled)


def get_config() -> ExpectConfig:
    """Return the current global config."""
    return _global_config
