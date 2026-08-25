"""Base mixin for all assertion classes in selenium-expect."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from selenium_expect._config import ExpectConfig, get_config
from selenium_expect._errors import AssertionFormatter
from selenium_expect._retry import retry_until


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
        effective_timeout = timeout if timeout is not None else self._config.timeout
        if polling is None:
            effective_interval = self._config.polling_interval
            effective_intervals = self._config.polling_intervals
        elif isinstance(polling, list):
            effective_interval = 0.5
            effective_intervals = polling
        else:
            effective_interval = polling
            effective_intervals = None

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

    def to_satisfy_all(
        self,
        *conditions: Callable[[Any], None],
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert all conditions pass (AND). Each condition receives the target."""
        from selenium_expect._compose import satisfy_all

        satisfy_all(
            self._target,
            *conditions,
            timeout=timeout,
            polling=polling,
            message=self._message,
        )

    def to_satisfy_any(
        self,
        *conditions: Callable[[Any], None],
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert at least one condition passes (OR)."""
        from selenium_expect._compose import satisfy_any

        satisfy_any(
            self._target,
            *conditions,
            timeout=timeout,
            polling=polling,
            message=self._message,
        )

    def to_satisfy_none(
        self,
        *conditions: Callable[[Any], None],
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert no condition passes (NOT)."""
        from selenium_expect._compose import satisfy_none

        satisfy_none(
            self._target,
            *conditions,
            timeout=timeout,
            polling=polling,
            message=self._message,
        )

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
