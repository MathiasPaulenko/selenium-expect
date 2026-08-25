"""ExpectWindow — assertions for window position, size, and rect."""

from __future__ import annotations

from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions._base import AssertionMixin


class ExpectWindow(AssertionMixin):
    """Assertions for window position, size, and rect (driver-level).

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

    def to_have_position(
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
            entity="window",
            timeout=timeout,
            polling=polling,
        )

    def to_have_size(
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
            entity="window",
            timeout=timeout,
            polling=polling,
        )

    def to_have_rect(
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
            entity="window",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "window"

    def _get_element_html(self) -> str | None:
        return None
