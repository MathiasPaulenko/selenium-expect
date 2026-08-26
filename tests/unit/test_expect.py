"""Unit tests for selenium_expect._expect dispatcher."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from selenium.webdriver.support.ui import Select

from selenium_expect import expect
from selenium_expect._config import ExpectConfig
from selenium_expect.assertions.element import ExpectElement


class TestExpectDispatcher:
    def test_dispatches_to_element(self, mock_element: Any) -> None:
        """expect(element) returns ExpectElement instance."""
        result = expect(mock_element)
        assert isinstance(result, ExpectElement)

    def test_raises_on_unsupported_type(self) -> None:
        """expect(42) raises TypeError."""
        with pytest.raises(TypeError, match="does not support"):
            expect(42)

    def test_raises_on_none(self) -> None:
        """expect(None) raises TypeError."""
        with pytest.raises(TypeError, match="None"):
            expect(None)  # type: ignore[arg-type]

    def test_select_checked_before_element(self) -> None:
        """Select wraps WebElement — registry checks Select first.

        Select is registered, so expect(select) dispatches to ExpectSelect.
        """
        from selenium_expect.assertions.select import ExpectSelect

        select = MagicMock(spec=Select)
        result = expect(select)
        assert isinstance(result, ExpectSelect)


class TestExpectConfigOverride:
    def test_per_assertion_timeout(self, mock_element: Any) -> None:
        """expect(el, timeout=10) uses 10s instead of global default."""
        result = expect(mock_element, timeout=10.0)
        assert result._config.timeout == 10.0

    def test_per_assertion_polling(self, mock_element: Any) -> None:
        """expect(el, polling=0.1) uses 0.1s interval."""
        result = expect(mock_element, polling=0.1)
        assert result._config.polling_interval == 0.1

    def test_per_assertion_polling_intervals(self, mock_element: Any) -> None:
        """expect(el, polling=[0.05, 0.1, 0.5]) uses backoff schedule."""
        result = expect(mock_element, polling=[0.05, 0.1, 0.5])
        assert result._config.polling_intervals == [0.05, 0.1, 0.5]

    def test_per_assertion_message(self, mock_element: Any) -> None:
        """expect(el, message='custom') includes message in error."""
        result = expect(mock_element, message="custom error")
        assert result._message == "custom error"

    def test_per_assertion_soft(self, mock_element: Any) -> None:
        """expect(el, soft=True) accumulates failures instead of raising."""
        result = expect(mock_element, soft=True)
        assert result._config.soft_mode is True

    def test_per_assertion_config_object(self, mock_element: Any) -> None:
        """expect(el, config=ExpectConfig(timeout=20)) uses config."""
        config = ExpectConfig(timeout=20.0)
        result = expect(mock_element, config=config)
        assert result._config.timeout == 20.0

    def test_per_assertion_overrides_global(self, mock_element: Any) -> None:
        """Per-assertion kwargs override global config."""
        result = expect(mock_element, timeout=15.0)
        assert result._config.timeout == 15.0
        assert result._config.polling_interval == 0.5  # global default unchanged


class TestExpectConfigure:
    def test_configure_returns_callable(self) -> None:
        """expect.configure(timeout=10) returns a callable."""
        configured = expect.configure(timeout=10.0)
        assert callable(configured)

    def test_configure_applies_defaults(self, mock_element: Any) -> None:
        """expect.configure(timeout=10) pre-applies timeout as default."""
        fast_expect = expect.configure(timeout=10.0)
        result = fast_expect(mock_element)
        assert result._config.timeout == 10.0

    def test_configure_multiple_kwargs(self, mock_element: Any) -> None:
        """expect.configure(timeout=10, polling=0.1) applies both."""
        fast_expect = expect.configure(timeout=10.0, polling=0.1)
        result = fast_expect(mock_element)
        assert result._config.timeout == 10.0
        assert result._config.polling_interval == 0.1

    def test_configure_override_by_caller(self, mock_element: Any) -> None:
        """Caller kwargs override configured defaults."""
        fast_expect = expect.configure(timeout=10.0)
        result = fast_expect(mock_element, timeout=20.0)
        assert result._config.timeout == 20.0

    def test_configure_message(self, mock_element: Any) -> None:
        """expect.configure(message=...) pre-applies message."""
        configured = expect.configure(message="custom")
        result = configured(mock_element)
        assert result._message == "custom"

    def test_configure_soft(self, mock_element: Any) -> None:
        """expect.configure(soft=True) pre-applies soft mode."""
        configured = expect.configure(soft=True)
        result = configured(mock_element)
        assert result._config.soft_mode is True

    def test_configure_preserves_polling_intervals(self, mock_element: Any) -> None:
        """expect.configure(polling=[...]) pre-applies backoff schedule."""
        configured = expect.configure(polling=[0.05, 0.1, 0.2])
        result = configured(mock_element)
        assert result._config.polling_intervals == [0.05, 0.1, 0.2]

    def test_configure_no_kwargs(self, mock_element: Any) -> None:
        """expect.configure() with no kwargs behaves like expect()."""
        configured = expect.configure()
        result = configured(mock_element)
        assert result._config.timeout == result._config.timeout  # uses global default


class TestExpectLocator:
    def test_by_value_returns_locator(self, mock_driver: Any) -> None:
        """expect(driver, by='id', value='foo') returns LocatorExpect."""
        from selenium_expect._locator import LocatorExpect

        result = expect(mock_driver, by="id", value="foo")
        assert isinstance(result, LocatorExpect)

    def test_by_without_value_raises(self, mock_driver: Any) -> None:
        """expect(driver, by='id') without value raises ValueError."""
        with pytest.raises(ValueError, match="both 'by' and 'value'"):
            expect(mock_driver, by="id")  # type: ignore[call-arg]

    def test_value_without_by_raises(self, mock_driver: Any) -> None:
        """expect(driver, value='foo') without by raises ValueError."""
        with pytest.raises(ValueError, match="both 'by' and 'value'"):
            expect(mock_driver, value="foo")  # type: ignore[call-arg]

    def test_locator_tuple_returns_locator(self, mock_driver: Any) -> None:
        """expect(driver, locator=('id', 'foo')) returns LocatorExpect."""
        from selenium_expect._locator import LocatorExpect

        result = expect(mock_driver, locator=("id", "foo"))
        assert isinstance(result, LocatorExpect)

    def test_locator_with_by_raises(self, mock_driver: Any) -> None:
        """expect(driver, locator=..., by=...) raises ValueError."""
        with pytest.raises(ValueError, match="Cannot use both"):
            expect(mock_driver, locator=("id", "foo"), by="id", value="bar")
