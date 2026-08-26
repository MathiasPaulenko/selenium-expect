# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
