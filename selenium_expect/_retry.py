"""Retry engine for selenium-expect assertions.

The retry loop is agnostic — it knows nothing about Selenium. It calls
a condition callable repeatedly until it returns ``(True, value)`` or
the timeout expires. Retryable Selenium exceptions are caught and
treated as a failed poll.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    NoSuchFrameException,
    NoSuchWindowException,
    StaleElementReferenceException,
)

logger = logging.getLogger("selenium_expect")

RETRYABLE_EXCEPTIONS: tuple[type[Exception], ...] = (
    StaleElementReferenceException,
    NoSuchElementException,
    NoAlertPresentException,
    NoSuchWindowException,
    NoSuchFrameException,
)


@dataclass(slots=True)
class RetryResult:
    """Result of a retry loop execution."""

    passed: bool
    actual_value: Any
    elapsed_ms: int
    poll_count: int
    timeline: list[dict[str, Any]] = field(default_factory=list)


def retry_until(
    condition: Callable[[], tuple[bool, Any]],
    timeout: float,
    polling_interval: float = 0.5,
    polling_intervals: list[float] | None = None,
    debug: bool = False,
) -> RetryResult:
    """Execute ``condition()`` repeatedly until it returns ``(True, value)`` or timeout.

    Args:
        condition: Callable returning ``(passed: bool, actual_value: Any)``.
        timeout: Maximum seconds to wait.
        polling_interval: Fixed seconds between polls.
        polling_intervals: Backoff schedule (overrides ``polling_interval``).
            When exhausted, the last interval is repeated.
        debug: If ``True``, log each poll via the ``logging`` module.

    Returns:
        ``RetryResult`` with pass/fail, actual value, elapsed time, and poll timeline.
    """
    start = time.monotonic()
    poll_count = 0
    timeline: list[dict[str, Any]] = []
    actual_value: Any = None

    def _get_interval(idx: int) -> float:
        if polling_intervals is None:
            return polling_interval
        if idx < len(polling_intervals):
            return polling_intervals[idx]
        return polling_intervals[-1]

    while True:
        elapsed = time.monotonic() - start
        if elapsed >= timeout:
            break

        poll_count += 1
        try:
            passed, actual_value = condition()
        except RETRYABLE_EXCEPTIONS as exc:
            passed = False
            actual_value = f"{type(exc).__name__}: {exc}"
            if debug:
                logger.debug(
                    "poll %d: retryable exception %s — %.1fms elapsed",
                    poll_count,
                    type(exc).__name__,
                    (time.monotonic() - start) * 1000,
                )
            timeline.append({"poll": poll_count, "passed": False, "actual": str(actual_value)})
            _sleep_and_check_timeout(start, timeout, _get_interval(poll_count - 1))
            continue

        if debug:
            logger.debug(
                "poll %d: passed=%s actual=%r — %.1fms elapsed",
                poll_count,
                passed,
                actual_value,
                (time.monotonic() - start) * 1000,
            )

        timeline.append({"poll": poll_count, "passed": passed, "actual": actual_value})

        if passed:
            return RetryResult(
                passed=True,
                actual_value=actual_value,
                elapsed_ms=int((time.monotonic() - start) * 1000),
                poll_count=poll_count,
                timeline=timeline,
            )

        _sleep_and_check_timeout(start, timeout, _get_interval(poll_count - 1))

    return RetryResult(
        passed=False,
        actual_value=actual_value,
        elapsed_ms=int((time.monotonic() - start) * 1000),
        poll_count=poll_count,
        timeline=timeline,
    )


def _sleep_and_check_timeout(start: float, timeout: float, interval: float) -> None:
    """Sleep for *interval* seconds, but not past the timeout deadline."""
    elapsed = time.monotonic() - start
    remaining = timeout - elapsed
    if remaining <= 0:
        return
    time.sleep(min(interval, remaining))
