"""PollAssertion — retry-based assertions over arbitrary functions.

``poll(fn)`` wraps any zero-arg callable and provides Playwright-style
assertion methods that retry until the function's return value satisfies
the condition or the timeout expires.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from selenium_expect._config import ExpectConfig, get_config
from selenium_expect._errors import AssertionFormatter
from selenium_expect._retry import retry_until


class PollAssertion:
    """Assertion over an arbitrary function with retry loop."""

    def __init__(
        self,
        fn: Callable[[], Any],
        timeout: float | None = None,
        polling: float | list[float] | None = None,
        config: ExpectConfig | None = None,
    ) -> None:
        self._fn = fn
        self._config = config if config is not None else get_config()
        self._timeout = timeout if timeout is not None else self._config.timeout
        if polling is None:
            self._polling_interval = self._config.polling_interval
            self._polling_intervals = self._config.polling_intervals
        elif isinstance(polling, list):
            self._polling_interval = 0.5
            self._polling_intervals = polling
        else:
            self._polling_interval = polling
            self._polling_intervals = None

    def _run(
        self,
        condition: Callable[[], tuple[bool, Any]],
        condition_name: str,
        expected: Any = None,
    ) -> None:
        """Execute the retry loop and raise on failure."""
        result = retry_until(
            condition=condition,
            timeout=self._timeout,
            polling_interval=self._polling_interval,
            polling_intervals=self._polling_intervals,
            debug=self._config.debug_mode,
        )
        if result.passed:
            return
        error_msg = AssertionFormatter.format_error(
            entity="poll()",
            condition=condition_name,
            expected=expected,
            actual=result.actual_value,
            elapsed_ms=result.elapsed_ms,
            poll_count=result.poll_count,
            polling_interval=self._polling_interval,
            timeline=result.timeline,
        )
        if self._config.soft_mode:
            from selenium_expect._soft import SoftAssertionCollector

            SoftAssertionCollector.add_failure(error_msg)
        else:
            raise AssertionError(error_msg)

    def to_equal(self, expected: Any) -> None:
        """Assert fn() == expected."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (actual == expected, actual)

        self._run(condition, f"to equal {expected!r}", expected)

    def to_be_truthy(self) -> None:
        """Assert bool(fn()) is True."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (bool(actual), actual)

        self._run(condition, "to be truthy", True)

    def to_be_falsy(self) -> None:
        """Assert bool(fn()) is False."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (not bool(actual), actual)

        self._run(condition, "to be falsy", False)

    def to_be_none(self) -> None:
        """Assert fn() is None."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (actual is None, actual)

        self._run(condition, "to be None", None)

    def to_contain(self, expected: Any) -> None:
        """Assert expected in fn()."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (expected in (actual or ""), actual)

        self._run(condition, f"to contain {expected!r}", expected)

    def to_match(self, pattern: str) -> None:
        """Assert re.search(pattern, str(fn()))."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (re.search(pattern, str(actual)) is not None, actual)

        self._run(condition, f"to match {pattern!r}", pattern)

    def to_be_greater_than(self, expected: Any) -> None:
        """Assert fn() > expected."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (actual > expected, actual)

        self._run(condition, f"to be greater than {expected}", expected)

    def to_be_less_than(self, expected: Any) -> None:
        """Assert fn() < expected."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (actual < expected, actual)

        self._run(condition, f"to be less than {expected}", expected)

    def to_be_in_list(self, expected: list[Any]) -> None:
        """Assert fn() in expected."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            return (actual in expected, actual)

        self._run(condition, f"to be in {expected!r}", expected)

    def to_have_length(self, expected: int) -> None:
        """Assert len(fn()) == expected."""
        fn = self._fn

        def condition() -> tuple[bool, Any]:
            actual = fn()
            try:
                actual_len = len(actual)
            except TypeError:
                return (False, f"no len() for {actual!r}")
            return (actual_len == expected, actual_len)

        self._run(condition, f"to have length {expected}", expected)


def poll(
    fn: Callable[[], Any],
    *,
    timeout: float | None = None,
    polling: float | list[float] | None = None,
    config: ExpectConfig | None = None,
) -> PollAssertion:
    """Create a ``PollAssertion`` for retry-based assertions on *fn*.

    Usage::

        expect.poll(lambda: driver.execute_script("return document.readyState"))
            .to_equal("complete")
    """
    return PollAssertion(fn, timeout=timeout, polling=polling, config=config)
