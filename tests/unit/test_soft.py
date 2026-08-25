"""Unit tests for selenium_expect._soft.SoftAssertionCollector."""

from __future__ import annotations

import pytest

from selenium_expect import SoftAssertionCollector, assert_all, expect
from selenium_expect._config import ExpectConfig


@pytest.fixture(autouse=True)
def _reset_collector() -> None:
    """Reset the collector before and after each test."""
    SoftAssertionCollector.reset()
    yield
    SoftAssertionCollector.reset()


class TestSoftAssertionCollector:
    def test_add_failure(self) -> None:
        """add_failure stores a failure message."""
        SoftAssertionCollector.add_failure("error 1")
        assert SoftAssertionCollector.get_failures() == ["error 1"]

    def test_add_multiple_failures(self) -> None:
        """add_failure stores multiple failures in order."""
        SoftAssertionCollector.add_failure("error 1")
        SoftAssertionCollector.add_failure("error 2")
        assert SoftAssertionCollector.get_failures() == ["error 1", "error 2"]

    def test_reset(self) -> None:
        """reset clears all failures."""
        SoftAssertionCollector.add_failure("error 1")
        SoftAssertionCollector.reset()
        assert SoftAssertionCollector.get_failures() == []

    def test_assert_all_no_failures(self) -> None:
        """assert_all does nothing when no failures collected."""
        assert_all()  # should not raise

    def test_assert_all_with_failures(self) -> None:
        """assert_all raises with combined message and resets."""
        SoftAssertionCollector.add_failure("error 1")
        SoftAssertionCollector.add_failure("error 2")
        with pytest.raises(AssertionError, match="Soft assertion failures"):
            assert_all()
        # Should be reset after raising
        assert SoftAssertionCollector.get_failures() == []

    def test_assert_all_resets_after_raise(self) -> None:
        """assert_all resets even after raising."""
        SoftAssertionCollector.add_failure("error")
        with pytest.raises(AssertionError):
            assert_all()
        assert SoftAssertionCollector.get_failures() == []


class TestSoftAssertionsIntegration:
    def test_soft_mode_collects_failures(self, mock_element: object) -> None:
        """expect(el, soft=True).to_have_text('wrong') collects instead of raising."""
        expect(mock_element, soft=True).to_have_text("wrong text")
        failures = SoftAssertionCollector.get_failures()
        assert len(failures) == 1
        assert "to have text" in failures[0]

    def test_soft_mode_multiple_failures(self, mock_element: object) -> None:
        """Multiple soft failures are all collected."""
        expect(mock_element, soft=True).to_have_text("wrong 1")
        expect(mock_element, soft=True).to_have_text("wrong 2")
        failures = SoftAssertionCollector.get_failures()
        assert len(failures) == 2

    def test_soft_mode_passes_no_failure(self, mock_element: object) -> None:
        """Passing soft assertion doesn't add a failure."""
        expect(mock_element, soft=True).to_be_visible()
        assert SoftAssertionCollector.get_failures() == []

    def test_soft_mode_assert_all_raises(self, mock_element: object) -> None:
        """assert_all raises after soft failures."""
        expect(mock_element, soft=True).to_have_text("wrong")
        with pytest.raises(AssertionError, match="Soft assertion failures"):
            assert_all()

    def test_soft_mode_config(self, mock_element: object) -> None:
        """soft_mode via ExpectConfig works."""
        config = ExpectConfig(soft_mode=True)
        expect(mock_element, config=config).to_have_text("wrong")
        assert len(SoftAssertionCollector.get_failures()) == 1

    def test_non_soft_mode_raises_immediately(self, mock_element: object) -> None:
        """Without soft mode, assertion raises immediately."""
        with pytest.raises(AssertionError, match="to have text"):
            expect(mock_element).to_have_text("wrong text")
        assert SoftAssertionCollector.get_failures() == []
