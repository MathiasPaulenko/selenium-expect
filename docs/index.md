# selenium-expect

Fluent `expect()` assertions with auto-retry for Selenium Python.

## Why selenium-expect?

Writing Selenium tests traditionally means pairing every check with
`WebDriverWait` and `expected_conditions` — verbose, repetitive, and easy
to get wrong.  `selenium-expect` replaces that pattern with a single
fluent `expect()` call that **auto-retries** until the condition passes
or the timeout expires.

### Before (raw Selenium)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Verbose, repetitive, error-prone
wait = WebDriverWait(driver, 10)
wait.until(EC.title_is("Dashboard"))
wait.until(EC.visibility_of_element_located((By.ID, "welcome")))
element = driver.find_element(By.ID, "welcome")
assert element.text == "Welcome, Alice!"
wait.until(EC.element_to_be_clickable((By.ID, "submit")))
```

### After (selenium-expect)

```python
from selenium_expect import expect

# Concise, fluent, auto-retrying
expect(driver).to_have_title("Dashboard")
welcome = driver.find_element(By.ID, "welcome")
expect(welcome).to_be_visible().to_have_text("Welcome, Alice!")
expect(driver.find_element(By.ID, "submit")).to_be_clickable()
```

## Features

- **Auto-retry**: No more `WebDriverWait` + `expected_conditions` boilerplate. Every assertion polls until it passes or times out.
- **Fluent API**: Chain assertions naturally — `expect(element).to_be_visible().to_have_text("Hello")`
- **Negation**: Use `.not_` to invert any assertion — `expect(element).not_.to_be_disabled()`
- **161 assertions** across 10 categories: driver, element, list, alert, cookie, JS, shadow DOM, select, iframe, window
- **Soft assertions**: Accumulate failures across multiple checks, then raise once at the end with `assert_all()`
- **Custom matchers**: Extend `expect()` with your own assertion methods via the `@extend` decorator
- **Locator-based expect**: Re-find elements on each poll cycle — eliminates `StaleElementReferenceException`
- **Configurable polling**: Fixed interval or custom backoff schedule with `polling_intervals`
- **Descriptive errors**: Timeline, element HTML snippet, actual vs. expected values, and custom messages
- **Composition assertions**: Combine multiple conditions with `to_satisfy_all`, `to_satisfy_any`, `to_satisfy_none`
- **Poll function**: Assert on arbitrary callables with `expect.poll(fn).to_equal(value)`
- **Zero framework dependency**: Works with pytest, unittest, Behave, or standalone scripts
- **Type-safe**: Full type hints, `mypy --strict` compatible
- **Python 3.11+**: Modern Python features throughout

## Quick links

- [Getting started](getting-started.md) — Installation, first assertions, auto-retry explained
- [Assertions reference](assertions/driver.md) — Complete API for every assertion category
- [Guides](guide/configuration.md) — Configuration, soft assertions, custom matchers, and more
- [API reference](api-reference.md) — Full programmatic reference
- [Changelog](changelog.md) — Release history

## Installation

```bash
pip install selenium-expect
```

For development documentation:

```bash
pip install selenium-expect[docs]
```

## Quick example

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect

driver = webdriver.Chrome()
driver.get("https://example.com")

# Driver / page assertions
expect(driver).to_have_title("Example Domain")
expect(driver).to_have_url("https://example.com/")

# Element assertions — chainable
h1 = driver.find_element(By.TAG_NAME, "h1")
expect(h1).to_be_visible().to_have_text("Example Domain")

# Negation
expect(h1).not_.to_be_hidden()

# Locator-based — re-finds on each poll, no StaleElementReferenceException
expect(driver, by=By.ID, value="submit").to_be_clickable(timeout=15)

# Custom timeout and polling per assertion
expect(h1).to_have_text_contains("Example", timeout=5, polling=0.25)
```

## More examples

### Soft assertions

Collect all failures and raise once:

```python
from selenium_expect import expect, assert_all

# Each assertion records failures without raising
expect(driver).to_have_title("Wrong Title", soft=True)
expect(driver.find_element(By.ID, "status")).to_have_text("Ready", soft=True)

# Raise if any soft assertions failed
assert_all()
```

### Custom matchers

Add your own assertion methods:

```python
from selenium_expect import expect, extend

@extend("to_have_color")
def to_have_color(self, color: str):
    """Assert element has a specific CSS color."""
    actual = self._target.value_of_css_property("color")
    if actual != color:
        raise AssertionError(f"Expected color {color!r}, got {actual!r}")

# Now use it like any built-in assertion
expect(element).to_have_color("rgba(255, 0, 0, 1)")
expect(element).not_.to_have_color("rgba(0, 0, 0, 1)")
```

### Polling arbitrary functions

```python
from selenium_expect import expect

# Assert on any callable — auto-retries until it matches
expect.poll(lambda: driver.execute_script("return document.readyState")).to_equal("complete")

# Works with any comparison
expect.poll(lambda: len(driver.find_elements(By.CLASS_NAME, "item"))).to_be_greater_than(5)
```

### Pre-configured expect variants

```python
from selenium_expect import expect

# Create a fast variant for quick checks
fast_expect = expect.configure(timeout=1.0, polling=0.1)
fast_expect(element).to_be_visible()

# Create a patient variant for slow pages
patient_expect = expect.configure(timeout=30.0, polling=0.5)
patient_expect(driver).to_have_title("Loaded")
```

## Comparison with other tools

| Feature | selenium-expect | WebDriverWait + EC |
| --- | --- | --- | --- |
| Auto-retry | Yes | Yes (manual) |
| Fluent chaining | Yes | No |
| Negation | `.not_` | Manual | `.not_` |
| Soft assertions | Yes | No | No |
| Custom matchers | Yes | No | No |
| Locator-based re-find | Yes | Via `EC` |
| Configurable backoff | Yes | No |
| Descriptive errors | Timeline + HTML | Minimal |
| Framework dependency | None | None |
| Browser support | Any Selenium driver | Any Selenium driver |

## License

MIT — see [LICENSE](https://github.com/MathiasPaulenko/selenium-expect/blob/main/LICENSE) for details.
