"""Unit tests for selenium_expect._retry."""

from __future__ import annotations

import logging
import time

import pytest
from selenium.common.exceptions import (
    NoAlertPresentException,
    NoSuchElementException,
    StaleElementReferenceException,
)

from selenium_expect._retry import retry_until


class TestRetryUntilPass:
    def test_passes_immediately(self) -> None:
        result = retry_until(
            condition=lambda: (True, "ok"),
            timeout=1.0,
            polling_interval=0.1,
        )
        assert result.passed is True
        assert result.poll_count == 1

    def test_passes_after_retries(self) -> None:
        calls = {"n": 0}

        def condition() -> tuple[bool, str]:
            calls["n"] += 1
            if calls["n"] >= 3:
                return (True, "ok")
            return (False, "not yet")

        result = retry_until(condition, timeout=2.0, polling_interval=0.01)
        assert result.passed is True
        assert result.poll_count == 3

    def test_returns_correct_actual_value(self) -> None:
        result = retry_until(
            condition=lambda: (True, 42),
            timeout=1.0,
            polling_interval=0.1,
        )
        assert result.actual_value == 42

    def test_returns_elapsed_ms(self) -> None:
        result = retry_until(
            condition=lambda: (True, "ok"),
            timeout=1.0,
            polling_interval=0.1,
        )
        assert result.elapsed_ms >= 0

    def test_returns_poll_count(self) -> None:
        calls = {"n": 0}

        def condition() -> tuple[bool, str]:
            calls["n"] += 1
            if calls["n"] >= 2:
                return (True, "ok")
            return (False, "no")

        result = retry_until(condition, timeout=2.0, polling_interval=0.01)
        assert result.poll_count == 2

    def test_returns_timeline(self) -> None:
        result = retry_until(
            condition=lambda: (True, "ok"),
            timeout=1.0,
            polling_interval=0.1,
        )
        assert len(result.timeline) == 1
        assert result.timeline[0]["poll"] == 1
        assert result.timeline[0]["passed"] is True


class TestRetryUntilTimeout:
    def test_fails_on_timeout(self) -> None:
        result = retry_until(
            condition=lambda: (False, "never"),
            timeout=0.2,
            polling_interval=0.05,
        )
        assert result.passed is False

    def test_returns_last_actual_value(self) -> None:
        result = retry_until(
            condition=lambda: (False, "last value"),
            timeout=0.1,
            polling_interval=0.02,
        )
        assert result.actual_value == "last value"

    def test_respects_timeout_value(self) -> None:
        start = time.monotonic()
        retry_until(
            condition=lambda: (False, "no"),
            timeout=0.3,
            polling_interval=0.05,
        )
        elapsed = time.monotonic() - start
        assert elapsed >= 0.25  # approximately >= timeout


class TestRetryPollingIntervals:
    def test_fixed_interval(self) -> None:
        start = time.monotonic()
        retry_until(
            condition=lambda: (False, "no"),
            timeout=0.3,
            polling_interval=0.1,
        )
        elapsed = time.monotonic() - start
        # With 0.1s interval and 0.3s timeout, should take ~0.3s
        assert elapsed >= 0.2

    def test_backoff_schedule(self) -> None:
        intervals: list[float] = []
        poll_times: list[float] = []
        start = time.monotonic()

        def condition() -> tuple[bool, str]:
            poll_times.append(time.monotonic() - start)
            return (False, "no")

        retry_until(
            condition=condition,
            timeout=2.0,
            polling_intervals=[0.1, 0.3, 0.5],
        )
        # Verify that intervals between polls increase (backoff behavior).
        # Use generous tolerance to account for OS timer granularity (~15ms on Windows).
        for i in range(1, len(poll_times)):
            delta = poll_times[i] - poll_times[i - 1]
            intervals.append(delta)

        assert len(intervals) >= 2
        assert all(i > 0 for i in intervals)
        # With intervals [0.1, 0.3, 0.5], the second gap should be noticeably
        # larger than the first even with OS jitter.
        assert intervals[1] > intervals[0]

    def test_backoff_loops_after_exhaustion(self) -> None:
        poll_count = {"n": 0}

        def condition() -> tuple[bool, str]:
            poll_count["n"] += 1
            return (False, "no")

        result = retry_until(
            condition=condition,
            timeout=0.5,
            polling_intervals=[0.05, 0.1],
        )
        # Should have polled more than 2 times (intervals exhausted, last repeated)
        assert result.poll_count > 2


class TestRetryExceptions:
    def test_retries_on_stale_element(self) -> None:
        calls = {"n": 0}

        def condition() -> tuple[bool, str]:
            calls["n"] += 1
            if calls["n"] == 1:
                raise StaleElementReferenceException("stale")
            return (True, "ok")

        result = retry_until(condition, timeout=1.0, polling_interval=0.01)
        assert result.passed is True
        assert result.poll_count == 2

    def test_retries_on_no_such_element(self) -> None:
        calls = {"n": 0}

        def condition() -> tuple[bool, str]:
            calls["n"] += 1
            if calls["n"] == 1:
                raise NoSuchElementException("not found")
            return (True, "ok")

        result = retry_until(condition, timeout=1.0, polling_interval=0.01)
        assert result.passed is True

    def test_retries_on_no_alert_present(self) -> None:
        calls = {"n": 0}

        def condition() -> tuple[bool, str]:
            calls["n"] += 1
            if calls["n"] == 1:
                raise NoAlertPresentException("no alert")
            return (True, "ok")

        result = retry_until(condition, timeout=1.0, polling_interval=0.01)
        assert result.passed is True

    def test_does_not_retry_on_assertion_error(self) -> None:
        def condition() -> tuple[bool, str]:
            raise AssertionError("boom")

        with pytest.raises(AssertionError, match="boom"):
            retry_until(condition, timeout=1.0, polling_interval=0.01)

    def test_does_not_retry_on_type_error(self) -> None:
        def condition() -> tuple[bool, str]:
            raise TypeError("bad type")

        with pytest.raises(TypeError, match="bad type"):
            retry_until(condition, timeout=1.0, polling_interval=0.01)

    def test_retries_then_passes_after_exception(self) -> None:
        calls = {"n": 0}

        def condition() -> tuple[bool, str]:
            calls["n"] += 1
            if calls["n"] <= 2:
                raise StaleElementReferenceException("stale")
            return (True, "recovered")

        result = retry_until(condition, timeout=1.0, polling_interval=0.01)
        assert result.passed is True
        assert result.actual_value == "recovered"
        assert result.poll_count == 3


class TestRetryDebug:
    def test_debug_logs_each_poll(self, caplog: pytest.LogCaptureFixture) -> None:
        with caplog.at_level(logging.DEBUG, logger="selenium_expect"):
            retry_until(
                condition=lambda: (True, "ok"),
                timeout=1.0,
                polling_interval=0.1,
                debug=True,
            )
        debug_records = [r for r in caplog.records if r.levelno == logging.DEBUG]
        assert len(debug_records) >= 1
