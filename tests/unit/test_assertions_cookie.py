"""Unit tests for selenium_expect.assertions.cookie.ExpectCookie."""

from __future__ import annotations

from typing import Any

import pytest

from selenium_expect.assertions.cookie import ExpectCookie


class TestExpectCookie:
    def test_to_have_cookie(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie('session') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie("session")

    def test_to_have_cookie_value(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_value('session', 'abc123') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_value("session", "abc123")

    def test_to_have_cookie_value_contains(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_value_contains('session', 'abc') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_value_contains("session", "abc")

    def test_to_have_cookie_domain(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_domain('session', '.example.com') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_domain("session", ".example.com")

    def test_to_have_cookie_path(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_path('session', '/') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_path("session", "/")

    def test_to_have_cookie_http_only(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_http_only('session') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_http_only("session")

    def test_to_have_cookie_secure(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_secure('session') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_secure("session")

    def test_to_have_cookie_same_site(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_same_site('session', 'Lax') passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_same_site("session", "Lax")

    def test_to_have_cookie_count(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_count(2) passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_count(2)

    def test_to_have_cookie_count_greater_than(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_count_greater_than(1) passes."""
        ExpectCookie(mock_driver_with_cookies).to_have_cookie_count_greater_than(1)

    def test_to_have_no_cookies(self, mock_driver: Any) -> None:
        """ExpectCookie(driver).to_have_no_cookies() passes when no cookies."""
        mock_driver.get_cookies.return_value = []
        ExpectCookie(mock_driver).to_have_no_cookies()

    def test_to_have_cookie_not_found(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie('missing') raises."""
        with pytest.raises(AssertionError, match="to have cookie"):
            ExpectCookie(mock_driver_with_cookies).to_have_cookie("missing")

    def test_to_have_cookie_value_fails(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_value('session', 'wrong') raises."""
        with pytest.raises(AssertionError, match="to have cookie"):
            ExpectCookie(mock_driver_with_cookies).to_have_cookie_value("session", "wrong")

    def test_to_have_cookie_count_fails(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_count(5) raises."""
        with pytest.raises(AssertionError, match="to have cookie count"):
            ExpectCookie(mock_driver_with_cookies).to_have_cookie_count(5)

    def test_to_have_cookie_http_only_fails(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_http_only('theme') raises (httpOnly=False)."""
        with pytest.raises(AssertionError, match="httpOnly"):
            ExpectCookie(mock_driver_with_cookies).to_have_cookie_http_only("theme")

    def test_to_have_cookie_secure_fails(self, mock_driver_with_cookies: Any) -> None:
        """ExpectCookie(driver).to_have_cookie_secure('theme') raises (secure=False)."""
        with pytest.raises(AssertionError, match="secure"):
            ExpectCookie(mock_driver_with_cookies).to_have_cookie_secure("theme")
