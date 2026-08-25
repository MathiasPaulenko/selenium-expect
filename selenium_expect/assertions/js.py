"""ExpectJS — assertions for JavaScript / browser state via driver.execute_script."""

from __future__ import annotations

import re
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions._base import AssertionMixin


class ExpectJS(AssertionMixin):
    """Assertions for JavaScript / browser state via ``driver.execute_script``.

    Not dispatched via ``expect()`` (which maps ``WebDriver`` to
    ``ExpectDriver``); instantiate directly with a driver.
    """

    def __init__(
        self,
        target: WebDriver,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    # --- JS result ---

    def to_have_js_result(
        self,
        script: str,
        expected: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.execute_script(script) == expected."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(script)
            return (actual == expected, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have JS result {expected!r}",
            expected=expected,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_js_result_contains(
        self,
        script: str,
        expected: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert expected in driver.execute_script(script)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(script)
            return (expected in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have JS result containing {expected!r}",
            expected=expected,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_js_result_matches(
        self,
        script: str,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, str(driver.execute_script(script)))."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(script)
            return (re.search(pattern, str(actual)) is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have JS result matching {pattern!r}",
            expected=pattern,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_async_js_result(
        self,
        script: str,
        expected: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.execute_async_script(script) == expected."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_async_script(script)
            return (actual == expected, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have async JS result {expected!r}",
            expected=expected,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    # --- localStorage ---

    def to_have_local_storage_item(
        self,
        key: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert localStorage.getItem(key) == value via execute_script."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(f"return localStorage.getItem('{key}');")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have localStorage item {key!r}={value!r}",
            expected=value,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_local_storage_item_present(
        self,
        key: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert localStorage.getItem(key) is not None."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(f"return localStorage.getItem('{key}');")
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have localStorage item {key!r} present",
            expected="not None",
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_local_storage_item_absent(
        self,
        key: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert localStorage.getItem(key) is None."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(f"return localStorage.getItem('{key}');")
            return (actual is None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have localStorage item {key!r} absent",
            expected="None",
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_local_storage_length(
        self,
        length: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert localStorage.length == length."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script("return localStorage.length;")
            return (actual == length, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have localStorage length {length}",
            expected=length,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    # --- sessionStorage ---

    def to_have_session_storage_item(
        self,
        key: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert sessionStorage.getItem(key) == value."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(f"return sessionStorage.getItem('{key}');")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have sessionStorage item {key!r}={value!r}",
            expected=value,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_session_storage_item_present(
        self,
        key: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert sessionStorage.getItem(key) is not None."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(f"return sessionStorage.getItem('{key}');")
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have sessionStorage item {key!r} present",
            expected="not None",
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_session_storage_item_absent(
        self,
        key: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert sessionStorage.getItem(key) is None."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script(f"return sessionStorage.getItem('{key}');")
            return (actual is None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have sessionStorage item {key!r} absent",
            expected="None",
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    def to_have_session_storage_length(
        self,
        length: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert sessionStorage.length == length."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script("return sessionStorage.length;")
            return (actual == length, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have sessionStorage length {length}",
            expected=length,
            entity="js",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "JS"

    def _get_element_html(self) -> str | None:
        return None
