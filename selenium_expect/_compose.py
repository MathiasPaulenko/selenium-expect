"""Composition assertions — satisfy_all, satisfy_any, satisfy_none.

Each condition is a callable that receives the target and executes an
assertion (e.g. a lambda calling ``expect(el).to_be_visible()``).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from selenium_expect._errors import AssertionFormatter


def satisfy_all(
    target: Any,
    *conditions: Callable[[Any], None],
    message: str | None = None,
) -> None:
    """Assert all conditions pass (AND logic).

    Each condition is a callable that receives *target* and may raise
    ``AssertionError`` on failure. All must pass without raising.

    Each condition is responsible for its own retry/timeout via ``expect()``.
    """
    if not conditions:
        raise ValueError("satisfy_all requires at least one condition")
    failures: list[str] = []
    for i, cond in enumerate(conditions):
        try:
            cond(target)
        except AssertionError as exc:
            failures.append(f"condition {i}: {exc}")
    if failures:
        combined = "\n".join(failures)
        error_msg = AssertionFormatter.format_error(
            entity="composition",
            condition="to_satisfy_all",
            expected="all pass",
            actual=combined,
            elapsed_ms=0,
            poll_count=len(conditions),
            polling_interval=0.0,
            message=message,
        )
        raise AssertionError(error_msg)


def satisfy_any(
    target: Any,
    *conditions: Callable[[Any], None],
    message: str | None = None,
) -> None:
    """Assert at least one condition passes (OR logic).

    Each condition is a callable that receives *target* and may raise
    ``AssertionError`` on failure. At least one must pass without raising.

    Each condition is responsible for its own retry/timeout via ``expect()``.
    """
    if not conditions:
        raise ValueError("satisfy_any requires at least one condition")
    failures: list[str] = []
    for i, cond in enumerate(conditions):
        try:
            cond(target)
            return  # at least one passed
        except AssertionError as exc:
            failures.append(f"condition {i}: {exc}")
    combined = "\n".join(failures)
    error_msg = AssertionFormatter.format_error(
        entity="composition",
        condition="to_satisfy_any",
        expected="at least one pass",
        actual=combined,
        elapsed_ms=0,
        poll_count=len(conditions),
        polling_interval=0.0,
        message=message,
    )
    raise AssertionError(error_msg)


def satisfy_none(
    target: Any,
    *conditions: Callable[[Any], None],
    message: str | None = None,
) -> None:
    """Assert no condition passes (NOT logic).

    Each condition is a callable that receives *target* and may raise
    ``AssertionError``. All must raise (i.e. none pass).

    Each condition is responsible for its own retry/timeout via ``expect()``.
    """
    if not conditions:
        raise ValueError("satisfy_none requires at least one condition")
    passed: list[int] = []
    for i, cond in enumerate(conditions):
        try:
            cond(target)
            passed.append(i)
        except AssertionError:
            pass  # expected to fail
    if passed:
        error_msg = AssertionFormatter.format_error(
            entity="composition",
            condition="to_satisfy_none",
            expected="none pass",
            actual=f"conditions {passed} passed",
            elapsed_ms=0,
            poll_count=len(conditions),
            polling_interval=0.0,
            message=message,
        )
        raise AssertionError(error_msg)
