# Getting started

## Requirements

- Python >= 3.11
- selenium >= 4.10

## Installation

```bash
pip install selenium-expect
```

Verify the installation:

```python
import selenium_expect
print(selenium_expect.__version__)
```

## First assertion

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect, set_default_timeout

set_default_timeout(10)

driver = webdriver.Chrome()
driver.get("https://example.com")

# Page-level assertions
expect(driver).to_have_title("Example Domain")
expect(driver).to_have_url_contains("example.com")

# Element-level assertions
heading = driver.find_element(By.TAG_NAME, "h1")
expect(heading).to_be_visible()
expect(heading).to_have_text("Example Domain")

# Negation
expect(heading).not_.to_have_text("Goodbye")

driver.quit()
```

## Chaining assertions

Assertions return `self`, so you can chain them fluently:

```python
# Chain multiple assertions on the same element
expect(login_button).to_be_visible().to_be_enabled().to_be_clickable()

# Chain text and attribute checks
expect(name_field).to_have_attribute("placeholder", "Enter your name").to_have_value("")

# Chain driver-level checks
expect(driver).to_have_title_contains("Dashboard").to_have_url_contains("/dashboard")
```

!!! note "Chaining and negation"
    When you use `.not_`, the negation applies to **all** assertions in the chain:

    ```python
    # Both assertions are negated
    expect(element).not_.to_be_visible().to_have_text("Loading")
    ```

## Auto-retry explained

Every assertion runs in a retry loop. By default, the loop polls every **0.5 seconds** for up to **5 seconds**. If the condition is not met within the timeout, an `AssertionError` is raised with a descriptive multi-line message.

### How the retry loop works

```text
┌──────────────────────────────────────────────────┐
│  expect(element).to_be_visible(timeout=5)        │
├──────────────────────────────────────────────────┤
│  1. Evaluate condition (element.is_displayed())  │
│  2. If True  → assertion passes, return          │
│  3. If False → sleep(polling_interval)           │
│  4. Repeat until timeout expires                 │
│  5. Timeout   → raise AssertionError with        │
│                 timeline, expected vs. actual    │
└──────────────────────────────────────────────────┘
```

### Global defaults

```python
from selenium_expect import (
    set_default_timeout,
    set_default_polling_interval,
)

set_default_timeout(10)          # 10 seconds
set_default_polling_interval(0.25)  # poll every 250ms
```

### Per-assertion override

```python
# Quick check — 2 second timeout, 100ms polling
expect(element).to_be_visible(timeout=2, polling=0.1)

# Patient check — 30 second timeout for slow pages
expect(driver).to_have_title("Loaded", timeout=30)

# Override polling only (uses global timeout)
expect(element).to_have_text("Ready", polling=0.05)
```

### Backoff schedule

Instead of a fixed interval, provide a list of intervals that are cycled through. This is useful for scenarios where you want to poll frequently at first, then back off:

```python
from selenium_expect import set_default_polling_intervals

# Poll at 100ms, 200ms, 500ms, 1s, then cycle
set_default_polling_intervals([0.1, 0.2, 0.5, 1.0])

# Or per-assertion
expect(element).to_be_visible(polling=[0.1, 0.2, 0.5])

# With a long timeout and backoff
expect(driver).to_have_title("Ready", timeout=60, polling=[0.5, 1.0, 2.0, 5.0])
```

## Negation

Every assertion supports negation via the `.not_` property:

```python
# Element is NOT visible
expect(element).not_.to_be_visible()

# Text is NOT "Hi"
expect(element).not_.to_have_text("Hi")

# Title is NOT "Loading..."
expect(driver).not_.to_have_title("Loading...")

# Element is NOT disabled (i.e., it's enabled)
expect(button).not_.to_be_disabled()

# URL does NOT contain "/login"
expect(driver).not_.to_have_url_contains("/login")
```

Negation works with **every** assertion — driver, element, list, alert, cookie, select, shadow, JS, iframe, and window assertions all support `.not_`.

## Locator-based expect

Instead of passing a `WebElement`, pass a `WebDriver` with `by` and `value` to re-find the element on each poll cycle. This eliminates `StaleElementReferenceException`:

```python
from selenium.webdriver.common.by import By

# Re-finds the element on every poll — no stale element errors
expect(driver, by=By.ID, value="dynamic-content").to_be_visible(timeout=15)

# Works with all element assertions
expect(driver, by=By.CSS_SELECTOR, value=".alert").to_have_text_contains("Success")

# Negation works too
expect(driver, by=By.ID, value="loading-spinner").not_.to_be_visible(timeout=10)

# Tuple shorthand
expect(driver, locator=(By.XPATH, "//div[@class='result']")).to_have_text("Done")
```

See [Locator-based expect](guide/locator-based.md) for full details.

## Using with pytest

`selenium-expect` works seamlessly with pytest. Assertion failures raise `AssertionError`, which pytest reports naturally:

```python
# test_login.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_login_success(driver):
    driver.get("https://app.example.com/login")

    # Fill in the form
    driver.find_element(By.ID, "username").send_keys("alice")
    driver.find_element(By.ID, "password").send_keys("secret")
    driver.find_element(By.ID, "submit").click()

    # Assert the result — auto-retries handle timing
    expect(driver).to_have_url_contains("/dashboard")
    expect(driver).to_have_title("Dashboard | Example App")

    welcome = driver.find_element(By.ID, "welcome-message")
    expect(welcome).to_be_visible().to_have_text_contains("Welcome, Alice!")

    # Verify the logout button is clickable
    expect(driver.find_element(By.ID, "logout")).to_be_clickable()
```

## Using with Behave (BDD)

```python
# features/steps/login_steps.py
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect

@given("I am on the login page")
def step_on_login_page(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://app.example.com/login")

@when('I log in as "{username}" with password "{password}"')
def step_login(context, username, password):
    context.driver.find_element(By.ID, "username").send_keys(username)
    context.driver.find_element(By.ID, "password").send_keys(password)
    context.driver.find_element(By.ID, "submit").click()

@then('I should see the dashboard')
def step_see_dashboard(context):
    expect(context.driver).to_have_title("Dashboard")
    expect(context.driver).to_have_url_contains("/dashboard")

@then('I should see "Welcome, {name}!"')
def step_welcome(context, name):
    el = context.driver.find_element(By.ID, "welcome-message")
    expect(el).to_be_visible().to_have_text(f"Welcome, {name}!")
```

## Error messages

When an assertion fails, the error message includes a timeline, the expected vs. actual values, and (for elements) an HTML snippet:

```text
AssertionError: Expected element to be visible
  Entity: <h1 id="title">
  Expected: True
  Actual:   False
  Timeout:  5.00s (10 polls × 0.50s)
  Timeline:
    [0.00s] not visible
    [0.50s] not visible
    [1.00s] not visible
    ...
    [5.00s] not visible
  Message: custom message here (if provided)
```

See [Error messages](guide/error-messages.md) for full details.

## Next steps

- [Driver / Page assertions](assertions/driver.md) — Title, URL, ready state, capabilities, and more
- [Element assertions](assertions/element.md) — Visibility, text, attributes, CSS, position, accessibility
- [List assertions](assertions/list.md) — Count, texts, values, aggregate state
- [Alert assertions](assertions/alert.md) — Presence and text of JavaScript alerts
- [Cookie assertions](assertions/cookie.md) — Presence, value, domain, path, security flags
- [Select assertions](assertions/select.md) — Dropdown values, selected options, option count
- [Shadow DOM assertions](assertions/shadow.md) — Shadow root elements
- [JS / Browser state assertions](assertions/js.md) — JavaScript results, localStorage, sessionStorage
- [Iframe assertions](assertions/iframe.md) — Frame availability, count, content
- [Window assertions](assertions/window.md) — Position, size, rect
- [Configuration](guide/configuration.md) — Global and per-assertion settings
- [Soft assertions](guide/soft-assertions.md) — Accumulate failures
- [Custom matchers](guide/custom-matchers.md) — Extend with your own assertions
- [Locator-based expect](guide/locator-based.md) — Re-find elements on each poll
- [Composition assertions](guide/composition.md) — Combine multiple conditions
- [expect.poll()](guide/poll.md) — Assert on arbitrary callables
- [Error messages](guide/error-messages.md) — Understanding failure output
- [Migration guide](guide/migration.md) — Migrate from WebDriverWait
