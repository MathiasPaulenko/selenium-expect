# Contributing to selenium-expect

Thank you for your interest in contributing! This document covers the
essential setup and workflow for contributors.

## Development setup

```bash
git clone https://github.com/MathiasPaulenko/selenium-expect.git
cd selenium-expect
pip install -e ".[dev]"
pre-commit install
```

## Daily workflow

```bash
make check      # lint + format check + type check + tests
make lint-fix   # auto-fix lint issues
make format     # format code
make test       # run unit tests
make test-cov   # run tests with coverage report
```

## Code quality gates

All contributions must pass:

- **ruff** — linting and formatting (`ruff check` + `ruff format --check`)
- **mypy --strict** — type checking with no `Any` leakage
- **pytest** — unit tests with >= 90% coverage
- **pre-commit hooks** — trailing whitespace, YAML/TOML validation, etc.

Run `make check` before pushing to catch issues early.

## Testing guidelines

- **Unit tests** (`tests/unit/`) — fast, no browser required. Mock all
  Selenium objects. Every bug fix must include a regression test.
- **Integration tests** (`tests/integration/`) — require a real browser
  (Chrome or Firefox). Run with `pytest -m integration`.

### Test conventions

- Use `pytest` fixtures for shared setup (see `tests/conftest.py`).
- Mock drivers and elements via `unittest.mock.MagicMock`.
- Name regression tests descriptively: `test_<scenario>_<expected_behavior>`.
- Place regression tests in `tests/unit/test_regression_fixes.py`.

## Pull request process

1. Create a feature branch from `main`.
2. Write tests for your change.
3. Ensure `make check` passes.
4. Update `CHANGELOG.md` under `## [Unreleased]`.
5. Open a PR with a clear description linking to any relevant issues.

## Architecture overview

```text
selenium_expect/
├── __init__.py          # Public API exports
├── _expect.py           # Expect callable class — main dispatcher
├── _config.py           # ExpectConfig (immutable, frozen dataclass)
├── _retry.py            # retry_until() — agnostic retry loop
├── _poll.py             # PollAssertion — expect.poll()
├── _locator.py          # LocatorExpect — re-finds element each poll
├── _soft.py             # SoftAssertionCollector
├── _matcher.py          # Custom matcher registry (@extend)
├── _compose.py          # to_satisfy_all/any/none
├── _errors.py           # AssertionFormatter
└── assertions/
    ├── _base.py         # AssertionMixin — _run_assertion()
    ├── alert.py         # Alert assertions
    ├── cookie.py        # Cookie assertions
    ├── driver.py        # WebDriver assertions
    ├── element.py       # WebElement assertions
    ├── iframe.py        # iframe assertions
    ├── js.py            # JavaScript / storage assertions
    ├── list.py          # List[WebElement] assertions
    ├── select.py        # Select dropdown assertions
    ├── shadow.py        # Shadow DOM assertions
    └── window.py        # Window assertions
```

Key design principles:

- **Single retry path**: All assertions go through `_run_assertion()` in
  `_base.py`, which calls `retry_until()` in `_retry.py`.
- **Immutable config**: `ExpectConfig` is frozen. Use `.replace()` for
  per-assertion overrides.
- **Negation via flag**: `not_` property sets `_negate` — no duplicated
  methods.
- **Registry pattern**: `ASSERTION_REGISTRY` maps type names to assertion
  classes. `expect()` dispatches based on target type.

## Release process

1. Update `CHANGELOG.md` with dated version header.
2. Update `__version__` in `selenium_expect/__init__.py`.
3. Update `version` in `pyproject.toml`.
4. Commit and tag: `git tag v0.x.y`.
5. Push the tag: `git push origin v0.x.y`.
6. CI automatically builds, publishes to PyPI (via trusted publishing), and creates a GitHub Release.

## License

MIT — see [LICENSE](LICENSE).
