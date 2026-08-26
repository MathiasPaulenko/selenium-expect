"""ExpectCookie — assertions for browser cookies."""

from __future__ import annotations

from typing import Any

from selenium.webdriver.remote.webdriver import WebDriver

from selenium_expect._config import ExpectConfig
from selenium_expect.assertions._base import AssertionMixin


class ExpectCookie(AssertionMixin):
    """Assertions for browser cookies.

    Initialized with a ``WebDriver`` — uses ``driver.get_cookie()`` and
    ``driver.get_cookies()`` to inspect cookies.  Not dispatched via
    ``expect()`` (which maps ``WebDriver`` to ``ExpectDriver``); instantiate
    directly or via a helper.
    """

    def __init__(
        self,
        target: WebDriver,
        config: ExpectConfig | None = None,
        message: str | None = None,
        negate: bool = False,
    ) -> None:
        super().__init__(target=target, config=config, message=message, negate=negate)

    # --- Cookie presence ---

    def to_have_cookie(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name) is not None."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            return (cookie is not None, cookie)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r}",
            expected=name,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_value(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['value'] == value."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("value") if cookie else None
            return (actual == value, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} value {value!r}",
            expected=value,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_value_contains(
        self,
        name: str,
        value: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert value in driver.get_cookie(name)['value']."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("value") if cookie else None
            return (value in (actual or ""), actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} value containing {value!r}",
            expected=value,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_domain(
        self,
        name: str,
        domain: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['domain'] == domain."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("domain") if cookie else None
            return (actual == domain, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} domain {domain!r}",
            expected=domain,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_path(
        self,
        name: str,
        path: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['path'] == path."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("path") if cookie else None
            return (actual == path, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} path {path!r}",
            expected=path,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_http_only(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['httpOnly'] == True."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("httpOnly") if cookie else None
            return (actual is True, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} httpOnly=True",
            expected=True,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_secure(
        self,
        name: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['secure'] == True."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("secure") if cookie else None
            return (actual is True, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} secure=True",
            expected=True,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_same_site(
        self,
        name: str,
        same_site: str,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['sameSite'] == same_site."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            actual = cookie.get("sameSite") if cookie else None
            return (actual == same_site, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} sameSite={same_site!r}",
            expected=same_site,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_count(
        self,
        count: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.get_cookies()) == count."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.get_cookies())
            return (actual == count, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie count {count}",
            expected=count,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_count_greater_than(
        self,
        n: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.get_cookies()) > n."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.get_cookies())
            return (actual > n, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie count > {n}",
            expected=f">{n}",
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_cookie_expiry(
        self,
        name: str,
        expiry: int,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert driver.get_cookie(name)['expiry'] == expiry."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            cookie = driver.get_cookie(name)
            if cookie is None:
                return (False, "cookie not found")
            actual = cookie.get("expiry")
            return (actual == expiry, actual)

        self._run_assertion(
            condition=condition,
            condition_name=f"to have cookie {name!r} expiry {expiry}",
            expected=expiry,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    def to_have_no_cookies(
        self,
        *,
        timeout: float | None = None,
        polling: float | list[float] | None = None,
    ) -> None:
        """Assert len(driver.get_cookies()) == 0."""
        driver = self._target

        def condition() -> tuple[bool, Any]:
            actual = len(driver.get_cookies())
            return (actual == 0, actual)

        self._run_assertion(
            condition=condition,
            condition_name="to have no cookies",
            expected=0,
            entity="cookies",
            timeout=timeout,
            polling=polling,
        )

    # --- Overrides ---

    def _entity_description(self) -> str:
        return "cookies"

    def _get_element_html(self) -> str | None:
        return None
