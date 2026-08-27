# Configuration

## Global defaults

All configuration is managed through the `ExpectConfig` dataclass and module-level setters.

### `set_default_timeout(seconds)`

Sets the default timeout for all assertions.

```python
from selenium_expect import set_default_timeout

set_default_timeout(10)  # 10 seconds
set_default_timeout(5000)  # interpreted as 5000 ms = 5 seconds
```

!!! note
    If `seconds` is an `int >= 1000`, it is interpreted as **milliseconds**. Floats and ints `< 1000` are treated as seconds.

### `set_default_polling_interval(seconds)`

Sets the default polling interval (fixed).

```python
from selenium_expect import set_default_polling_interval

set_default_polling_interval(0.25)
```

### `set_default_polling_intervals(intervals)`

Sets a backoff schedule for polling. The list is cycled through during the retry loop.

```python
from selenium_expect import set_default_polling_intervals

set_default_polling_intervals([0.1, 0.2, 0.5, 1.0])
```

### `set_screenshot_on_failure(enabled, path=None)`

Enables automatic screenshot capture on assertion failure.

```python
from selenium_expect import set_screenshot_on_failure

set_screenshot_on_failure(True, path="./screenshots/")
```

### `set_debug_mode(enabled)`

Enables debug logging for retry loops. Prints poll count, elapsed time, and actual values.

```python
from selenium_expect import set_debug_mode

set_debug_mode(True)
```

## Per-assertion overrides

Every assertion accepts `timeout` and `polling` keyword arguments that override the global defaults for that single call:

```python
expect(element).to_be_visible(timeout=2, polling=0.1)
expect(driver).to_have_title("Dashboard", timeout=10, polling=[0.1, 0.2, 0.5])
```

## `expect.configure()`

Create a pre-configured `expect` variant with baked-in defaults:

```python
from selenium_expect import expect

fast_expect = expect.configure(timeout=1.0, polling=0.1)
fast_expect(element).to_be_visible()
fast_expect(driver).to_have_title("Dashboard")
```

Explicit kwargs from the caller override the defaults:

```python
fast_expect(element).to_be_visible(timeout=5)  # uses timeout=5, polling=0.1
```

## `ExpectConfig`

The immutable `ExpectConfig` dataclass holds all settings:

| Field | Type | Default | Description |
|---|---|---|---|
| `timeout` | `float` | `5.0` | Default timeout in seconds |
| `polling_interval` | `float` | `0.5` | Fixed polling interval |
| `polling_intervals` | `list[float] \| None` | `None` | Backoff schedule |
| `screenshot_on_failure` | `bool` | `False` | Capture screenshot on failure |
| `screenshot_path` | `str \| None` | `None` | Screenshot directory |
| `debug_mode` | `bool` | `False` | Debug logging |
| `soft_mode` | `bool` | `False` | Soft assertion mode |

Use `config.replace(**kwargs)` to create a new instance with overridden fields.

## Examples

### Setting up a test suite

```python
# conftest.py
import pytest
from selenium_expect import (
    set_default_timeout,
    set_default_polling_interval,
    set_screenshot_on_failure,
    set_debug_mode,
)

def pytest_configure(config):
    # Global defaults for all tests
    set_default_timeout(10)
    set_default_polling_interval(0.25)

    # Capture screenshots on failure
    set_screenshot_on_failure(True, path="./test_screenshots/")

    # Enable debug mode in CI
    if config.getoption("--ci"):
        set_debug_mode(True)
```

### Using backoff for slow pages

```python
from selenium_expect import set_default_polling_intervals

# Poll frequently at first, then back off for slow-loading pages
set_default_polling_intervals([0.1, 0.2, 0.2, 0.5, 0.5, 1.0, 1.0])
```

### Pre-configured variants for different scenarios

```python
from selenium_expect import expect

# Fast checks for quick assertions (e.g., UI state after click)
fast = expect.configure(timeout=2.0, polling=0.1)

# Patient checks for slow operations (e.g., page navigation, API calls)
patient = expect.configure(timeout=30.0, polling=0.5)

# Debug variant with screenshots
debug = expect.configure(
    timeout=10.0,
    polling=0.25,
    screenshot_on_failure=True,
    screenshot_path="./debug_screens/",
)

# Use them in tests
def test_quick_check(driver):
    fast(driver.find_element(By.ID, "btn")).to_be_visible()

def test_slow_page_load(driver):
    patient(driver).to_have_title("Dashboard", timeout=60)
```

### Combining global and per-assertion overrides

```python
# Global default: 10s timeout, 0.25s polling
set_default_timeout(10)
set_default_polling_interval(0.25)

# Per-assertion: override for a specific check
expect(element).to_be_visible(timeout=2, polling=0.05)  # quick check
expect(driver).to_have_title("Loaded", timeout=60)      # patient check
expect(element).to_have_text("Ready", polling=[0.1, 0.2, 0.5])  # backoff
```
