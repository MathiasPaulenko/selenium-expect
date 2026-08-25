"""ExpectElement — assertions for WebElement state, text, and more."""

from __future__ import annotations

import re
from typing import Any

from selenium.webdriver.remote.webelement import WebElement

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions import register
from selenium_expect.assertions._base import AssertionMixin


class ExpectElement(AssertionMixin):
    """Assertions for WebElement state, text, attributes, CSS, identity, position."""

    def __init__(
        self,
        target: WebElement,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    # --- State ---

    def to_be_visible(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_displayed() == True."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_displayed(), el.is_displayed())

        self._run_assertion(
            condition=condition,
            condition_name="to be visible",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_hidden(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_displayed() == False."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            displayed = el.is_displayed()
            return (not displayed, displayed)

        self._run_assertion(
            condition=condition,
            condition_name="to be hidden",
            expected=False,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_enabled(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_enabled() == True."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_enabled(), el.is_enabled())

        self._run_assertion(
            condition=condition,
            condition_name="to be enabled",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_disabled(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_enabled() == False."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            enabled = el.is_enabled()
            return (not enabled, enabled)

        self._run_assertion(
            condition=condition,
            condition_name="to be disabled",
            expected=False,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_checked(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_selected() == True (checkbox/radio)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_selected(), el.is_selected())

        self._run_assertion(
            condition=condition,
            condition_name="to be checked",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_selected(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_selected() == True (option/checkbox/radio)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            return (el.is_selected(), el.is_selected())

        self._run_assertion(
            condition=condition,
            condition_name="to be selected",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_present(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element exists in DOM (element.tag_name doesn't raise)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            try:
                tag = el.tag_name
                return (True, tag)
            except Exception as exc:
                return (False, str(exc))

        self._run_assertion(
            condition=condition,
            condition_name="to be present",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_absent(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element doesn't exist (raises StaleElementReferenceException
        or NoSuchElementException)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el.tag_name  # noqa: B018
                return (False, "present")
            except Exception:
                return (True, "absent")

        self._run_assertion(
            condition=condition,
            condition_name="to be absent",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_clickable(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.is_displayed() and element.is_enabled()."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            displayed = el.is_displayed()
            enabled = el.is_enabled()
            clickable = displayed and enabled
            return (clickable, {"displayed": displayed, "enabled": enabled})

        self._run_assertion(
            condition=condition,
            condition_name="to be clickable",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_be_stale(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element is stale (any access raises StaleElementReferenceException)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            try:
                el.tag_name  # noqa: B018
                return (False, "not stale")
            except Exception:
                return (True, "stale")

        self._run_assertion(
            condition=condition,
            condition_name="to be stale",
            expected=True,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Text ---

    def to_have_text(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text == text."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (actual == text, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text {text!r}",
            expected=text,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_contains(
        self,
        text: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert text in element.text."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (text in actual, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text containing {text!r}",
            expected=text,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_matches(
        self,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, element.text)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (re.search(pattern, actual) is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have text matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text == ''."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (actual == "", actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have text empty",
            expected="",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_text_not_empty(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.text != ''."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.text
            return (actual != "", actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have text not empty",
            expected="non-empty",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_value(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute('value') == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("value")
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_value_contains(
        self,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.get_attribute('value')."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("value")
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have value containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Attributes ---

    def to_have_attribute(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.get_attribute(name)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_matches(
        self,
        name: str,
        pattern: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert re.search(pattern, element.get_attribute(name))."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (re.search(pattern, actual or "") is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} matching {pattern!r}",
            expected=pattern,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_empty(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) == '' or None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual is None or actual == "", actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} empty",
            expected="empty or None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_present(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) is not None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} present",
            expected="present",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_attribute_absent(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute(name) is None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute(name)
            return (actual is None, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have attribute {name!r} absent",
            expected="absent",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- CSS properties ---

    def to_have_css_property(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.value_of_css_property(name) == value."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.value_of_css_property(name)
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have CSS {name!r}={value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_css_property_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in element.value_of_css_property(name)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.value_of_css_property(name)
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have CSS {name!r} containing {value!r}",
            expected=value,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Identity / DOM ---

    def to_have_tag(
        self,
        tag: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.tag_name == tag."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.tag_name
            return (actual == tag, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have tag {tag!r}",
            expected=tag,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_id(
        self,
        id: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.get_attribute('id') == id."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("id")
            return (actual == id, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have id {id!r}",
            expected=id,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_class(
        self,
        class_name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert class_name in element.get_attribute('class').split()."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            classes = (actual or "").split()
            return (class_name in classes, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have class {class_name!r}",
            expected=class_name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_class_contains(
        self,
        class_name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert class_name in element.get_attribute('class') (substring)."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.get_attribute("class")
            return (class_name in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have class containing {class_name!r}",
            expected=class_name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Position / dimensions ---

    def to_have_location(
        self,
        x: int,
        y: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location == {'x': x, 'y': y}."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            loc = el.location
            actual = {"x": loc["x"], "y": loc["y"]}
            return (actual == {"x": x, "y": y}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location ({x}, {y})",
            expected={"x": x, "y": y},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_x(
        self,
        x: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location['x'] == x."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.location["x"]
            return (actual == x, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location x={x}",
            expected=x,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_location_y(
        self,
        y: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.location['y'] == y."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.location["y"]
            return (actual == y, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have location y={y}",
            expected=y,
            entity=self._entity_description(),
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
        """Assert element.size == {'width': width, 'height': height}."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            sz = el.size
            actual = {"width": sz["width"], "height": sz["height"]}
            return (actual == {"width": width, "height": height}, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size ({width}x{height})",
            expected={"width": width, "height": height},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size_width(
        self,
        width: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size['width'] == width."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.size["width"]
            return (actual == width, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size width={width}",
            expected=width,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_size_height(
        self,
        height: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.size['height'] == height."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.size["height"]
            return (actual == height, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have size height={height}",
            expected=height,
            entity=self._entity_description(),
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
        """Assert element.rect matches all four values."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            rect = el.rect
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
            condition_name=f"to have rect ({x}, {y}, {width}x{height})",
            expected={"x": x, "y": y, "width": width, "height": height},
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Accessibility (Selenium 4+) ---

    def to_have_aria_role(
        self,
        role: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.aria_role == role."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.aria_role
            return (actual == role, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have aria role {role!r}",
            expected=role,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_aria_role_contains(
        self,
        role: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert role in element.aria_role."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.aria_role
            return (role in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have aria role containing {role!r}",
            expected=role,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_accessible_name(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.accessible_name == name."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.accessible_name
            return (actual == name, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have accessible name {name!r}",
            expected=name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_accessible_name_contains(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert name in element.accessible_name."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.accessible_name
            return (name in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have accessible name containing {name!r}",
            expected=name,
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Shadow DOM ---

    def to_have_shadow_root(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.shadow_root is not None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.shadow_root
            return (actual is not None, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have shadow root",
            expected="not None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    def to_have_shadow_root_absent(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert element.shadow_root is None."""
        el = self._target

        def condition() -> tuple[bool, Any]:
            actual = el.shadow_root
            return (actual is None, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have shadow root absent",
            expected="None",
            entity=self._entity_description(),
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        el = self._target
        try:
            tag = el.tag_name
            elem_id = el.get_attribute("id")
            if elem_id:
                return f"<{tag} id={elem_id!r}>"
            return f"<{tag}>"
        except Exception:
            return repr(el)

    def _get_element_html(self) -> str | None:
        el = self._target
        try:
            html = el.get_attribute("outerHTML")
            return html if html else None
        except Exception:
            return None


register("WebElement", ExpectElement)
