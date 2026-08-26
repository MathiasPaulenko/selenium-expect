"""Base mixin for all assertion classes in selenium-expect."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from selenium_expect._config import (
    ExpectConfig,
    get_config,
)
from selenium_expect._config import (
    normalize_timeout as _normalize_timeout,
)
from selenium_expect._errors import AssertionFormatter
from selenium_expect._retry import retry_until

_logger = logging.getLogger("selenium_expect")


class AssertionMixin:
    """Base class for all assertion classes.

    Provides:
    - ``_run_assertion()``: retry loop + error formatting + negation logic
    - ``not_``: property returning a negated copy
    - ``_entity_description()``: override in subclasses
    - ``_get_element_html()``: override in subclasses
    """

    def __init__(
        self,
        target: Any,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        self._target = target
        self._config = config if config is not None else get_config()
        self._message = message
        self._negate = negate

    def _run_assertion(
        self,
        condition: Callable[[], tuple[bool, Any]],
        condition_name: str,
        expected: Any = None,
        entity: str | None = None,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Execute assertion with retry. Raises ``AssertionError`` on failure."""
        effective_timeout = (
            _normalize_timeout(timeout) if timeout is not None else self._config.timeout
        )
        if effective_timeout < 0:
            raise ValueError(f"timeout must be >= 0, got {effective_timeout}")
        if polling is None:
            effective_interval = self._config.polling_interval
            effective_intervals = self._config.polling_intervals
        elif isinstance(polling, list):
            if len(polling) == 0:
                raise ValueError("polling list must not be empty; use a float for fixed interval")
            effective_interval = 0.5
            effective_intervals = polling
        else:
            effective_interval = polling
            effective_intervals = None
        if effective_interval < 0:
            raise ValueError(f"polling interval must be >= 0, got {effective_interval}")
        if effective_intervals is not None:
            for i, interval in enumerate(effective_intervals):
                if interval < 0:
                    raise ValueError(f"polling_intervals[{i}] must be >= 0, got {interval}")

        result = retry_until(
            condition=condition,
            timeout=effective_timeout,
            polling_interval=effective_interval,
            polling_intervals=effective_intervals,
            debug=self._config.debug_mode,
        )

        passed = result.passed
        if self._negate:
            passed = not passed

        if passed:
            return

        entity_desc = entity if entity is not None else self._entity_description()
        element_html = self._get_element_html()

        error_msg = AssertionFormatter.format_error(
            entity=entity_desc,
            condition=condition_name,
            expected=expected,
            actual=result.actual_value,
            elapsed_ms=result.elapsed_ms,
            poll_count=result.poll_count,
            polling_interval=effective_interval,
            message=self._message,
            element_html=element_html,
            timeline=result.timeline,
        )

        self._take_screenshot_on_failure(condition_name)

        if self._config.soft_mode:
            from selenium_expect._soft import SoftAssertionCollector

            SoftAssertionCollector.add_failure(error_msg)
        else:
            raise AssertionError(error_msg)

    @property
    def not_(self) -> AssertionMixin:
        """Return a negated copy. Enables ``expect(x).not_.to_be_visible()``."""
        return self.__class__(
            target=self._target,
            config=self._config,
            message=self._message,
            negate=not self._negate,
        )

    def _entity_description(self) -> str:
        """Describe the target for error messages. Override in subclasses."""
        return repr(self._target)

    def _get_element_html(self) -> str | None:
        """Return element outerHTML for error context. Override in subclasses."""
        return None

    def _get_driver(self) -> Any:
        """Extract the WebDriver from the target for screenshots.

        Override in subclasses if the target is not a WebDriver itself.
        """
        target = self._target
        if hasattr(target, "save_screenshot"):
            return target
        parent = getattr(target, "parent", None)
        if parent is not None and hasattr(parent, "save_screenshot"):
            return parent
        return None

    def _take_screenshot_on_failure(self, condition_name: str) -> None:
        """Save a screenshot if ``screenshot_on_failure`` is enabled."""
        if not self._config.screenshot_on_failure:
            return

        driver = self._get_driver()
        if driver is None:
            return

        path = Path(self._config.screenshot_path or "./screenshots/")
        path.mkdir(parents=True, exist_ok=True)

        safe_name = re.sub(r"[^\w\-.]", "_", condition_name)[:80]
        timestamp = datetime.now(tz=UTC).strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}_{safe_name}.png"
        filepath = path / filename

        try:
            driver.save_screenshot(str(filepath))
            _logger.debug("Screenshot saved to %s", filepath)
        except Exception as exc:
            _logger.warning("Failed to save screenshot: %s", exc)

    def to_satisfy_all(
        self,
        *conditions: Callable[[Any], None],
    ) -> None:
        """Assert all conditions pass (AND). Each condition receives the target.

        Each condition is a callable responsible for its own retry/timeout.
        """
        from selenium_expect._compose import satisfy_all

        try:
            satisfy_all(self._target, *conditions, message=self._message)
        except AssertionError as exc:
            if self._negate:
                return
            self._raise_or_collect(exc)
        else:
            if self._negate:
                self._raise_or_collect(
                    AssertionError(
                        AssertionFormatter.format_error(
                            entity="composition",
                            condition="not to_satisfy_all",
                            expected="not all pass",
                            actual="all conditions passed",
                            elapsed_ms=0,
                            poll_count=len(conditions),
                            polling_interval=0.0,
                            message=self._message,
                        )
                    )
                )

    def to_satisfy_any(
        self,
        *conditions: Callable[[Any], None],
    ) -> None:
        """Assert at least one condition passes (OR).

        Each condition is a callable responsible for its own retry/timeout.
        """
        from selenium_expect._compose import satisfy_any

        try:
            satisfy_any(self._target, *conditions, message=self._message)
        except AssertionError as exc:
            if self._negate:
                return
            self._raise_or_collect(exc)
        else:
            if self._negate:
                self._raise_or_collect(
                    AssertionError(
                        AssertionFormatter.format_error(
                            entity="composition",
                            condition="not to_satisfy_any",
                            expected="none pass",
                            actual="at least one condition passed",
                            elapsed_ms=0,
                            poll_count=len(conditions),
                            polling_interval=0.0,
                            message=self._message,
                        )
                    )
                )

    def to_satisfy_none(
        self,
        *conditions: Callable[[Any], None],
    ) -> None:
        """Assert no condition passes (NOT).

        Each condition is a callable responsible for its own retry/timeout.
        """
        from selenium_expect._compose import satisfy_none

        try:
            satisfy_none(self._target, *conditions, message=self._message)
        except AssertionError as exc:
            if self._negate:
                return
            self._raise_or_collect(exc)
        else:
            if self._negate:
                self._raise_or_collect(
                    AssertionError(
                        AssertionFormatter.format_error(
                            entity="composition",
                            condition="not to_satisfy_none",
                            expected="at least one passes",
                            actual="no conditions passed",
                            elapsed_ms=0,
                            poll_count=len(conditions),
                            polling_interval=0.0,
                            message=self._message,
                        )
                    )
                )

    def _raise_or_collect(self, exc: AssertionError) -> None:
        """Raise *exc* or collect it in soft mode."""
        if self._config.soft_mode:
            from selenium_expect._soft import SoftAssertionCollector

            SoftAssertionCollector.add_failure(str(exc))
        else:
            raise exc

    def __getattr__(self, name: str) -> Any:
        """Dispatch to custom matchers registered via ``extend()``.

        Called only when normal attribute resolution fails, so existing
        methods take precedence.
        """
        from selenium_expect._matcher import CustomMatcherRegistry

        matcher_fn = CustomMatcherRegistry.get(name)
        if matcher_fn is None:
            raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")

        def _invoke(*args: Any, **kwargs: Any) -> None:
            target = self._target
            timeout = kwargs.pop("timeout", None)
            polling = kwargs.pop("polling", None)

            def condition() -> tuple[bool, Any]:
                return matcher_fn(target, *args, **kwargs)

            self._run_assertion(
                condition=condition,
                condition_name=name,
                expected=None,
                entity=None,
                timeout=timeout,
                polling=polling,
            )

        return _invoke
