"""expect() entry point — dispatches to the correct assertion class."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, cast

from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from selenium_expect._config import ExpectConfig, get_config, normalize_timeout
from selenium_expect._poll import PollAssertion
from selenium_expect.assertions import ASSERTION_REGISTRY
from selenium_expect.assertions._base import AssertionMixin


def _resolve_target_type(target: Any) -> str:
    """Determine the registry type name for *target*.

    Select is checked before WebElement because Select wraps a WebElement.
    """
    if isinstance(target, Select):
        return "Select"
    if isinstance(target, WebElement):
        return "WebElement"
    if isinstance(target, list):
        return "list"
    if isinstance(target, WebDriver):
        return "WebDriver"
    if isinstance(target, Alert):
        return "Alert"
    if isinstance(target, ShadowRoot):
        return "ShadowRoot"
    cls_name = type(target).__name__
    if cls_name == "WebDriver":
        return "WebDriver"
    if cls_name == "Alert":
        return "Alert"
    return cls_name


class Expect:
    """Callable expect dispatcher with attached utilities.

    Use ``expect(target)`` to create assertions, ``expect.poll(fn)`` for
    retry-based polling, and ``expect.configure(...)`` for pre-configured
    variants.
    """

    def __call__(
        self,
        target: Any,
        /,
        *,
        message: str | None = None,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
        soft: bool | None = None,
        config: ExpectConfig | None = None,
        by: str | None = None,
        value: str | None = None,
        locator: tuple[str, str] | None = None,
    ) -> AssertionMixin:
        """Create an expect assertion for the given target.

        Dispatches to the appropriate assertion class via ``ASSERTION_REGISTRY``
        based on the target's type.

        If ``by`` and ``value`` are provided, a ``LocatorExpect`` is created
        that re-finds the element on each poll cycle.

        Alternatively, ``locator=(By.ID, 'foo')`` can be used as a tuple
        shorthand for ``by=..., value=...``.
        """
        if locator is not None:
            if by is not None or value is not None:
                raise ValueError("Cannot use both 'locator' and 'by/value' arguments")
            by, value = locator

        if (by is not None) != (value is not None):
            raise ValueError("Must provide both 'by' and 'value', or neither")

        if by is not None and value is not None:
            from selenium_expect._locator import LocatorExpect

            if not isinstance(target, WebDriver):
                raise TypeError("expect() with by/value requires a WebDriver target")

            effective_config = config if config is not None else get_config()
            if timeout is not None or polling is not None or soft is not None:
                overrides: dict[str, Any] = {}
                if timeout is not None:
                    overrides["timeout"] = normalize_timeout(timeout)
                if polling is not None:
                    if isinstance(polling, list):
                        overrides["polling_intervals"] = polling
                    else:
                        overrides["polling_interval"] = polling
                if soft is not None:
                    overrides["soft_mode"] = soft
                effective_config = effective_config.replace(**overrides)

            return LocatorExpect(
                driver=target,
                by=by,
                value=value,
                config=effective_config,
                message=message,
            )

        if target is None:
            raise TypeError("expect() does not support None as target")

        type_name = _resolve_target_type(target)
        cls = ASSERTION_REGISTRY.get(type_name)
        if cls is None:
            raise TypeError(f"expect() does not support target type '{type_name}'")

        assertion_cls = cast(type[AssertionMixin], cls)

        effective_config = config if config is not None else get_config()

        if timeout is not None or polling is not None or soft is not None:
            cfg_overrides: dict[str, Any] = {}
            if timeout is not None:
                cfg_overrides["timeout"] = normalize_timeout(timeout)
            if polling is not None:
                if isinstance(polling, list):
                    cfg_overrides["polling_intervals"] = polling
                else:
                    cfg_overrides["polling_interval"] = polling
            if soft is not None:
                cfg_overrides["soft_mode"] = soft
            effective_config = effective_config.replace(**cfg_overrides)

        return assertion_cls(target=target, config=effective_config, message=message)

    def poll(
        self,
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

    def configure(self, **defaults: Any) -> Callable[..., AssertionMixin]:
        """Create a pre-configured expect variant.

        Returns a callable that behaves like ``expect()`` with *defaults*
        pre-applied. Explicit kwargs from the caller override the defaults.

        Usage::

            fast_expect = expect.configure(timeout=1.0, polling=0.1)
            fast_expect(el).to_be_visible()
        """

        def _configured_expect(
            target: Any,
            /,
            **overrides: Any,
        ) -> AssertionMixin:
            merged: dict[str, Any] = {**defaults, **overrides}
            return self(target, **merged)

        return _configured_expect


expect = Expect()
