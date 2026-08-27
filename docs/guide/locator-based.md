# Locator-based expect

Locator-based `expect` re-finds the element on **every poll cycle**, eliminating `StaleElementReferenceException` in dynamic pages.

## Usage

Pass `by` and `value` (or `locator` tuple) to `expect()` with a `WebDriver` target:

```python
from selenium.webdriver.common.by import By
from selenium_expect import expect

# Using by/value
expect(driver, by=By.ID, value="submit-btn").to_be_visible()

# Using locator tuple
expect(driver, locator=(By.ID, "submit-btn")).to_have_text("Submit")
```

## How it works

`LocatorExpect` calls `driver.find_element(by, value)` on each retry poll. This means:

- If the element is detached and re-attached between polls, the assertion still works.
- If the element doesn't exist yet, the assertion waits for it to appear.
- All `ExpectElement` assertion methods are available via delegation.

## Negation

```python
expect(driver, by=By.ID, value="loading").not_.to_be_visible()
```

## Custom matchers

Custom matchers registered via `@extend` also work with locator-based expect:

```python
@extend("to_be_in_viewport")
def check_in_viewport(element):
    ...

expect(driver, by=By.ID, value="target").to_be_in_viewport()
```

The element is re-found on each poll before the matcher is invoked.

## Per-assertion overrides

```python
expect(driver, by=By.ID, value="dynamic-element").to_be_visible(
    timeout=10, polling=0.2
)
```

## When to use

- **Locator-based**: When the element may be re-rendered or detached (React, Vue, HTMX).
- **Element-based**: When you have a stable reference and want slightly faster polls (no `find_element` overhead).

## Comparison

| Feature | `expect(element)` | `expect(driver, by=..., value=...)` |
|---|---|---|
| Re-finds on each poll | No | Yes |
| `StaleElementReferenceException` | Possible | Avoided |
| All element assertions | Yes | Yes |
| Negation | Yes | Yes |
| Custom matchers | Yes | Yes |
| Overhead per poll | Lower | One `find_element` call |

## Examples

### Waiting for a dynamically rendered element

```python
from selenium.webdriver.common.by import By
from selenium_expect import expect

# React/Vue components may re-render — locator-based handles this
expect(driver, by=By.ID, value="dynamic-list").to_be_visible(timeout=15)
expect(driver, by=By.CSS_SELECTOR, value=".list-item:first-child").to_have_text("First Item")
```

### Waiting for an element to disappear

```python
# Wait for a loading overlay to disappear
expect(driver, by=By.ID, value="loading-overlay").not_.to_be_visible(timeout=30)

# Or use to_be_hidden
expect(driver, by=By.CLASS_NAME, value="spinner").to_be_hidden(timeout=10)
```

### Chaining with locator-based expect

```python
# All element assertions work with locator-based expect
expect(driver, by=By.ID, value="submit").to_be_visible().to_be_enabled().to_be_clickable()

# Text and attribute assertions
expect(driver, by=By.CSS_SELECTOR, value=".alert").to_have_text_contains("Success")
expect(driver, by=By.NAME, value="csrf_token").to_have_attribute_present("value")
```

### Using with different locator strategies

```python
# By ID
expect(driver, by=By.ID, value="login-form").to_be_visible()

# By CSS selector
expect(driver, by=By.CSS_SELECTOR, value="form.login > .submit").to_be_clickable()

# By XPath
expect(driver, by=By.XPATH, value="//div[@role='alert']").to_have_text("Saved")

# By class name
expect(driver, by=By.CLASS_NAME, value="notification").to_be_visible()

# By tag name
expect(driver, by=By.TAG_NAME, value="dialog").to_be_present()

# Using the locator tuple shorthand
expect(driver, locator=(By.CSS_SELECTOR, "button[data-action='save']")).to_be_enabled()
```

### Real-world example — SPA navigation

```python
def test_spa_navigation(driver):
    driver.get("https://app.example.com/")

    # Click a navigation link
    driver.find_element(By.LINK_TEXT, "Settings").click()

    # Wait for the new view to render (element may not exist yet)
    expect(driver, by=By.ID, value="settings-view").to_be_visible(timeout=15)

    # Verify content in the new view
    expect(driver, by=By.CSS_SELECTOR, value="#settings-view h1").to_have_text("Settings")

    # Wait for a form inside the view to be ready
    expect(driver, by=By.ID, value="settings-form").to_be_visible().to_be_enabled()

    # Verify the save button
    expect(driver, by=By.CSS_SELECTOR, value="#settings-form button[type='submit']").to_be_clickable()
```
