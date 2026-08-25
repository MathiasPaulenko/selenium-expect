"""Unit tests for selenium_expect._config."""

from __future__ import annotations

import pytest

from selenium_expect._config import (
    ExpectConfig,
    get_config,
    set_debug_mode,
    set_default_polling_interval,
    set_default_polling_intervals,
    set_default_timeout,
    set_screenshot_on_failure,
)


class TestExpectConfigDefaults:
    def test_defaults(self) -> None:
        config = ExpectConfig()
        assert config.timeout == 5.0
        assert config.polling_interval == 0.5
        assert config.polling_intervals is None
        assert config.screenshot_on_failure is False
        assert config.screenshot_path is None
        assert config.debug_mode is False
        assert config.soft_mode is False

    def test_frozen(self) -> None:
        config = ExpectConfig()
        with pytest.raises((AttributeError, Exception)):
            config.timeout = 10.0  # type: ignore[misc]

    def test_replace_creates_new_instance(self) -> None:
        config = ExpectConfig()
        new = config.replace(timeout=10.0)
        assert new is not config
        assert config.timeout == 5.0
        assert new.timeout == 10.0

    def test_replace_multiple_fields(self) -> None:
        config = ExpectConfig()
        new = config.replace(timeout=10.0, polling_interval=1.0)
        assert new.timeout == 10.0
        assert new.polling_interval == 1.0
        assert config.timeout == 5.0
        assert config.polling_interval == 0.5


class TestExpectConfigValidation:
    def test_negative_timeout_raises(self) -> None:
        with pytest.raises(ValueError, match="timeout"):
            ExpectConfig(timeout=-1.0)

    def test_negative_polling_interval_raises(self) -> None:
        with pytest.raises(ValueError, match="polling_interval"):
            ExpectConfig(polling_interval=-0.5)

    def test_negative_polling_interval_in_list_raises(self) -> None:
        with pytest.raises(ValueError, match="polling_intervals"):
            ExpectConfig(polling_intervals=[0.1, -0.5, 1.0])

    def test_zero_timeout_allowed(self) -> None:
        config = ExpectConfig(timeout=0.0)
        assert config.timeout == 0.0

    def test_zero_polling_interval_allowed(self) -> None:
        config = ExpectConfig(polling_interval=0.0)
        assert config.polling_interval == 0.0


class TestGlobalConfigSetters:
    def test_set_default_timeout(self) -> None:
        set_default_timeout(10.0)
        assert get_config().timeout == 10.0

    def test_set_default_polling_interval(self) -> None:
        set_default_polling_interval(1.0)
        assert get_config().polling_interval == 1.0

    def test_set_default_polling_intervals(self) -> None:
        set_default_polling_intervals([0.1, 0.5, 1.0])
        assert get_config().polling_intervals == [0.1, 0.5, 1.0]

    def test_set_screenshot_on_failure(self) -> None:
        set_screenshot_on_failure(True)
        config = get_config()
        assert config.screenshot_on_failure is True
        assert config.screenshot_path == "./screenshots/"

    def test_set_screenshot_on_failure_with_path(self) -> None:
        set_screenshot_on_failure(True, "/tmp/shots")
        config = get_config()
        assert config.screenshot_on_failure is True
        assert config.screenshot_path == "/tmp/shots"

    def test_set_debug_mode(self) -> None:
        set_debug_mode(True)
        assert get_config().debug_mode is True

    def test_get_config_returns_current(self) -> None:
        set_default_timeout(42.0)
        assert get_config().timeout == 42.0

    def test_config_resets_between_tests(self) -> None:
        """autouse fixture resets config — verify isolation."""
        assert get_config().timeout == 5.0
        assert get_config().polling_interval == 0.5
        assert get_config().debug_mode is False
