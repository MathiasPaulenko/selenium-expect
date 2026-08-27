# Error messages

When an assertion fails, `selenium-expect` raises an `AssertionError` with a descriptive multi-line message.

## Structure

```text
Expected {entity} {condition}, but got {actual}
  Expected: {expected}
  Actual:   {actual}
  Element:  {truncated_html}
  Waited:   {elapsed_ms}ms ({poll_count} polls at {polling_interval}s interval)
  Message:  {custom_message}
  Timeline: [poll N: actual, ...]
```

## Example

```text
Expected <h1> to have text 'Hello, World!', but got Goodbye
  Expected: Hello, World!
  Actual:   Goodbye
  Element:  <h1 id="greeting">Goodbye</h1>
  Waited:   5001ms (10 polls at 0.5s interval)
  Timeline: [poll 6: Goodbye, poll 7: Goodbye, poll 8: Goodbye, poll 9: Goodbye, poll 10: Goodbye]
```

## Fields

| Field | Description |
|---|---|
| `entity` | Description of the target (e.g. `<h1 id="greeting">`, `driver`, `ShadowRoot`) |
| `condition` | What was expected (e.g. `to have text 'Hello'`) |
| `expected` | Expected value |
| `actual` | Actual value at the last poll |
| `Element` | Truncated `outerHTML` of the element (first 200 chars) |
| `Waited` | Total time waited, poll count, and interval |
| `Message` | Custom message passed via `expect(target, message="...")` |
| `Timeline` | Last 5 poll results for debugging intermittent issues |

## Custom messages

Pass a `message` to `expect()` for additional context:

```python
expect(element, message="Login button should be visible after auth").to_be_visible()
```

## Debug mode

Enable debug logging to see retry loop details in real time:

```python
from selenium_expect import set_debug_mode

set_debug_mode(True)
```

This prints poll count, elapsed time, and actual values to the `selenium_expect` logger.

## Screenshots

Enable automatic screenshot capture on failure:

```python
from selenium_expect import set_screenshot_on_failure

set_screenshot_on_failure(True, path="./screenshots/")
```

Screenshots are saved as `screenshot_{timestamp}_{condition}.png`.

## Examples

### Understanding the timeline

The timeline shows the last 5 poll results, which helps diagnose intermittent issues:

```text
Expected <span id="status"> to have text 'Ready', but got Loading
  Expected: Ready
  Actual:   Loading
  Element:  <span id="status">Loading</span>
  Waited:   5001ms (10 polls at 0.5s interval)
  Timeline: [poll 6: Loading, poll 7: Loading, poll 8: Loading, poll 9: Loading, poll 10: Loading]
```

If the value was changing during the wait, the timeline would show it:

```text
Expected <span id="status"> to have text 'Ready', but got Loading
  Expected: Ready
  Actual:   Loading
  Element:  <span id="status">Loading</span>
  Waited:   5001ms (10 polls at 0.5s interval)
  Timeline: [poll 6: Pending, poll 7: Loading, poll 8: Loading, poll 9: Loading, poll 10: Loading]
```

### Using custom messages for context

```python
# Add context to error messages
expect(
    driver.find_element(By.ID, "checkout-btn"),
    message="Checkout button should be enabled after cart has items"
).to_be_enabled()

expect(
    driver,
    message="Should redirect to dashboard after login"
).to_have_url_contains("/dashboard")
```

### Debug mode output

When debug mode is enabled, each poll prints details:

```text
[selenium_expect] poll 1/10: to be visible → False (elapsed: 0ms)
[selenium_expect] poll 2/10: to be visible → False (elapsed: 501ms)
[selenium_expect] poll 3/10: to be visible → True (elapsed: 1002ms)
```

### Screenshots on failure

```python
from selenium_expect import set_screenshot_on_failure

# Enable with a custom path
set_screenshot_on_failure(True, path="./screenshots/")

# Now any assertion failure saves a screenshot
expect(element).to_be_visible(timeout=5)
# If this fails, you'll find: ./screenshots/screenshot_20240101_120000_to_be_visible.png
```
