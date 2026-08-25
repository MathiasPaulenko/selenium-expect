# Agent Notes for selenium-expect

## Project purpose

`selenium-expect` brings Playwright's `expect()` assertion pattern to Selenium
Python. Auto-retry assertions that don't flake, with a fluent API.

## Important implementation details

- `expect()` dispatcher in `_expect.py` resolves target type to assertion class
  via `assertions/__init__.py` registry
- `AssertionMixin` in `assertions/_base.py` provides `_run_assertion()` — all
  assertions call this single method
- `retry_until()` in `_retry.py` is agnostic — doesn't know Selenium
- `ExpectConfig` is a frozen dataclass with `.replace()` for immutable updates
- Negation is a flag (`_negate`) on the assertion instance, not duplicated methods
- `py.typed` is included in the wheel (PEP 561)

## Build and verification commands

```bash
ruff check selenium_expect/ tests/
ruff format --check selenium_expect/ tests/
mypy --strict selenium_expect
pytest --cov=selenium_expect --cov-report=term-missing
python -m build
```

## Known constraints

- `ref/` is intentionally ignored (local reference material). Do not commit it.
- Selenium 4.10+ required for `aria_role`, `accessible_name`, `shadow_root`
- Integration tests require a browser (Chrome/Firefox) — run with `-m integration`
