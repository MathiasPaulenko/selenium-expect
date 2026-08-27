# API reference

## `expect(target, ...)`

Create an assertion for the given target. Dispatches to the appropriate assertion class based on the target's type.

::: selenium_expect._expect.Expect

## `ExpectConfig`

Immutable configuration dataclass for all assertions.

::: selenium_expect._config.ExpectConfig

## `poll(fn, ...)`

Create a `PollAssertion` for retry-based assertions on an arbitrary function.

::: selenium_expect._poll.poll

## `PollAssertion`

Assertion over an arbitrary function with retry loop.

::: selenium_expect._poll.PollAssertion

## `extend(name)`

Decorator to register a custom matcher under `name`.

::: selenium_expect._matcher.extend

## `merge_expects(*modules)`

Combine custom matchers from multiple modules into the registry.

::: selenium_expect._matcher.merge_expects

## `SoftAssertionCollector`

Collects soft assertion failures for deferred raising.

::: selenium_expect._soft.SoftAssertionCollector

## `assert_all()`

Raise `AssertionError` if any soft failures were collected, then reset.

::: selenium_expect._soft.assert_all

## Configuration setters

### `set_default_timeout(seconds)`

::: selenium_expect._config.set_default_timeout

### `set_default_polling_interval(seconds)`

::: selenium_expect._config.set_default_polling_interval

### `set_default_polling_intervals(intervals)`

::: selenium_expect._config.set_default_polling_intervals

### `set_screenshot_on_failure(enabled, path=None)`

::: selenium_expect._config.set_screenshot_on_failure

### `set_debug_mode(enabled)`

::: selenium_expect._config.set_debug_mode

### `get_config()`

::: selenium_expect._config.get_config

## Assertion classes

### `ExpectElement`

Assertions for `WebElement` objects.

::: selenium_expect.assertions.element.ExpectElement

### `ExpectDriver`

Assertions for `WebDriver` and page-level state.

::: selenium_expect.assertions.driver.ExpectDriver

### `ExpectList`

Assertions for lists of `WebElement` objects.

::: selenium_expect.assertions.list.ExpectList

### `ExpectAlert`

Assertions for JavaScript `Alert` objects.

::: selenium_expect.assertions.alert.ExpectAlert

### `ExpectCookie`

Assertions for browser cookies.

::: selenium_expect.assertions.cookie.ExpectCookie

### `ExpectSelect`

Assertions for HTML `<select>` elements.

::: selenium_expect.assertions.select.ExpectSelect

### `ExpectShadow`

Assertions for `ShadowRoot` elements.

::: selenium_expect.assertions.shadow.ExpectShadow

### `ExpectJS`

Assertions for JavaScript and browser state.

::: selenium_expect.assertions.js.ExpectJS

### `ExpectIframe`

Assertions for iframes.

::: selenium_expect.assertions.iframe.ExpectIframe

### `ExpectWindow`

Assertions for browser window position, size, and rect.

::: selenium_expect.assertions.window.ExpectWindow

### `LocatorExpect`

Locator-based expect that re-finds the element on each poll.

::: selenium_expect._locator.LocatorExpect
