# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-10-07

### Added

- `to_have_texts_match(patterns)` and `to_have_values_contains(values)` list assertions
- Assertion methods now return `self`, enabling fluent chaining (`expect(el).to_be_visible().to_be_enabled()`)
- `expect.configure()` variants expose `.poll`
- `extend()` validates matcher names (must be a public identifier)

### Changed

- `to_be_in_frame()` takes no arguments and asserts the driver is currently inside a frame (no context switch side effects)
- `to_be_in_default_content()` performs a real check instead of always passing
- `ExpectConfig.polling_intervals` is normalized to an immutable tuple
- `normalize_timeout()` treats any value >= 1000 as milliseconds (floats included); scalar `polling` is normalized the same way
- `expect()` accepts tuples as list targets
- Screenshot capture works for `Alert` and element-list targets
- Locator assertion failures preserve the inner assertion's error message
- `pytest` runs unit tests by default; use `pytest -m integration` for browser tests
- Integration tests run against a local HTTP server (no external network dependency)
- `SoftAssertionCollector` stores failures per thread/async context (`ContextVar`), so parallel tests are isolated
- Release workflow verifies the tag matches `pyproject.toml` version (and `__version__`) before building

### Fixed

- `LocatorExpect.to_satisfy_all/any/none` passed the WebDriver instead of the re-found element to conditions
- `to_have_frame_available` and `to_have_frame_text` now restore the previous frame context (`parent_frame`) instead of always jumping to top-level content
- `to_be_visible`, `to_be_enabled`, `to_be_checked`, and `to_be_selected` no longer query the element twice per poll
- `test_smoke.py::test_version` expected version `0.1.0`
- Documentation: fluent chaining, soft assertions, `expect.configure()`, custom matcher, iframe, select, JS, and API-reference examples now match the real API; broken comparison tables fixed

## [1.0.0] - 2026-08-27

### Added

- Project skeleton with CI, linting, and build infrastructure
- Regression tests for all bug fixes listed below
- `CONTRIBUTING.md` with development setup, testing guidelines, and architecture overview
- `SECURITY.md` with vulnerability reporting policy
- `CODE_OF_CONDUCT.md` based on Contributor Covenant 2.1
- GitHub issue templates for bug reports and feature requests
- Automated release workflow (`.github/workflows/release.yml`) with PyPI trusted publishing and GitHub Releases
- `expect.configure()` example and Features section to README
- Ruff badge to README header
- Comprehensive MkDocs documentation with Material theme
- Auto-retry polling with configurable timeout and backoff schedules
- Fluent assertion API for `WebElement`, `WebDriver`, `list[WebElement]`, `Alert`, `Select`, `ShadowRoot`, iframes, cookies, JavaScript, and windows
- Locator-based expect to avoid `StaleElementReferenceException`
- Soft assertions with `SoftAssertionCollector` and `assert_all()`
- Custom matchers via `@extend` decorator and `merge_expects()`
- `expect.poll()` for retry-based assertions on arbitrary functions
- `ExpectConfig` dataclass for global and per-assertion configuration
- Screenshot capture on assertion failure
- Debug mode with per-poll logging
- Descriptive error messages with timelines and actual vs expected values
- Composition assertions: `to_satisfy_all`, `to_satisfy_any`, `to_satisfy_none`
- Negation via `.not_` on all assertions

### Fixed

- **`_retry.py`**: Empty `polling_intervals` list caused `IndexError` on first poll
- **`_retry.py`**: `timeout=0` skipped the first poll, never evaluating the condition
- **`_config.py`**: `ExpectConfig` did not validate empty `polling_intervals` lists
- **`_config.py`**: `set_default_timeout()` did not normalize milliseconds (int >= 1000 treated as seconds instead of ms)
- **`_poll.py`**: `PollAssertion.to_contain()` crashed on falsy non-string values (`0`, `False`, `[]`)
- **`_poll.py`**: `PollAssertion` did not normalize timeout consistently with `expect()`
- **`_poll.py`**: Missing validation for empty per-assertion `polling` lists
- **`_expect.py`**: `expect(timeout=5000)` stored 5000 seconds instead of 5 seconds (timeout not normalized before config overrides)
- **`_locator.py`**: `LocatorExpect.__getattr__` did not fall back to `CustomMatcherRegistry`, breaking custom matchers on locator-based assertions
- **`list.py`**: `to_have_texts_contains` and `to_have_texts_containing` crashed on `None` element text
- **`js.py`**: `to_have_js_result_contains` crashed on falsy non-string values (`0`, `False`, `[]`)
- **`js.py`**: JavaScript injection vulnerability in `localStorage`, `sessionStorage`, and `to_have_js_variable` methods (f-string interpolation replaced with `arguments[0]` parameter passing)
- **`driver.py`**: `to_have_capability_contains` crashed on falsy non-string capability values (`False`, `0`)
- **`element.py`**: `to_have_property_contains` crashed on falsy non-string property values (`False`, `0`)

### Changed

- **`_expect.py`**: Replaced `expect` function with monkeypatched `.poll`/`.configure` attributes with a proper `Expect` callable class — eliminates `type: ignore`, improves type safety and API discoverability
- **`_base.py`**: Replaced `os`/`os.path` with `pathlib.Path` for screenshot path handling
- **`_base.py`**: Screenshot timestamps now use timezone-aware `datetime.now(tz=UTC)` instead of naive `datetime.now()`
- **`_config.py`**: Centralized `normalize_timeout` function imported by all modules that need timeout normalization
