"""ExpectDriver — assertions for WebDriver / page-level state."""

from __future__ import annotations

import re
from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin
from selenium_expect.assertions.cookie import ExpectCookie
from selenium_expect.assertions.iframe import ExpectIframe
from selenium_expect.assertions.js import ExpectJS
from selenium_expect.assertions.window import ExpectWindow


class ExpectDriver(ExpectCookie, ExpectJS, ExpectIframe, ExpectWindow, AssertionMixin):
    """Assertions for WebDriver / page-level state.

    Inherits cookie, JS, iframe, and window assertions via multiple
    inheritance so all driver-level assertions are available via
    ``expect(driver)``.
    """

    def __init__(
        self,
        target: WebDriver,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    # --- Title ---

    def to_have_title(
        self,
        title: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.title == title."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.title
            return (actual == title, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have title {title!r}",
            expected=title,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_title_contains(
        self,
        title: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert title in driver.title."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.title
            return (title in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have title containing {title!r}",
            expected=title,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_title_matches(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, driver.title)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.title
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have title matching {pattern!r}",
            expected=pattern,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    # --- URL ---

    def to_have_url(
        self,
        url: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.current_url == url."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.current_url
            return (actual == url, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have URL {url!r}",
            expected=url,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_url_contains(
        self,
        url: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert url in driver.current_url."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.current_url
            return (url in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have URL containing {url!r}",
            expected=url,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_url_matches(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, driver.current_url)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.current_url
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have URL matching {pattern!r}",
            expected=pattern,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_url_changes(
        self,
        url: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.current_url != url (URL has changed from the given value)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.current_url
            return (actual != url, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have URL changed from {url!r}",
            expected=f"!= {url!r}",
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    # --- Ready state ---

    def to_have_ready_state(
        self,
        state: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert document.readyState == state (e.g. 'complete', 'interactive', 'loading')."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.execute_script("return document.readyState;")
            return (actual == state, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have ready state {state!r}",
            expected=state,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    # --- Windows / tabs ---

    def to_have_window_count(
        self,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.window_handles) == count."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.window_handles)
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window count {count}",
            expected=count,
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_window_count_greater_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.window_handles) > n."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.window_handles)
            return (actual > n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window count > {n}",
            expected=f">{n}",
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_window_count_less_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.window_handles) < n."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.window_handles)
            return (actual < n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window count < {n}",
            expected=f"<{n}",
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_window_handle(
        self,
        handle: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.current_window_handle == handle."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.current_window_handle
            return (actual == handle, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window handle {handle!r}",
            expected=handle,
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_new_window_opened(
        self,
        previous_handles: list[str],
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert that a new window has opened (current handles > previous handles)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            current = driver.window_handles
            new_handles = [h for h in current if h not in previous_handles]
            return (len(new_handles) > 0, new_handles)

        self._run_assertion(
            condition=condition,
            condition_name="to have new window opened",
            expected="new handle",
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    # --- Browser / capabilities ---

    def to_have_browser_name(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.name == name."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.name
            return (actual == name, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have browser name {name!r}",
            expected=name,
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_orientation(
        self,
        orientation: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.orientation == orientation."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.orientation
            return (actual == orientation, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have orientation {orientation!r}",
            expected=orientation,
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_capability(
        self,
        key: str,
        value: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.capabilities[key] == value."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            caps = driver.capabilities
            actual = caps.get(key) if caps else None
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have capability {key!r}={value!r}",
            expected=value,
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_capability_contains(
        self,
        key: str,
        value: Any,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in driver.capabilities[key]."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            caps = driver.capabilities
            actual = caps.get(key) if caps else None
            if actual is None:
                return (False, actual)
            return (value in str(actual), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have capability {key!r} containing {value!r}",
            expected=value,
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    # --- Page source ---

    def to_have_page_source_contains(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert text in driver.page_source."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.page_source
            return (text in (actual or ""), len(actual) if actual else 0)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have page source containing {text!r}",
            expected=text,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_page_source_matches(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, driver.page_source)."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.page_source
            return (re.search(pattern, actual or "") is not None, len(actual) if actual else 0)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have page source matching {pattern!r}",
            expected=pattern,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_page_source_not_contains(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert text not in driver.page_source."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.page_source
            return (text not in (actual or ""), len(actual) if actual else 0)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have page source not containing {text!r}",
            expected=f"not {text!r}",
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    # --- Window position / size / rect ---

    def to_have_window_position(
        self,
        x: int,
        y: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_window_position() == {'x': x, 'y': y}."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            pos = driver.get_window_position()
            actual = {"x": pos["x"], "y": pos["y"]}
            return (actual == {"x": x, "y": y}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window position ({x}, {y})",
            expected={"x": x, "y": y},
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_window_size(
        self,
        width: int,
        height: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_window_size() == {'width': width, 'height': height}."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            sz = driver.get_window_size()
            actual = {"width": sz["width"], "height": sz["height"]}
            return (actual == {"width": width, "height": height}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window size ({width}x{height})",
            expected={"width": width, "height": height},
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    def to_have_window_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_window_rect() matches all four values."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            rect = driver.get_window_rect()
            actual = {
                "x": rect["x"],
                "y": rect["y"],
                "width": rect["width"],
                "height": rect["height"],
            }
            expected = {"x": x, "y": y, "width": width, "height": height}
            return (actual == expected, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have window rect ({x}, {y}, {width}x{height})",
            expected={"x": x, "y": y, "width": width, "height": height},
            entity="browser",
            timeout=timeout,
            polling=polling,
        )

    # --- Active element ---

    def to_have_active_element_tag(
        self,
        tag: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.switch_to.active_element.tag_name == tag."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.switch_to.active_element.tag_name
            return (actual == tag, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have active element tag {tag!r}",
            expected=tag,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_active_element_id(
        self,
        id: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.switch_to.active_element.get_attribute('id') == id."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.switch_to.active_element.get_attribute("id")
            return (actual == id, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have active element id {id!r}",
            expected=id,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    def to_have_active_element_class(
        self,
        class_name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert class_name in active_element.get_attribute('class')."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = driver.switch_to.active_element.get_attribute("class")
            classes = (actual or "").split()
            return (class_name in classes, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have active element class {class_name!r}",
            expected=class_name,
            entity="page",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "WebDriver"

    def _get_element_html(self) -> str | None:
        return None


register("WebDriver", ExpectDriver)
