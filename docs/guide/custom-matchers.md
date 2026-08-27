# Custom matchers

Custom matchers let you extend `expect()` with your own assertion methods that integrate with the retry loop and negation.

## `@extend` decorator

Register a custom matcher function under a name. The function receives the assertion's target as its first argument and must return a `(bool, Any)` tuple — the bool indicates pass/fail, and the Any is the actual value for error reporting.

```python
from selenium_expect import extend

@extend("to_be_in_viewport")
def check_in_viewport(element):
    driver = element.parent
    script = """
    var rect = arguments[0].getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= window.innerHeight &&
        rect.right <= window.innerWidth
    );
    """
    in_viewport = driver.execute_script(script, element)
    return (in_viewport, "in viewport" if in_viewport else "out of viewport")
```

### Usage

Once registered, the matcher is available on any `expect()` call:

```python
expect(element).to_be_in_viewport()
expect(element).not_.to_be_in_viewport()
expect(element).to_be_in_viewport(timeout=5, polling=0.2)
```

Custom matchers work with:

- `expect(element)` — `ExpectElement`
- `expect(driver)` — `ExpectDriver`
- `expect(driver, by=By.ID, value="foo")` — `LocatorExpect` (re-finds on each poll)
- `expect(items)` — `ExpectList`
- `expect(alert)` — `ExpectAlert`
- `expect(select)` — `ExpectSelect`
- `expect(shadow_root)` — `ExpectShadow`

## `merge_expects()`

Combine custom matchers from multiple modules into the registry:

```python
from selenium_expect import merge_expects

import my_project.matchers
import my_project.custom_assertions

merge_expects(my_project.matchers, my_project.custom_assertions)
```

You can also pass importable strings:

```python
merge_expects("my_project.matchers", "my_project.custom_assertions")
```

## Matcher signature

```python
def my_matcher(target: Any, *args, **kwargs) -> tuple[bool, Any]:
    ...
    return (passed, actual_value)
```

- `target`: The object passed to `expect()` (e.g. `WebElement`, `WebDriver`).
- `*args, **kwargs`: Any additional arguments from the call site (excluding `timeout` and `polling`, which are consumed by the retry loop).
- Return: `(bool, Any)` where `bool` is `True` if the condition passed.

## Example: custom text matcher

```python
from selenium_expect import extend

@extend("to_have_trimmed_text")
def check_trimmed_text(element, expected: str):
    actual = element.text.strip()
    return (actual == expected, actual)

# Usage
expect(element).to_have_trimmed_text("Hello, World!")
```
