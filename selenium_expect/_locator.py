"""LocatorExpect — re-finds element on each poll cycle.

When ``expect(driver, by=By.ID, value="foo")`` is used, a ``LocatorExpect``
is returned instead of ``ExpectElement``. On every poll cycle it calls
``driver.find_element(by, value)`` to get a fresh element, then delegates
the condition check to the corresponding ``ExpectElement`` method.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Self

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions._base import AssertionMixin


class LocatorExpect(AssertionMixin):
    """Locator-based expect that re-finds the element on each poll.

    Delegates all ``ExpectElement`` assertion methods via ``__getattr__``.
    Each assertion method is executed with a fresh element obtained from
    ``driver.find_element(by, value)`` on every poll cycle.
    """

    def __init__(
        self,
        driver: WebDriver,
        by: str,
        value: str,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=driver, config=config, message=message, negate=negate)
        self._driver = driver
        self._by = by
        self._value = value

    def _find_element(self) -> Any:
        """Find the element fresh. Returns None if not found."""
        try:
            return self._driver.find_element(self._by, self._value)
        except NoSuchElementException:
            return None

    @property
    def not_(self) -> LocatorExpect:
        """Return a negated copy."""
        return LocatorExpect(
            driver=self._driver,
            by=self._by,
            value=self._value,
            config=self._config,
            message=self._message,
            negate=not self._negate,
        )

    def to_satisfy_all(self, *conditions: Callable[[Any], None]) -> Self:
        """Assert all conditions pass on the re-found element (AND)."""
        from selenium_expect._compose import satisfy_all

        def condition() -> tuple[bool, Any]:
            el = self._find_element()
            if el is None:
                return (False, "element not found")
            try:
                satisfy_all(el, *conditions, message=self._message)
                return (True, "all pass")
            except AssertionError as exc:
                return (False, str(exc))

        self._run_assertion(
            condition=condition,
            condition_name="to_satisfy_all",
            expected="all pass",
            entity=self._entity_description(),
        )
        return self

    def to_satisfy_any(self, *conditions: Callable[[Any], None]) -> Self:
        """Assert at least one condition passes on the re-found element (OR)."""
        from selenium_expect._compose import satisfy_any

        def condition() -> tuple[bool, Any]:
            el = self._find_element()
            if el is None:
                return (False, "element not found")
            try:
                satisfy_any(el, *conditions, message=self._message)
                return (True, "at least one pass")
            except AssertionError as exc:
                return (False, str(exc))

        self._run_assertion(
            condition=condition,
            condition_name="to_satisfy_any",
            expected="at least one pass",
            entity=self._entity_description(),
        )
        return self

    def to_satisfy_none(self, *conditions: Callable[[Any], None]) -> Self:
        """Assert no condition passes on the re-found element (NOT)."""
        from selenium_expect._compose import satisfy_none

        def condition() -> tuple[bool, Any]:
            el = self._find_element()
            if el is None:
                return (False, "element not found")
            try:
                satisfy_none(el, *conditions, message=self._message)
                return (True, "none pass")
            except AssertionError as exc:
                return (False, str(exc))

        self._run_assertion(
            condition=condition,
            condition_name="to_satisfy_none",
            expected="none pass",
            entity=self._entity_description(),
        )
        return self

    def _entity_description(self) -> str:
        return f"locator({self._by}={self._value!r})"

    def _get_element_html(self) -> str | None:
        el = self._find_element()
        if el is None:
            return None
        try:
            html: str | None = el.get_attribute("outerHTML")
            return html
        except StaleElementReferenceException:
            return None

    def __getattr__(self, name: str) -> Any:
        """Delegate to ExpectElement methods or custom matchers with re-find on each poll.

        For each assertion method call, we wrap the condition so that
        ``find_element`` is called fresh on every retry poll.
        """
        # Avoid recursion for private/dunder attributes
        if name.startswith("_"):
            raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")

        from selenium_expect._matcher import CustomMatcherRegistry
        from selenium_expect.assertions.element import ExpectElement

        # Check for custom matcher first
        matcher_fn = CustomMatcherRegistry.get(name)

        # Get the actual method from ExpectElement
        element_method = getattr(ExpectElement, name, None)

        if matcher_fn is None and (element_method is None or not callable(element_method)):
            raise AttributeError(f"{type(self).__name__!r} object has no attribute {name!r}")

        if matcher_fn is not None:

            def _invoke_matcher(*args: Any, **kwargs: Any) -> LocatorExpect:
                timeout = kwargs.pop("timeout", None)
                polling = kwargs.pop("polling", None)

                def condition() -> tuple[bool, Any]:
                    try:
                        el = self._driver.find_element(self._by, self._value)
                    except NoSuchElementException:
                        return (False, "element not found")
                    try:
                        return matcher_fn(el, *args, **kwargs)
                    except StaleElementReferenceException:
                        return (False, "stale element")

                self._run_assertion(
                    condition=condition,
                    condition_name=name.replace("_", " "),
                    expected=None,
                    entity=self._entity_description(),
                    timeout=timeout,
                    polling=polling,
                )

                return self

            return _invoke_matcher

        def _invoke(*args: Any, **kwargs: Any) -> LocatorExpect:
            timeout = kwargs.pop("timeout", None)
            polling = kwargs.pop("polling", None)

            def condition() -> tuple[bool, Any]:
                try:
                    el = self._driver.find_element(self._by, self._value)
                except NoSuchElementException:
                    return (False, "element not found")
                inner_config = self._config.replace(soft_mode=False, screenshot_on_failure=False)
                temp = ExpectElement(
                    target=el,
                    config=inner_config,
                    message=self._message,
                    negate=False,
                )
                method = getattr(temp, name)
                try:
                    method(*args, timeout=0.001, **kwargs)
                    return (True, "passed")
                except AssertionError as exc:
                    first_line = str(exc).splitlines()[0] if str(exc) else "failed"
                    return (False, first_line)
                except StaleElementReferenceException:
                    return (False, "stale element")

            self._run_assertion(
                condition=condition,
                condition_name=name.replace("_", " "),
                expected=None,
                entity=self._entity_description(),
                timeout=timeout,
                polling=polling,
            )

            return self

        return _invoke
