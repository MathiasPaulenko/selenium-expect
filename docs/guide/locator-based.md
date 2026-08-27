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
