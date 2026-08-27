# Getting started

## Requirements

- Python >= 3.11
- selenium >= 4.10

## Installation

```bash
pip install selenium-expect
```

## First assertion

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_expect import expect, set_default_timeout

set_default_timeout(10)

driver = webdriver.Chrome()
driver.get("https://example.com")

# Page-level
expect(driver).to_have_title("Example Domain")
expect(driver).to_have_url_contains("example.com")

# Element-level
heading = driver.find_element(By.TAG_NAME, "h1")
expect(heading).to_be_visible()
expect(heading).to_have_text("Example Domain")

# Negation
expect(heading).not_.to_have_text("Goodbye")

driver.quit()
```

## Auto-retry explained

Every assertion runs in a retry loop. By default, the loop polls every **0.5 seconds** for up to **5 seconds**. If the condition is not met within the timeout, an `AssertionError` is raised with a descriptive multi-line message.

You can override the timeout and polling interval globally or per-assertion:

```python
# Global defaults
from selenium_expect import set_default_timeout, set_default_polling_interval

set_default_timeout(10)
set_default_polling_interval(0.25)

# Per-assertion override
expect(element).to_be_visible(timeout=2, polling=0.1)
```

### Backoff schedule

Instead of a fixed interval, you can provide a list of intervals that are cycled through:

```python
from selenium_expect import set_default_polling_intervals

set_default_polling_intervals([0.1, 0.2, 0.5, 1.0])

# Or per-assertion
expect(element).to_be_visible(polling=[0.1, 0.2, 0.5])
```

## Negation

Every assertion supports negation via the `.not_` property:

```python
expect(element).not_.to_be_visible()      # assert element is NOT visible
expect(element).not_.to_have_text("Hi")   # assert text is NOT "Hi"
expect(driver).not_.to_have_title("Loading...")
```

## Next steps

- [Driver / Page assertions](assertions/driver.md)
- [Element assertions](assertions/element.md)
- [List assertions](assertions/list.md)
- [Configuration](guide/configuration.md)
- [Soft assertions](guide/soft-assertions.md)
- [Custom matchers](guide/custom-matchers.md)
- [Locator-based expect](guide/locator-based.md)
- [expect.poll()](guide/poll.md)
