# selenium-expect

Playwright-style `expect()` assertions with auto-retry for Selenium Python.

## Features

- **Auto-retry**: No more `WebDriverWait` + `expected_conditions` boilerplate
- **Fluent API**: `expect(element).to_be_visible().to_have_text("Hello")`
- **Negation**: `expect(element).not_.to_be_disabled()`
- **161 assertions** across 10 categories: driver, element, list, alert, cookie, JS, shadow DOM, select, iframe, window
- **Soft assertions**: Accumulate failures, check at the end
- **Custom matchers**: Extend `expect()` with your own assertions
- **Locator-based**: Re-find elements on each poll — no `StaleElementReferenceException`
- **Configurable polling**: Fixed interval or backoff schedule
- **Descriptive errors**: Timeline, element HTML, and custom messages
- **Zero framework dependency**: Works with pytest, unittest, Behave, or standalone

## Quick links

- [Getting started](getting-started.md)
- [Assertions reference](assertions/driver.md)
- [Configuration](guide/configuration.md)
- [API reference](api-reference.md)

## Installation

```bash
pip install selenium-expect
```

## Example

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect

driver = webdriver.Chrome()
driver.get("https://example.com")

expect(driver).to_have_title("Example Domain")
expect(driver.find_element(By.TAG_NAME, "h1")).to_have_text("Example Domain")
```
