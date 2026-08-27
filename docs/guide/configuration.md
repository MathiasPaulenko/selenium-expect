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
