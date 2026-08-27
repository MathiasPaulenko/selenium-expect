# Soft assertions

Soft assertions accumulate failures instead of raising immediately. This lets you run multiple checks and collect all failures at once, rather than stopping at the first error.

## Enabling soft mode

### Per-assertion

Pass `soft=True` to any `expect()` call:

```python
expect(element).to_be_visible(soft=True)
expect(element).to_have_text("Hello", soft=True)
```

### Global

Enable soft mode globally via `expect.configure()`:

```python
soft_expect = expect.configure(soft=True)
soft_expect(element).to_be_visible()
soft_expect(element).to_have_text("Hello")
```

## Checking results

Call `assert_all()` to raise a combined `AssertionError` if any failures were collected:

```python
from selenium_expect import assert_all, expect

expect(element).to_be_visible(soft=True)
expect(element).to_have_text("Hello", soft=True)
expect(driver).to_have_title("Dashboard", soft=True)

assert_all()  # raises if any of the above failed
```

The combined error message includes all individual failures separated by `---`:

```text
Soft assertion failures (2):
Expected <h1> to have text 'Hello', but got 'Goodbye'
  Expected: Hello
  Actual:   Goodbye
  Waited:   5000ms (10 polls at 0.5s interval)
---
Expected driver to have title 'Dashboard', but got 'Loading...'
  Expected: Dashboard
  Actual:   Loading...
  Waited:   5000ms (10 polls at 0.5s interval)
```

## `SoftAssertionCollector`

The `SoftAssertionCollector` class manages the failure list:

```python
from selenium_expect import SoftAssertionCollector

SoftAssertionCollector.reset()           # clear collected failures
SoftAssertionCollector.get_failures()    # return list of failure messages
SoftAssertionCollector.assert_all()      # raise + reset
```

## Pattern: test with soft assertions

```python
def test_form_validation(driver):
    SoftAssertionCollector.reset()

    expect(driver.find_element(By.ID, "name")).to_have_value("John", soft=True)
    expect(driver.find_element(By.ID, "email")).to_have_value("john@example.com", soft=True)
    expect(driver.find_element(By.ID, "phone")).to_have_value("+1234567890", soft=True)

    assert_all()
```

## Pattern: soft assertions with pytest

```python
import pytest
from selenium_expect import expect, assert_all, SoftAssertionCollector
from selenium.webdriver.common.by import By

@pytest.fixture(autouse=True)
def reset_soft_assertions():
    SoftAssertionCollector.reset()
    yield

def test_profile_page(driver):
    driver.get("https://app.example.com/profile")

    # All assertions run even if some fail
    expect(driver).to_have_title("Profile", soft=True)
    expect(driver.find_element(By.ID, "name")).to_have_text("John Doe", soft=True)
    expect(driver.find_element(By.ID, "email")).to_have_text_contains("john", soft=True)
    expect(driver.find_element(By.ID, "avatar")).to_be_visible(soft=True)
    expect(driver.find_element(By.ID, "edit-btn")).to_be_clickable(soft=True)

    # Raise if any failed
    assert_all()
```

## Pattern: mixing soft and hard assertions

```python
def test_checkout(driver):
    # Hard assertion — stops immediately if this fails
    expect(driver).to_have_url_contains("/checkout")

    # Soft assertions — collect all failures
    expect(driver.find_element(By.ID, "total")).to_have_text("$99.99", soft=True)
    expect(driver.find_element(By.ID, "item-count")).to_have_text("3 items", soft=True)
    expect(driver.find_element(By.ID, "shipping")).to_have_text("Free", soft=True)

    assert_all()
```

## Pattern: soft assertions with pre-configured expect

```python
from selenium_expect import expect

# Create a soft expect variant
soft_expect = expect.configure(soft=True)

def test_dashboard(driver):
    # All assertions are soft by default
    soft_expect(driver).to_have_title("Dashboard")
    soft_expect(driver.find_element(By.ID, "welcome")).to_have_text_contains("Welcome")
    soft_expect(driver.find_element(By.ID, "stats")).to_be_visible()

    # Check all at once
    assert_all()
```
